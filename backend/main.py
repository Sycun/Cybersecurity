from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse, FileResponse
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from sqlalchemy import text
from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import mimetypes
import magic

from database import SessionLocal, engine, Base
from models import Question, Tool, AutoSolve, SolveTemplate
from schemas import QuestionCreate, QuestionResponse, ToolResponse, AnalysisRequest, AutoSolveRequest, AutoSolveResponse, SolveTemplateCreate, SolveTemplateResponse, CodeExecutionRequest, CodeExecutionResponse, ConversationCreateRequest, MessageRequest
from ai_service import AIService, extract_structured_content
from auto_solver import AutoSolver
from utils import detect_question_type, get_recommended_tools
from config import config
from logger import get_logger
from cache import ai_response_cache
from data_service import data_service
from conversation_service import conversation_service

# 加载环境变量
load_dotenv()

# 设置日志
logger = get_logger("main")

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CTF智能分析平台",
    description="支持多AI提供者的CTF题目智能分析平台，包括DeepSeek、硅基流动、本地模型和OpenAI兼容API",
    version="2.1.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖注入：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 初始化AI服务
ai_service = AIService()

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """根路径"""
    return {"message": "CTF智能分析平台API", "version": "2.1.0"}

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 检查数据库连接
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "healthy",
            "database": "healthy",
            "ai_provider": ai_service.provider_type,
            "cache_enabled": config.ENABLE_CACHE,
            "timestamp": "2024-01-01T12:00:00.000000"
        }
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"服务异常: {str(e)}")

@app.post("/api/analyze")
async def analyze_challenge(
    description: str = Form(...),
    question_type: str = Form(...),
    ai_provider: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    conversation_id: Optional[str] = Form(None),
    use_context: bool = Form(True),
    file: Optional[UploadFile] = File(None),
    file_type: Optional[str] = Form(None)
):
    """分析CTF题目，支持多模态文件上传"""
    try:
        # 文件类型自动识别
        detected_type = None
        file_content = None
        if file:
            file_content = await file.read()
            detected_type = file_type or file.content_type or mimetypes.guess_type(file.filename)[0]
            if not detected_type and file_content:
                try:
                    detected_type = magic.from_buffer(file_content, mime=True)
                except Exception:
                    detected_type = None

        # 多模态分析分发
        multimodal_context = {}
        if detected_type:
            if detected_type.startswith("image/"):
                # 图片分析（如OCR/隐写）
                multimodal_context["image"] = file_content
            elif detected_type in ["application/vnd.tcpdump.pcap", "application/octet-stream"] and file.filename.endswith(".pcap"):
                multimodal_context["pcap"] = file_content
            elif detected_type in ["application/x-executable", "application/x-dosexec", "application/octet-stream"]:
                multimodal_context["binary"] = file_content
            else:
                multimodal_context["file"] = file_content

        # 创建或获取对话会话
        conv_id = conversation_id
        if not conv_id:
            conv_id = conversation_service.create_conversation(
                user_id=user_id,
                initial_context={"question_type": question_type}
            )
        conversation_service.add_message(
            conversation_id=conv_id,
            role="user",
            content=description,
            metadata={"question_type": question_type, "ai_provider": ai_provider, "file_type": detected_type}
        )

        # 构建多轮对话提示词（可拼接文件摘要/特征）
        enhanced_prompt = description
        if multimodal_context:
            enhanced_prompt += f"\n\n[文件类型: {detected_type}, 文件名: {file.filename}]"
            # TODO: 可插入自动摘要/特征提取

        # 调用AI分析
        if ai_provider and ai_provider != ai_service.provider_type:
            ai_service.switch_provider(ai_provider)
        response = await ai_service.analyze_challenge(
            enhanced_prompt,
            question_type,
            user_id=user_id,
            use_context=use_context,
            conversation_id=conv_id
        )
        conversation_service.add_message(
            conversation_id=conv_id,
            role="assistant",
            content=response,
            metadata={"ai_provider": ai_service.provider_type}
        )
        analysis_data = {
            "description": description,
            "question_type": question_type,
            "ai_response": response,
            "ai_provider": ai_service.provider_type,
            "conversation_id": conv_id,
            "use_context": use_context,
            "file_type": detected_type,
            "file_name": file.filename if file else None
        }
        data_service.save_analysis_history(analysis_data)
        structured = extract_structured_content(response)
        return {
            "success": True,
            "response": response,
            "structured": structured,
            "conversation_id": conv_id,
            "ai_provider": ai_service.provider_type,
            "file_type": detected_type
        }
    except Exception as e:
        logger.error(f"分析题目失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"分析题目失败: {str(e)}")

@app.post("/api/auto-solve", response_model=AutoSolveResponse)
async def auto_solve_challenge(
    description: str = Form(...),
    question_type: str = Form(...),
    template_id: Optional[str] = Form(None),
    custom_code: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    file_type: Optional[str] = Form(None)
):
    """自动解题，支持多模态文件上传"""
    try:
        logger.info(f"收到自动解题请求，题目类型: {question_type}")
        # 文件类型自动识别
        detected_type = None
        file_content = None
        if file:
            file_content = await file.read()
            detected_type = file_type or file.content_type or mimetypes.guess_type(file.filename)[0]
            if not detected_type and file_content:
                try:
                    detected_type = magic.from_buffer(file_content, mime=True)
                except Exception:
                    detected_type = None
        # 多模态参数准备
        multimodal_params = {}
        file_info = None
        if file_content:
            file_info = {
                "file": file_content,
                "file_type": detected_type,
                "file_name": file.filename
            }
            multimodal_params = {"file": file_content, "file_type": detected_type, "file_name": file.filename}
        # 创建自动解题引擎
        auto_solver = AutoSolver(ai_service=ai_service)
        # 执行自动解题
        result = await auto_solver.solve_challenge(
            question_id=None,  # 支持无题库ID
            solve_method=template_id,
            custom_code=custom_code,
            parameters=multimodal_params if multimodal_params else None,
            description=description,
            question_type=question_type,
            file_info=file_info
        )
        # 自动分析失败原因
        ai_suggestion = None
        if result.get("status") == "failed" and result.get("error_message"):
            ai_suggestion = await ai_service.analyze_challenge(
                f"自动解题失败，错误信息如下：\n{result['error_message']}\n请分析失败原因并给出改进建议。",
                question_type
            )
            result["ai_suggestion"] = ai_suggestion
        logger.info(f"自动解题完成，状态: {result['status']}")
        structured = extract_structured_content(result.get('generated_code', ""))
        return AutoSolveResponse(
            id=result.get('id', ""),
            question_id=result.get('question_id', ""),
            status=result.get('status', ""),
            solve_method=result.get('solve_method', ""),
            generated_code=result.get('generated_code', ""),
            execution_result=result.get('execution_result', ""),
            flag=result.get('flag', ""),
            error_message=result.get('error_message', ""),
            execution_time=result.get('execution_time', 0),
            created_at=result.get('created_at', ""),
            completed_at=result.get('completed_at', ""),
            structured=structured,
            success=result.get('status', "") == "completed",
            response=result.get('execution_result', ""),
            ai_suggestion=ai_suggestion
        )
    except Exception as e:
        logger.error(f"自动解题失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"自动解题失败: {str(e)}")

@app.get("/api/auto-solve/{solve_id}", response_model=AutoSolveResponse)
async def get_auto_solve_result(solve_id: str):
    """获取自动解题结果"""
    try:
        auto_solve = data_service.get_auto_solve(solve_id)
        if not auto_solve:
            raise HTTPException(status_code=404, detail="解题记录不存在")
        
        return AutoSolveResponse(
            id=auto_solve['id'],
            question_id=auto_solve['question_id'],
            status=auto_solve['status'],
            solve_method=auto_solve['solve_method'],
            generated_code=auto_solve['generated_code'],
            execution_result=auto_solve['execution_result'],
            flag=auto_solve['flag'],
            error_message=auto_solve['error_message'],
            execution_time=auto_solve['execution_time'],
            created_at=auto_solve['created_at'],
            completed_at=auto_solve['completed_at']
        )
        
    except Exception as e:
        logger.error(f"获取解题结果失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取解题结果失败: {str(e)}")

@app.get("/api/auto-solves")
async def get_auto_solves(question_id: str = None, limit: int = 50):
    """获取自动解题记录列表"""
    try:
        auto_solves = data_service.get_auto_solves(question_id=question_id, limit=limit)
        return auto_solves
    except Exception as e:
        logger.error(f"获取自动解题记录失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取自动解题记录失败: {str(e)}")

@app.post("/api/execute-code", response_model=CodeExecutionResponse)
async def execute_code(
    request: CodeExecutionRequest,
    db: Session = Depends(get_db)
):
    """执行代码（安全沙箱）"""
    try:
        logger.info(f"收到代码执行请求，语言: {request.language}")
        
        # 创建自动解题引擎用于代码执行
        auto_solver = AutoSolver(db, ai_service)
        
        # 执行代码
        execution_result, flag, error = await auto_solver._execute_code(
            code=request.code,
            language=request.language,
            parameters={"input": request.input_data} if request.input_data else None
        )
        
        return CodeExecutionResponse(
            success=not bool(error),
            output=execution_result,
            error=error,
            execution_time=0.0,  # 这里可以添加实际的时间计算
            memory_usage=None
        )
        
    except Exception as e:
        logger.error(f"代码执行失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"代码执行失败: {str(e)}")

@app.get("/api/solve-templates", response_model=list[SolveTemplateResponse])
async def get_solve_templates(
    category: str = None,
    db: Session = Depends(get_db)
):
    """获取解题模板"""
    try:
        auto_solver = AutoSolver(db, ai_service)
        templates = await auto_solver.get_solve_templates(category)
        
        return [
            SolveTemplateResponse(
                id=template.get('id'),
                name=template.get('name'),
                category=template.get('category'),
                description=template.get('description'),
                template_code=template.get('template_code'),
                parameters=template.get('parameters', {}),
                is_active=template.get('is_active', True),
                created_at=template.get('created_at')
            )
            for template in templates
        ]
        
    except Exception as e:
        logger.error(f"获取解题模板失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取解题模板失败: {str(e)}")

@app.post("/api/solve-templates", response_model=SolveTemplateResponse)
async def create_solve_template(
    request: SolveTemplateCreate,
    db: Session = Depends(get_db)
):
    """创建解题模板"""
    try:
        auto_solver = AutoSolver(db, ai_service)
        template = await auto_solver.create_solve_template(request.dict())
        
        return SolveTemplateResponse(
            id=template.get('id'),
            name=template.get('name'),
            category=template.get('category'),
            description=template.get('description'),
            template_code=template.get('template_code'),
            parameters=template.get('parameters', {}),
            is_active=template.get('is_active', True),
            created_at=template.get('created_at')
        )
        
    except Exception as e:
        logger.error(f"创建解题模板失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"创建解题模板失败: {str(e)}")

@app.put("/api/solve-templates/{name}")
async def update_solve_template(
    name: str,
    request: SolveTemplateCreate,
    db: Session = Depends(get_db)
):
    """更新解题模板"""
    try:
        auto_solver = AutoSolver(db, ai_service)
        success = await auto_solver.update_solve_template(name, request.dict())
        
        if not success:
            raise HTTPException(status_code=404, detail="模板不存在")
        
        return {"message": "模板更新成功"}
        
    except Exception as e:
        logger.error(f"更新解题模板失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"更新解题模板失败: {str(e)}")

@app.delete("/api/solve-templates/{name}")
async def delete_solve_template(
    name: str,
    db: Session = Depends(get_db)
):
    """删除解题模板"""
    try:
        auto_solver = AutoSolver(db, ai_service)
        success = await auto_solver.delete_solve_template(name)
        
        if not success:
            raise HTTPException(status_code=404, detail="模板不存在")
        
        return {"message": "模板删除成功"}
        
    except Exception as e:
        logger.error(f"删除解题模板失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"删除解题模板失败: {str(e)}")

@app.post("/api/solve-templates/{name}/enable")
async def enable_solve_template(
    name: str,
    db: Session = Depends(get_db)
):
    """启用解题模板"""
    try:
        auto_solver = AutoSolver(db, ai_service)
        success = await auto_solver.enable_solve_template(name)
        
        if not success:
            raise HTTPException(status_code=404, detail="模板不存在")
        
        return {"message": "模板启用成功"}
        
    except Exception as e:
        logger.error(f"启用解题模板失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"启用解题模板失败: {str(e)}")

@app.post("/api/solve-templates/{name}/disable")
async def disable_solve_template(
    name: str,
    db: Session = Depends(get_db)
):
    """禁用解题模板"""
    try:
        auto_solver = AutoSolver(db, ai_service)
        success = await auto_solver.disable_solve_template(name)
        
        if not success:
            raise HTTPException(status_code=404, detail="模板不存在")
        
        return {"message": "模板禁用成功"}
        
    except Exception as e:
        logger.error(f"禁用解题模板失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"禁用解题模板失败: {str(e)}")

@app.get("/api/challenges")
async def get_challenges(challenge_type: str = None, limit: int = 50):
    """获取题目列表"""
    try:
        challenges = data_service.get_challenges(challenge_type=challenge_type, limit=limit)
        
        return [
            {
                "id": challenge["id"],
                "description": challenge["description"][:100] + "..." if len(challenge["description"]) > 100 else challenge["description"],
                "type": challenge["type"],
                "timestamp": challenge["timestamp"]
            }
            for challenge in challenges
        ]
    except Exception as e:
        logger.error(f"获取题目列表失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取题目列表失败: {str(e)}")

@app.get("/api/challenges/{challenge_id}")
async def get_challenge_detail(challenge_id: str):
    """获取题目详情"""
    try:
        challenge = data_service.get_challenge(challenge_id)
        if not challenge:
            raise HTTPException(status_code=404, detail="题目不存在")
        
        return challenge
    except Exception as e:
        logger.error(f"获取题目详情失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取题目详情失败: {str(e)}")

@app.get("/api/history")
async def get_history():
    """获取分析历史"""
    try:
        history = data_service.get_analysis_history(limit=50)
        return [
            {
                "id": h["id"],
                "challenge_id": h["challenge_id"],
                "description": h["analysis_data"]["description"][:100] + "..." if len(h["analysis_data"]["description"]) > 100 else h["analysis_data"]["description"],
                "type": h["analysis_data"]["type"],
                "timestamp": h["timestamp"]
            }
            for h in history
        ]
    except Exception as e:
        logger.error(f"获取历史记录失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """获取统计信息"""
    try:
        stats = data_service.get_stats()
        
        return {
            "total_questions": stats["total_challenges"],
            "type_stats": stats["challenges_by_type"],
            "total_history": stats["total_history"]
        }
    except Exception as e:
        logger.error(f"获取统计信息失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

@app.get("/api/ai-providers")
async def get_ai_providers():
    """获取可用的AI提供者"""
    try:
        from ai_providers import AIProviderFactory
        
        available_providers = AIProviderFactory.get_available_providers()
        current_provider = ai_service.provider_type
        
        return {
            "current_provider": current_provider,
            "current_provider_info": available_providers.get(current_provider, {}),
            "available_providers": available_providers
        }
    except Exception as e:
        logger.error(f"获取AI提供者失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取AI提供者失败: {str(e)}")

@app.post("/api/ai-providers/switch")
async def switch_ai_provider(provider_type: str = Body(..., embed=True)):
    """切换AI提供者"""
    try:
        success = ai_service.switch_provider(provider_type)
        if success:
            # 保存到用户配置
            user_config = data_service.get_user_config()
            user_config["ai_provider"] = provider_type
            data_service.save_user_config(user_config)
            
            return {
                "message": f"AI提供者切换成功: {provider_type}",
                "current_provider": provider_type
            }
        else:
            raise HTTPException(status_code=400, detail="AI提供者切换失败")
    except Exception as e:
        logger.error(f"切换AI提供者失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"切换AI提供者失败: {str(e)}")

@app.get("/api/ai-providers/status")
async def get_ai_provider_status():
    """获取AI提供者状态和性能统计"""
    try:
        stats = ai_service.get_performance_stats()
        provider_info = ai_service.get_provider_info()
        
        return {
            "provider_info": provider_info,
            "performance_stats": stats
        }
    except Exception as e:
        logger.error(f"获取AI提供者状态失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取AI提供者状态失败: {str(e)}")

@app.post("/api/conversations")
async def create_conversation(request: ConversationCreateRequest):
    """创建新的对话会话"""
    try:
        conversation_id = conversation_service.create_conversation(
            user_id=request.user_id,
            initial_context=request.initial_context
        )
        
        return {
            "success": True,
            "conversation_id": conversation_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """获取对话详情"""
    try:
        conversation = data_service.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="对话不存在")
        
        return {
            "success": True,
            "conversation": conversation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/user/{user_id}")
async def get_user_conversations(user_id: str, limit: int = 10):
    """获取用户的对话列表"""
    try:
        conversations = data_service.get_user_conversations(user_id, limit)
        
        return {
            "success": True,
            "conversations": conversations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """删除对话"""
    try:
        success = data_service.delete_conversation(conversation_id)
        if not success:
            raise HTTPException(status_code=404, detail="对话不存在")
        
        return {
            "success": True,
            "message": "对话已删除"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/conversations/{conversation_id}/messages")
async def add_message(conversation_id: str, request: MessageRequest):
    """添加消息到对话"""
    try:
        success = conversation_service.add_message(
            conversation_id=conversation_id,
            role=request.role,
            content=request.content,
            metadata=request.metadata
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="对话不存在")
        
        return {
            "success": True,
            "message": "消息已添加"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tools")
async def get_tools(category: str = None):
    """获取工具列表"""
    try:
        tools = data_service.get_tools(category=category)
        return tools
    except Exception as e:
        logger.error(f"获取工具列表失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取工具列表失败: {str(e)}")

@app.get("/api/tools/{name}")
async def get_tool_detail(name: str):
    """获取工具详情"""
    try:
        tool = data_service.get_tool_by_name(name)
        if not tool:
            raise HTTPException(status_code=404, detail="工具不存在")
        return tool
    except Exception as e:
        logger.error(f"获取工具详情失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取工具详情失败: {str(e)}")

@app.post("/api/tools")
async def add_tool(tool: dict = Body(...)):
    """添加工具"""
    try:
        if not tool.get('name'):
            raise HTTPException(status_code=400, detail="工具名称不能为空")
        
        # 检查工具是否已存在
        existing_tool = data_service.get_tool_by_name(tool['name'])
        if existing_tool:
            raise HTTPException(status_code=400, detail="工具已存在")
        
        # 生成新的ID
        tools = data_service.get_tools()
        max_id = max([t.get('id', 0) for t in tools]) if tools else 0
        tool['id'] = max_id + 1
        
        success = data_service.add_tool(tool)
        if not success:
            raise HTTPException(status_code=500, detail="添加工具失败")
        
        return {"success": True, "tool": tool}
    except Exception as e:
        logger.error(f"添加工具失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"添加工具失败: {str(e)}")

@app.put("/api/tools/{name}")
async def update_tool(name: str, updated_tool: dict = Body(...)):
    """更新工具"""
    try:
        success = data_service.update_tool(name, updated_tool)
        if not success:
            raise HTTPException(status_code=404, detail="工具不存在")
        
        return {"success": True}
    except Exception as e:
        logger.error(f"更新工具失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"更新工具失败: {str(e)}")

@app.delete("/api/tools/{name}")
async def delete_tool(name: str):
    """删除工具"""
    try:
        success = data_service.delete_tool(name)
        if not success:
            raise HTTPException(status_code=404, detail="工具不存在")
        
        return {"success": True}
    except Exception as e:
        logger.error(f"删除工具失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"删除工具失败: {str(e)}")

@app.get("/api/user-config")
async def get_user_config():
    """获取用户配置"""
    try:
        config = data_service.get_config("user_config")
        if not config:
            raise HTTPException(status_code=404, detail="未找到用户配置")
        return config
    except Exception as e:
        logger.error(f"获取用户配置失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取用户配置失败: {str(e)}")

@app.post("/api/user-config")
async def save_user_config(config: dict = Body(...)):
    """保存用户配置"""
    try:
        ok = data_service.save_config("user_config", config)
        if not ok:
            raise HTTPException(status_code=500, detail="保存配置失败")
        return {"success": True}
    except Exception as e:
        logger.error(f"保存用户配置失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"保存用户配置失败: {str(e)}")

@app.post("/api/export/{data_type}")
async def export_data(data_type: str, format: str = "json"):
    """导出数据"""
    try:
        if data_type == "history":
            data = data_service.get_analysis_history(limit=1000)
        elif data_type == "challenges":
            data = data_service.get_challenges(limit=1000)
        elif data_type == "configs":
            data = [data_service.get_all_configs()]
        else:
            raise HTTPException(status_code=400, detail=f"不支持的数据类型: {data_type}")
        
        if not data:
            raise HTTPException(status_code=404, detail=f"没有找到{data_type}数据")
        
        file_path = data_service.export_data(data_type, data, format)
        filename = file_path.split("/")[-1]
        
        return {
            "success": True,
            "filename": filename,
            "file_path": file_path,
            "data_count": len(data),
            "format": format
        }
    except Exception as e:
        logger.error(f"导出{data_type}失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")

@app.get("/api/exports")
async def list_exports():
    """获取可下载的导出文件列表"""
    try:
        exports = []
        for file_path in sorted(data_service.exports_dir.glob("export_*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            exports.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "created_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
        return exports
    except Exception as e:
        logger.error(f"获取导出文件列表失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取导出文件列表失败: {str(e)}")

@app.get("/api/exports/{filename}")
async def download_export(filename: str):
    """下载指定导出文件"""
    try:
        file_path = data_service.exports_dir / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type="application/octet-stream"
        )
    except Exception as e:
        logger.error(f"下载导出文件失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"下载失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.BACKEND_HOST, port=config.BACKEND_PORT) 