import os
from typing import Optional, List
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()

class Config:
    """应用配置类"""
    
    def __init__(self):
        self.logger = get_logger("config")
        self._validate_config()
    
    # 基础配置
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ctf_analyzer.db")
    
    # 服务器配置
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "3000"))
    
    # CORS配置
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS", 
        "http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")
    
    # AI服务配置
    AI_SERVICE: str = os.getenv("AI_SERVICE", "deepseek")
    
    # DeepSeek配置
    DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_URL: str = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # 硅基流动配置
    SILICONFLOW_API_KEY: Optional[str] = os.getenv("SILICONFLOW_API_KEY")
    SILICONFLOW_API_URL: str = os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.cn/v1/chat/completions")
    SILICONFLOW_MODEL: str = os.getenv("SILICONFLOW_MODEL", "Qwen/QwQ-32B")
    
    # 本地模型配置
    LOCAL_MODEL_PATH: Optional[str] = os.getenv("LOCAL_MODEL_PATH")
    LOCAL_MODEL_TYPE: str = os.getenv("LOCAL_MODEL_TYPE", "auto")
    LOCAL_MODEL_DEVICE: str = os.getenv("LOCAL_MODEL_DEVICE", "auto")
    LOCAL_MODEL_MAX_LENGTH: int = int(os.getenv("LOCAL_MODEL_MAX_LENGTH", "4096"))
    LOCAL_MODEL_TEMPERATURE: float = float(os.getenv("LOCAL_MODEL_TEMPERATURE", "0.7"))
    
    # OpenAI兼容API配置
    OPENAI_COMPATIBLE_API_URL: Optional[str] = os.getenv("OPENAI_COMPATIBLE_API_URL")
    OPENAI_COMPATIBLE_API_KEY: str = os.getenv("OPENAI_COMPATIBLE_API_KEY", "sk-no-key-required")
    OPENAI_COMPATIBLE_MODEL: str = os.getenv("OPENAI_COMPATIBLE_MODEL", "gpt-3.5-turbo")
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # 性能配置
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "60"))
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    
    # 缓存配置
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "False").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1小时
    
    def _validate_config(self):
        """验证配置"""
        errors = []
        
        # 验证AI服务配置
        if self.AI_SERVICE == "deepseek" and not self.DEEPSEEK_API_KEY:
            errors.append("使用DeepSeek服务时，DEEPSEEK_API_KEY不能为空")
        
        if self.AI_SERVICE == "siliconflow" and not self.SILICONFLOW_API_KEY:
            errors.append("使用硅基流动服务时，SILICONFLOW_API_KEY不能为空")
        
        if self.AI_SERVICE == "local" and not self.LOCAL_MODEL_PATH:
            errors.append("使用本地模型时，LOCAL_MODEL_PATH不能为空")
        
        if self.AI_SERVICE == "openai_compatible" and not self.OPENAI_COMPATIBLE_API_URL:
            errors.append("使用OpenAI兼容API时，OPENAI_COMPATIBLE_API_URL不能为空")
        
        # 验证端口配置
        if not (1 <= self.BACKEND_PORT <= 65535):
            errors.append(f"BACKEND_PORT必须在1-65535之间，当前值: {self.BACKEND_PORT}")
        
        if not (1 <= self.FRONTEND_PORT <= 65535):
            errors.append(f"FRONTEND_PORT必须在1-65535之间，当前值: {self.FRONTEND_PORT}")
        
        if errors:
            for error in errors:
                self.logger.error(f"配置错误: {error}")
            raise ValueError(f"配置验证失败: {'; '.join(errors)}")
        
        self.logger.info("配置验证通过")
    
    def get_ai_provider_config(self) -> dict:
        """获取当前AI提供者的配置"""
        if self.AI_SERVICE == "deepseek":
            return {
                "api_key": self.DEEPSEEK_API_KEY,
                "api_url": self.DEEPSEEK_API_URL,
                "model": self.DEEPSEEK_MODEL
            }
        elif self.AI_SERVICE == "siliconflow":
            return {
                "api_key": self.SILICONFLOW_API_KEY,
                "api_url": self.SILICONFLOW_API_URL,
                "model": self.SILICONFLOW_MODEL
            }
        elif self.AI_SERVICE == "local":
            return {
                "model_path": self.LOCAL_MODEL_PATH,
                "model_type": self.LOCAL_MODEL_TYPE,
                "device": self.LOCAL_MODEL_DEVICE,
                "max_length": self.LOCAL_MODEL_MAX_LENGTH,
                "temperature": self.LOCAL_MODEL_TEMPERATURE
            }
        elif self.AI_SERVICE == "openai_compatible":
            return {
                "api_url": self.OPENAI_COMPATIBLE_API_URL,
                "api_key": self.OPENAI_COMPATIBLE_API_KEY,
                "model": self.OPENAI_COMPATIBLE_MODEL
            }
        else:
            raise ValueError(f"不支持的AI服务类型: {self.AI_SERVICE}")
    
    def is_production(self) -> bool:
        """判断是否为生产环境"""
        return not self.DEBUG
    
    def __str__(self):
        """返回配置摘要（隐藏敏感信息）"""
        return f"Config(AI_SERVICE={self.AI_SERVICE}, DEBUG={self.DEBUG}, PORT={self.BACKEND_PORT})"

# 全局配置实例
config = Config() 