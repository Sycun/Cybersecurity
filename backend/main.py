from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from database import SessionLocal, engine, Base
from models import Question, Tool
from schemas import QuestionCreate, QuestionResponse, ToolResponse, AnalysisRequest
from ai_service import AIService
from utils import detect_question_type, get_recommended_tools

# 加载环境变量
load_dotenv()

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CTF智能分析平台",
    description="基于DeepSeek AI的CTF题目智能分析平台",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
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

@app.get("/")
async def root():
    return {"message": "CTF智能分析平台API"}

@app.post("/api/analyze", response_model=QuestionResponse)
async def analyze_challenge(
    text: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """分析CTF题目"""
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=True
    ) 