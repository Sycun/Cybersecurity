from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Question(Base):
    """题目分析记录表"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False, comment="题目描述")
    type = Column(String(50), nullable=False, comment="题目类型")
    ai_response = Column(Text, comment="AI分析结果")
    file_name = Column(String(255), comment="上传的文件名")
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

class Tool(Base):
    """CTF工具表"""
    __tablename__ = "tools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="工具名称")
    description = Column(Text, comment="工具描述")
    command_template = Column(Text, comment="命令模板")
    applicable_types = Column(String(255), comment="适用的题目类型，逗号分隔")
    category = Column(String(50), comment="工具分类")
    is_active = Column(Boolean, default=True, comment="是否启用")
    
class LearningResource(Base):
    """学习资源表"""
    __tablename__ = "learning_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, comment="资源标题")
    url = Column(String(500), comment="资源链接")
    description = Column(Text, comment="资源描述")
    type = Column(String(50), comment="资源类型：tutorial, writeup, tool_doc等")
    applicable_types = Column(String(255), comment="适用的题目类型")
    difficulty = Column(String(20), comment="难度：beginner, intermediate, advanced")
    is_active = Column(Boolean, default=True, comment="是否启用") 