from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class QuestionCreate(BaseModel):
    """创建题目请求模型"""
    description: str
    type: Optional[str] = None
    file_name: Optional[str] = None

class AnalysisRequest(BaseModel):
    """分析请求模型"""
    text: Optional[str] = None
    file_content: Optional[str] = None
    file_name: Optional[str] = None

class ToolResponse(BaseModel):
    """工具响应模型"""
    id: int
    name: str
    description: Optional[str] = None
    command_template: Optional[str] = None
    category: Optional[str] = None
    
    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    """题目分析响应模型"""
    id: int
    description: str
    type: str
    ai_response: Optional[str] = None
    recommended_tools: List[ToolResponse] = []
    timestamp: datetime
    
    class Config:
        from_attributes = True

class LearningResourceResponse(BaseModel):
    """学习资源响应模型"""
    id: int
    title: str
    url: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    difficulty: Optional[str] = None
    
    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    """统计信息响应模型"""
    total_questions: int
    type_stats: dict 