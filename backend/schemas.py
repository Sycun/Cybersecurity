from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import UploadFile

class QuestionCreate(BaseModel):
    """创建题目请求模型"""
    description: str
    question_type: str
    file_name: Optional[str] = None

class AnalysisRequest(BaseModel):
    """分析请求模型"""
    description: str
    question_type: str
    ai_provider: Optional[str] = None
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    use_context: bool = True
    file: Optional[UploadFile] = None
    file_type: Optional[str] = None

class ToolResponse(BaseModel):
    """工具响应模型"""
    id: int
    name: str
    description: str
    category: str
    usage: str
    command: str
    
    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    """题目分析响应模型"""
    id: str
    description: str
    type: str
    ai_response: str
    recommended_tools: List[Dict[str, Any]]
    file_name: Optional[str] = None
    timestamp: str
    ai_provider: Optional[str] = None
    
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

class AutoSolveRequest(BaseModel):
    description: str
    question_type: str
    template_id: Optional[str] = None
    custom_code: Optional[str] = None
    file: Optional[UploadFile] = None
    file_type: Optional[str] = None

class AutoSolveResponse(BaseModel):
    id: Optional[str] = None
    success: bool
    response: str
    flag: Optional[str] = None
    status: Optional[str] = None
    error: Optional[str] = None
    ai_suggestion: Optional[str] = None
    execution_time: Optional[float] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    structured: Optional[Dict[str, Any]] = None

class SolveTemplateCreate(BaseModel):
    name: str
    description: str
    question_type: str
    template_code: str
    parameters: Optional[Dict[str, Any]] = None

class SolveTemplateResponse(BaseModel):
    id: str
    name: str
    description: str
    question_type: str
    template_code: str
    parameters: Optional[Dict[str, Any]] = None
    created_at: str

class CodeExecutionRequest(BaseModel):
    code: str
    question_type: str
    parameters: Optional[Dict[str, Any]] = None

class CodeExecutionResponse(BaseModel):
    success: bool
    output: str
    execution_time: float
    error: Optional[str] = None

class AIProviderInfo(BaseModel):
    name: str
    type: str
    status: str
    description: str
    config: Dict[str, Any]

class ConversationCreateRequest(BaseModel):
    user_id: Optional[str] = None
    initial_context: Optional[Dict[str, Any]] = None

class MessageRequest(BaseModel):
    role: str  # "user" 或 "assistant"
    content: str
    metadata: Optional[Dict[str, Any]] = None

class ConversationResponse(BaseModel):
    id: str
    user_id: Optional[str]
    created_at: str
    updated_at: str
    messages: List[Dict[str, Any]]
    context: Dict[str, Any]
    metadata: Dict[str, Any]

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str
    metadata: Dict[str, Any]

class AnalysisResponse(BaseModel):
    success: bool
    response: str
    structured: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None
    ai_provider: Optional[str] = None 