from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
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
    """工具推荐表"""
    __tablename__ = "tools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="工具名称")
    description = Column(Text, comment="工具描述")
    command = Column(Text, comment="使用命令")
    category = Column(String(50), comment="工具分类")

class AutoSolve(Base):
    """自动解题记录表"""
    __tablename__ = "auto_solves"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, nullable=False, comment="关联的题目ID")
    status = Column(String(20), default="pending", comment="解题状态: pending, running, completed, failed")
    solve_method = Column(String(50), comment="解题方法")
    generated_code = Column(Text, comment="生成的解题代码")
    execution_result = Column(Text, comment="执行结果")
    flag = Column(String(500), comment="获取到的flag")
    error_message = Column(Text, comment="错误信息")
    execution_time = Column(Integer, comment="执行时间(秒)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    completed_at = Column(DateTime(timezone=True), comment="完成时间")

class SolveTemplate(Base):
    """解题模板表"""
    __tablename__ = "solve_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="模板名称")
    category = Column(String(50), nullable=False, comment="题目类型")
    description = Column(Text, comment="模板描述")
    template_code = Column(Text, nullable=False, comment="模板代码")
    parameters = Column(JSON, comment="参数配置")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

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