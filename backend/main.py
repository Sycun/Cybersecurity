from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from sqlalchemy import text

from database import SessionLocal, engine, Base
from models import Question, Tool
from schemas import QuestionCreate, QuestionResponse, ToolResponse, AnalysisRequest
from ai_service import AIService
from utils import detect_question_type, get_recommended_tools
from config import config
from logger import get_logger
from cache import ai_response_cache

# 加载环境变量
load_dotenv()

# 设置日志
logger = get_logger("main")

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CTF智能分析平台",
    description="支持多AI提供者的CTF题目智能分析平台，包括DeepSeek、硅基流动、本地模型和OpenAI兼容API",
    version="2.0.0"
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
logger.info("CTF智能分析平台启动")

@app.get("/")
async def root():
    return {"message": "CTF智能分析平台API", "version": "2.0.0"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    try:
        # 检查数据库连接
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"数据库健康检查失败: {str(e)}")
        db_status = "unhealthy"
    
    # 获取AI服务信息
    provider_info = ai_service.get_provider_info()
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database": db_status,
        "ai_provider": provider_info["current_provider"],
        "cache_enabled": config.ENABLE_CACHE,
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }

@app.get("/api/stats/performance")
async def get_performance_stats():
    """获取性能统计信息"""
    try:
        stats = ai_service.get_performance_stats()
        return {
            "ai_performance": stats,
            "config": {
                "cache_enabled": config.ENABLE_CACHE,
                "cache_ttl": config.CACHE_TTL,
                "request_timeout": config.REQUEST_TIMEOUT
            }
        }
    except Exception as e:
        logger.error(f"获取性能统计失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取性能统计失败: {str(e)}")

@app.post("/api/cache/clear")
async def clear_cache():
    """清空缓存"""
    try:
        ai_service.clear_cache()
        return {"message": "缓存已清空"}
    except Exception as e:
        logger.error(f"清空缓存失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"清空缓存失败: {str(e)}")

@app.get("/api/cache/stats")
async def get_cache_stats():
    """获取缓存统计信息"""
    try:
        return ai_response_cache.get_cache_stats()
    except Exception as e:
        logger.error(f"获取缓存统计失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取缓存统计失败: {str(e)}")

@app.post("/api/analyze", response_model=QuestionResponse)
async def analyze_challenge(
    text: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """分析CTF题目"""
    try:
        logger.info("收到分析请求")
        
        # 获取题目描述
        description = ""
        file_content = ""
        
        if text:
            description = text
        
        if file:
            # 检查文件大小
            file_content = await file.read()
            if len(file_content) > config.MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail=f"文件大小超过限制 ({config.MAX_FILE_SIZE} bytes)")
            
            if file.content_type and file.content_type.startswith('text/'):
                description += f"\n文件内容:\n{file_content.decode('utf-8')}"
            else:
                description += f"\n上传了文件: {file.filename} (二进制文件)"
        
        if not description.strip():
            raise HTTPException(status_code=400, detail="请提供题目描述或上传文件")
        
        # 检测题目类型
        question_type = detect_question_type(description, file.filename if file else None)
        logger.info(f"检测到题目类型: {question_type}")
        
        # 调用AI分析
        ai_response = await ai_service.analyze_challenge(description, question_type)
        
        # 获取推荐工具
        recommended_tools = get_recommended_tools(question_type, db)
        
        # 保存到数据库
        db_question = Question(
            description=description,
            type=question_type,
            ai_response=ai_response,
            file_name=file.filename if file else None
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        logger.info(f"分析完成，题目ID: {db_question.id}")
        
        return QuestionResponse(
            id=db_question.id,
            description=description,
            type=question_type,
            ai_response=ai_response,
            recommended_tools=recommended_tools,
            timestamp=db_question.timestamp
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"分析请求失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@app.get("/api/tools/{question_type}", response_model=list[ToolResponse])
async def get_tools_by_type(question_type: str, db: Session = Depends(get_db)):
    """根据题目类型获取推荐工具"""
    tools = get_recommended_tools(question_type, db)
    return tools

@app.get("/api/history", response_model=list[QuestionResponse])
async def get_history(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """获取历史分析记录"""
    questions = db.query(Question).offset(skip).limit(limit).all()
    
    result = []
    for question in questions:
        tools = get_recommended_tools(question.type, db)
        result.append(QuestionResponse(
            id=question.id,
            description=question.description,
            type=question.type,
            ai_response=question.ai_response,
            recommended_tools=tools,
            timestamp=question.timestamp
        ))
    
    return result

@app.delete("/api/history/{question_id}")
async def delete_history_item(question_id: int, db: Session = Depends(get_db)):
    """删除历史记录"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    db.delete(question)
    db.commit()
    return {"message": "删除成功"}

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """获取统计信息"""
    total_questions = db.query(Question).count()
    
    # 按类型统计
    type_stats = {}
    for question_type in ["web", "pwn", "reverse", "crypto", "misc"]:
        count = db.query(Question).filter(Question.type == question_type).count()
        type_stats[question_type] = count
    
    return {
        "total_questions": total_questions,
        "type_stats": type_stats
    }

@app.get("/api/ai/providers")
async def get_ai_providers():
    """获取可用的AI提供者列表"""
    try:
        providers = AIService.get_available_providers()
        current_info = ai_service.get_provider_info()
        
        return {
            "available_providers": providers,
            "current_provider": current_info["current_provider"],
            "current_provider_name": current_info["current_provider_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取AI提供者信息失败: {str(e)}")

@app.post("/api/ai/switch")
async def switch_ai_provider(provider_type: str = Form(...)):
    """切换AI提供者"""
    try:
        success = ai_service.switch_provider(provider_type)
        if success:
            return {
                "message": f"成功切换到 {provider_type}",
                "current_provider": provider_type
            }
        else:
            raise HTTPException(status_code=400, detail="切换AI提供者失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"切换AI提供者失败: {str(e)}")

@app.post("/api/analyze/with-provider", response_model=QuestionResponse)
async def analyze_challenge_with_provider(
    text: str = Form(None),
    file: UploadFile = File(None),
    provider: str = Form(None),
    db: Session = Depends(get_db)
):
    """使用指定AI提供者分析CTF题目"""
    try:
        # 获取题目描述
        description = ""
        file_content = ""
        
        if text:
            description = text
        
        if file:
            file_content = await file.read()
            if file.content_type and file.content_type.startswith('text/'):
                description += f"\n文件内容:\n{file_content.decode('utf-8')}"
            else:
                description += f"\n上传了文件: {file.filename} (二进制文件)"
        
        if not description.strip():
            raise HTTPException(status_code=400, detail="请提供题目描述或上传文件")
        
        # 检测题目类型
        question_type = detect_question_type(description, file.filename if file else None)
        
        # 如果指定了提供者，创建临时AI服务实例
        if provider:
            temp_ai_service = AIService(provider_type=provider)
            ai_response = await temp_ai_service.analyze_challenge(description, question_type)
            used_provider = provider
        else:
            ai_response = await ai_service.analyze_challenge(description, question_type)
            used_provider = ai_service.provider_type
        
        # 获取推荐工具
        recommended_tools = get_recommended_tools(question_type, db)
        
        # 保存到数据库
        db_question = Question(
            description=description,
            type=question_type,
            ai_response=ai_response,
            file_name=file.filename if file else None
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        return QuestionResponse(
            id=db_question.id,
            description=description,
            type=question_type,
            ai_response=ai_response,
            recommended_tools=recommended_tools,
            timestamp=db_question.timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@app.get("/api/settings")
async def get_settings():
    """获取当前AI服务配置"""
    try:
        from config import config
        
        # 获取当前配置，但隐藏敏感信息
        settings = {
            "provider": config.AI_SERVICE,
            "deepseek_api_url": config.DEEPSEEK_API_URL,
            "deepseek_model": config.DEEPSEEK_MODEL,
            "siliconflow_api_url": config.SILICONFLOW_API_URL, 
            "siliconflow_model": config.SILICONFLOW_MODEL,
            "openai_compatible_api_url": config.OPENAI_COMPATIBLE_API_URL,
            "openai_compatible_model": config.OPENAI_COMPATIBLE_MODEL,
            "local_model_path": config.LOCAL_MODEL_PATH,
            "local_model_type": config.LOCAL_MODEL_TYPE,
            "local_model_device": config.LOCAL_MODEL_DEVICE,
            "local_model_max_length": config.LOCAL_MODEL_MAX_LENGTH,
            "local_model_temperature": config.LOCAL_MODEL_TEMPERATURE,
        }
        
        # 只返回非空的API Key的长度提示
        if config.DEEPSEEK_API_KEY:
            settings["deepseek_api_key"] = "*" * min(len(config.DEEPSEEK_API_KEY), 8) + "..." if len(config.DEEPSEEK_API_KEY) > 8 else "*" * len(config.DEEPSEEK_API_KEY)
        
        if config.SILICONFLOW_API_KEY:
            settings["siliconflow_api_key"] = "*" * min(len(config.SILICONFLOW_API_KEY), 8) + "..." if len(config.SILICONFLOW_API_KEY) > 8 else "*" * len(config.SILICONFLOW_API_KEY)
        
        if config.OPENAI_COMPATIBLE_API_KEY:
            settings["openai_compatible_api_key"] = "*" * min(len(config.OPENAI_COMPATIBLE_API_KEY), 8) + "..." if len(config.OPENAI_COMPATIBLE_API_KEY) > 8 else "*" * len(config.OPENAI_COMPATIBLE_API_KEY)
        
        return settings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取配置失败: {str(e)}")

@app.post("/api/settings")
async def update_settings(settings: dict):
    """更新AI服务配置"""
    try:
        import os
        from dotenv import set_key
        
        env_file = ".env"
        
        # 映射前端字段到环境变量
        env_mapping = {
            "provider": "AI_SERVICE",
            "deepseek_api_key": "DEEPSEEK_API_KEY",
            "deepseek_api_url": "DEEPSEEK_API_URL", 
            "deepseek_model": "DEEPSEEK_MODEL",
            "siliconflow_api_key": "SILICONFLOW_API_KEY",
            "siliconflow_api_url": "SILICONFLOW_API_URL",
            "siliconflow_model": "SILICONFLOW_MODEL",
            "openai_compatible_api_url": "OPENAI_COMPATIBLE_API_URL",
            "openai_compatible_api_key": "OPENAI_COMPATIBLE_API_KEY",
            "openai_compatible_model": "OPENAI_COMPATIBLE_MODEL",
            "local_model_path": "LOCAL_MODEL_PATH",
            "local_model_type": "LOCAL_MODEL_TYPE", 
            "local_model_device": "LOCAL_MODEL_DEVICE",
            "local_model_max_length": "LOCAL_MODEL_MAX_LENGTH",
            "local_model_temperature": "LOCAL_MODEL_TEMPERATURE",
        }
        
        # 更新环境变量文件
        for field, env_var in env_mapping.items():
            if field in settings and settings[field] is not None:
                # 跳过掩码的API Key
                if field.endswith('_api_key') and str(settings[field]).startswith('*'):
                    continue
                set_key(env_file, env_var, str(settings[field]))
        
        # 重新创建AI服务实例以应用新配置
        global ai_service
        from config import Config
        from ai_service import AIService
        
        # 重新加载配置
        new_config = Config()
        ai_service = AIService(provider_type=new_config.AI_SERVICE)
        
        return {"message": "配置更新成功"}
        
    except Exception as e:
        logger.error(f"更新配置失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"更新配置失败: {str(e)}")

@app.post("/api/test-connection")
async def test_connection(request: dict):
    """测试AI服务连接"""
    try:
        provider = request.get("provider")
        
        if not provider:
            # 测试当前配置
            test_ai_service = ai_service
        else:
            # 测试指定提供者
            test_ai_service = AIService(provider_type=provider)
        
        # 发送简单的测试请求
        test_response = await test_ai_service.analyze_challenge(
            "这是一个连接测试",
            "misc"
        )
        
        if test_response and len(test_response.strip()) > 0:
            return {"message": f"连接成功 - {provider or ai_service.provider_type}"}
        else:
            raise Exception("AI服务返回空响应")
            
    except Exception as e:
        logger.error(f"连接测试失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"连接测试失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=True
    ) 