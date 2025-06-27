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
    
    # =============================================================================
    # 基础配置
    # =============================================================================
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-this-in-production")
    
    # =============================================================================
    # 数据库配置
    # =============================================================================
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ctf_analyzer.db")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    DATABASE_TIMEOUT: int = int(os.getenv("DATABASE_TIMEOUT", "30"))
    DATABASE_RETRY_ATTEMPTS: int = int(os.getenv("DATABASE_RETRY_ATTEMPTS", "3"))
    DATABASE_RETRY_DELAY: int = int(os.getenv("DATABASE_RETRY_DELAY", "1"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    
    # =============================================================================
    # 服务器配置
    # =============================================================================
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "3000"))
    WORKER_PROCESSES: int = int(os.getenv("WORKER_PROCESSES", "1"))
    MAX_CONNECTIONS: int = int(os.getenv("MAX_CONNECTIONS", "1000"))
    
    # =============================================================================
    # CORS配置
    # =============================================================================
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS", 
        "http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")
    ENABLE_CORS: bool = os.getenv("ENABLE_CORS", "true").lower() == "true"
    CORS_ALLOW_METHODS: str = os.getenv("CORS_ALLOW_METHODS", "GET,POST,PUT,DELETE,OPTIONS")
    CORS_ALLOW_HEADERS: str = os.getenv("CORS_ALLOW_HEADERS", "*")
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    
    # =============================================================================
    # AI服务配置
    # =============================================================================
    AI_SERVICE: str = os.getenv("AI_SERVICE", "deepseek")
    DEFAULT_AI_MODEL: str = os.getenv("DEFAULT_AI_MODEL", "deepseek-chat")
    AI_REQUEST_TIMEOUT: int = int(os.getenv("AI_REQUEST_TIMEOUT", "120"))
    AI_MAX_RETRIES: int = int(os.getenv("AI_MAX_RETRIES", "3"))
    AI_RETRY_DELAY: int = int(os.getenv("AI_RETRY_DELAY", "1"))
    
    # =============================================================================
    # DeepSeek配置
    # =============================================================================
    DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_URL: str = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    DEEPSEEK_MAX_TOKENS: int = int(os.getenv("DEEPSEEK_MAX_TOKENS", "4096"))
    DEEPSEEK_TEMPERATURE: float = float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7"))
    
    # =============================================================================
    # 硅基流动配置
    # =============================================================================
    SILICONFLOW_API_KEY: Optional[str] = os.getenv("SILICONFLOW_API_KEY")
    SILICONFLOW_API_URL: str = os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.cn/v1/chat/completions")
    SILICONFLOW_MODEL: str = os.getenv("SILICONFLOW_MODEL", "Qwen/QwQ-32B")
    SILICONFLOW_MAX_TOKENS: int = int(os.getenv("SILICONFLOW_MAX_TOKENS", "4096"))
    SILICONFLOW_TEMPERATURE: float = float(os.getenv("SILICONFLOW_TEMPERATURE", "0.7"))
    
    # =============================================================================
    # 本地模型配置
    # =============================================================================
    LOCAL_MODEL_PATH: Optional[str] = os.getenv("LOCAL_MODEL_PATH")
    LOCAL_MODEL_TYPE: str = os.getenv("LOCAL_MODEL_TYPE", "auto")
    LOCAL_MODEL_DEVICE: str = os.getenv("LOCAL_MODEL_DEVICE", "auto")
    LOCAL_MODEL_MAX_LENGTH: int = int(os.getenv("LOCAL_MODEL_MAX_LENGTH", "4096"))
    LOCAL_MODEL_TEMPERATURE: float = float(os.getenv("LOCAL_MODEL_TEMPERATURE", "0.7"))
    LOCAL_MODEL_LOAD_TIMEOUT: int = int(os.getenv("LOCAL_MODEL_LOAD_TIMEOUT", "300"))
    
    # =============================================================================
    # OpenAI兼容API配置
    # =============================================================================
    OPENAI_COMPATIBLE_API_URL: Optional[str] = os.getenv("OPENAI_COMPATIBLE_API_URL")
    OPENAI_COMPATIBLE_API_KEY: str = os.getenv("OPENAI_COMPATIBLE_API_KEY", "sk-no-key-required")
    OPENAI_COMPATIBLE_MODEL: str = os.getenv("OPENAI_COMPATIBLE_MODEL", "gpt-3.5-turbo")
    OPENAI_COMPATIBLE_MAX_TOKENS: int = int(os.getenv("OPENAI_COMPATIBLE_MAX_TOKENS", "4096"))
    OPENAI_COMPATIBLE_TEMPERATURE: float = float(os.getenv("OPENAI_COMPATIBLE_TEMPERATURE", "0.7"))
    
    # =============================================================================
    # Anthropic Claude配置
    # =============================================================================
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_API_URL: str = os.getenv("ANTHROPIC_API_URL", "https://api.anthropic.com/v1/messages")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
    ANTHROPIC_MAX_TOKENS: int = int(os.getenv("ANTHROPIC_MAX_TOKENS", "4096"))
    ANTHROPIC_TEMPERATURE: float = float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7"))
    
    # =============================================================================
    # Azure OpenAI配置
    # =============================================================================
    AZURE_OPENAI_API_KEY: Optional[str] = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT: Optional[str] = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT_NAME: Optional[str] = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    AZURE_OPENAI_MODEL: str = os.getenv("AZURE_OPENAI_MODEL", "gpt-4")
    
    # =============================================================================
    # 安全配置
    # =============================================================================
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    JWT_REFRESH_HOURS: int = int(os.getenv("JWT_REFRESH_HOURS", "168"))
    PASSWORD_SALT_ROUNDS: int = int(os.getenv("PASSWORD_SALT_ROUNDS", "12"))
    ENABLE_HTTPS: bool = os.getenv("ENABLE_HTTPS", "false").lower() == "true"
    SSL_CERT_PATH: Optional[str] = os.getenv("SSL_CERT_PATH")
    SSL_KEY_PATH: Optional[str] = os.getenv("SSL_KEY_PATH")
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    LOGIN_LOCKOUT_MINUTES: int = int(os.getenv("LOGIN_LOCKOUT_MINUTES", "15"))
    
    # =============================================================================
    # 日志配置
    # =============================================================================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    LOG_MAX_SIZE: int = int(os.getenv("LOG_MAX_SIZE", "10"))
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    ENABLE_CONSOLE_LOG: bool = os.getenv("ENABLE_CONSOLE_LOG", "true").lower() == "true"
    ENABLE_STRUCTURED_LOGGING: bool = os.getenv("ENABLE_STRUCTURED_LOGGING", "false").lower() == "true"
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # =============================================================================
    # 性能配置
    # =============================================================================
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "60"))
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    ALLOWED_FILE_TYPES: List[str] = os.getenv(
        "ALLOWED_FILE_TYPES", 
        "image/*,text/*,application/json,application/xml"
    ).split(",")
    UPLOAD_CONCURRENCY: int = int(os.getenv("UPLOAD_CONCURRENCY", "5"))
    MEMORY_CACHE_SIZE: int = int(os.getenv("MEMORY_CACHE_SIZE", "100"))
    
    # =============================================================================
    # 缓存配置
    # =============================================================================
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1小时
    CACHE_MAX_ENTRIES: int = int(os.getenv("CACHE_MAX_ENTRIES", "1000"))
    CACHE_CLEANUP_INTERVAL: int = int(os.getenv("CACHE_CLEANUP_INTERVAL", "300"))
    CACHE_TYPE: str = os.getenv("CACHE_TYPE", "memory")
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    MEMCACHED_SERVERS: str = os.getenv("MEMCACHED_SERVERS", "localhost:11211")
    
    # =============================================================================
    # 邮件配置
    # =============================================================================
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "noreply@yourdomain.com")
    SMTP_TIMEOUT: int = int(os.getenv("SMTP_TIMEOUT", "30"))
    SMTP_RETRY_ATTEMPTS: int = int(os.getenv("SMTP_RETRY_ATTEMPTS", "3"))
    
    # =============================================================================
    # 监控配置
    # =============================================================================
    ENABLE_MONITORING: bool = os.getenv("ENABLE_MONITORING", "true").lower() == "true"
    MONITORING_RETENTION_DAYS: int = int(os.getenv("MONITORING_RETENTION_DAYS", "30"))
    ENABLE_HEALTH_CHECK: bool = os.getenv("ENABLE_HEALTH_CHECK", "true").lower() == "true"
    HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "60"))
    METRICS_COLLECTION_INTERVAL: int = int(os.getenv("METRICS_COLLECTION_INTERVAL", "30"))
    ENABLE_APM: bool = os.getenv("ENABLE_APM", "false").lower() == "true"
    APM_SERVER_URL: str = os.getenv("APM_SERVER_URL", "http://localhost:8200")
    
    # =============================================================================
    # 备份配置
    # =============================================================================
    ENABLE_AUTO_BACKUP: bool = os.getenv("ENABLE_AUTO_BACKUP", "false").lower() == "true"
    BACKUP_DIR: str = os.getenv("BACKUP_DIR", "backups")
    BACKUP_RETENTION_DAYS: int = int(os.getenv("BACKUP_RETENTION_DAYS", "7"))
    BACKUP_SCHEDULE: str = os.getenv("BACKUP_SCHEDULE", "0 2 * * *")
    BACKUP_COMPRESSION: str = os.getenv("BACKUP_COMPRESSION", "zip")
    BACKUP_ENCRYPTION_KEY: Optional[str] = os.getenv("BACKUP_ENCRYPTION_KEY")
    
    # =============================================================================
    # 第三方服务配置
    # =============================================================================
    GITHUB_CLIENT_ID: Optional[str] = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET: Optional[str] = os.getenv("GITHUB_CLIENT_SECRET")
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    WECHAT_APP_ID: Optional[str] = os.getenv("WECHAT_APP_ID")
    WECHAT_APP_SECRET: Optional[str] = os.getenv("WECHAT_APP_SECRET")
    DISCORD_WEBHOOK_URL: Optional[str] = os.getenv("DISCORD_WEBHOOK_URL")
    SLACK_WEBHOOK_URL: Optional[str] = os.getenv("SLACK_WEBHOOK_URL")
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # =============================================================================
    # 开发环境配置
    # =============================================================================
    ENABLE_HOT_RELOAD: bool = os.getenv("ENABLE_HOT_RELOAD", "true").lower() == "true"
    ENABLE_DETAILED_ERRORS: bool = os.getenv("ENABLE_DETAILED_ERRORS", "false").lower() == "true"
    DEV_SERVER_HOST: str = os.getenv("DEV_SERVER_HOST", "localhost")
    DEV_SERVER_PORT: int = int(os.getenv("DEV_SERVER_PORT", "3000"))
    ENABLE_DEBUG_TOOLBAR: bool = os.getenv("ENABLE_DEBUG_TOOLBAR", "false").lower() == "true"
    ENABLE_SQL_LOGGING: bool = os.getenv("ENABLE_SQL_LOGGING", "false").lower() == "true"
    
    # =============================================================================
    # 生产环境配置
    # =============================================================================
    PRODUCTION_DOMAIN: str = os.getenv("PRODUCTION_DOMAIN", "yourdomain.com")
    CDN_URL: Optional[str] = os.getenv("CDN_URL")
    STATIC_FILES_DIR: str = os.getenv("STATIC_FILES_DIR", "static")
    ENABLE_COMPRESSION: bool = os.getenv("ENABLE_COMPRESSION", "true").lower() == "true"
    ENABLE_CACHE_HEADERS: bool = os.getenv("ENABLE_CACHE_HEADERS", "true").lower() == "true"
    ENABLE_GZIP: bool = os.getenv("ENABLE_GZIP", "true").lower() == "true"
    ENABLE_BROTLI: bool = os.getenv("ENABLE_BROTLI", "false").lower() == "true"
    STATIC_CACHE_TTL: int = int(os.getenv("STATIC_CACHE_TTL", "86400"))
    
    # =============================================================================
    # 容器化配置
    # =============================================================================
    DOCKER_IMAGE_TAG: str = os.getenv("DOCKER_IMAGE_TAG", "latest")
    CONTAINER_MEMORY_LIMIT: str = os.getenv("CONTAINER_MEMORY_LIMIT", "1g")
    CONTAINER_CPU_LIMIT: str = os.getenv("CONTAINER_CPU_LIMIT", "1.0")
    CONTAINER_RESTART_POLICY: str = os.getenv("CONTAINER_RESTART_POLICY", "unless-stopped")
    CONTAINER_HEALTH_TIMEOUT: int = int(os.getenv("CONTAINER_HEALTH_TIMEOUT", "10"))
    
    # =============================================================================
    # 网络配置
    # =============================================================================
    PROXY_URL: Optional[str] = os.getenv("PROXY_URL")
    PROXY_USERNAME: Optional[str] = os.getenv("PROXY_USERNAME")
    PROXY_PASSWORD: Optional[str] = os.getenv("PROXY_PASSWORD")
    SKIP_SSL_VERIFY: bool = os.getenv("SKIP_SSL_VERIFY", "false").lower() == "true"
    CUSTOM_USER_AGENT: str = os.getenv("CUSTOM_USER_AGENT", "CTF-Analyzer/2.1.0")
    
    # =============================================================================
    # 功能开关
    # =============================================================================
    ENABLE_AUTO_SOLVE: bool = os.getenv("ENABLE_AUTO_SOLVE", "true").lower() == "true"
    ENABLE_CODE_EXECUTION: bool = os.getenv("ENABLE_CODE_EXECUTION", "true").lower() == "true"
    ENABLE_FILE_UPLOAD: bool = os.getenv("ENABLE_FILE_UPLOAD", "true").lower() == "true"
    ENABLE_CONVERSATION: bool = os.getenv("ENABLE_CONVERSATION", "true").lower() == "true"
    ENABLE_AUTHENTICATION: bool = os.getenv("ENABLE_AUTHENTICATION", "false").lower() == "true"
    ENABLE_REGISTRATION: bool = os.getenv("ENABLE_REGISTRATION", "false").lower() == "true"
    ENABLE_RATE_LIMITING: bool = os.getenv("ENABLE_RATE_LIMITING", "false").lower() == "true"
    ENABLE_IP_WHITELIST: bool = os.getenv("ENABLE_IP_WHITELIST", "false").lower() == "true"
    
    # =============================================================================
    # 限流配置
    # =============================================================================
    RATE_LIMIT_TYPE: str = os.getenv("RATE_LIMIT_TYPE", "fixed")
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "100"))
    IP_WHITELIST: List[str] = os.getenv("IP_WHITELIST", "127.0.0.1,::1").split(",")
    
    # =============================================================================
    # 数据导出配置
    # =============================================================================
    DEFAULT_EXPORT_FORMAT: str = os.getenv("DEFAULT_EXPORT_FORMAT", "json")
    EXPORT_DIR: str = os.getenv("EXPORT_DIR", "exports")
    EXPORT_RETENTION_DAYS: int = int(os.getenv("EXPORT_RETENTION_DAYS", "30"))
    MAX_EXPORT_SIZE: int = int(os.getenv("MAX_EXPORT_SIZE", "100"))
    
    # =============================================================================
    # 通知配置
    # =============================================================================
    ENABLE_EMAIL_NOTIFICATIONS: bool = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").lower() == "true"
    ENABLE_WEBHOOK_NOTIFICATIONS: bool = os.getenv("ENABLE_WEBHOOK_NOTIFICATIONS", "false").lower() == "true"
    NOTIFICATION_TEMPLATE_DIR: str = os.getenv("NOTIFICATION_TEMPLATE_DIR", "templates/notifications")
    NOTIFICATION_RETRY_ATTEMPTS: int = int(os.getenv("NOTIFICATION_RETRY_ATTEMPTS", "3"))
    NOTIFICATION_RETRY_DELAY: int = int(os.getenv("NOTIFICATION_RETRY_DELAY", "60"))
    
    def _validate_config(self):
        """验证配置"""
        errors = []
        warnings = []
        
        # =============================================================================
        # AI服务配置验证
        # =============================================================================
        if self.AI_SERVICE == "deepseek" and not self.DEEPSEEK_API_KEY:
            errors.append("使用DeepSeek服务时，DEEPSEEK_API_KEY不能为空")
        
        if self.AI_SERVICE == "siliconflow" and not self.SILICONFLOW_API_KEY:
            errors.append("使用硅基流动服务时，SILICONFLOW_API_KEY不能为空")
        
        if self.AI_SERVICE == "local" and not self.LOCAL_MODEL_PATH:
            errors.append("使用本地模型时，LOCAL_MODEL_PATH不能为空")
        
        if self.AI_SERVICE == "openai_compatible" and not self.OPENAI_COMPATIBLE_API_URL:
            errors.append("使用OpenAI兼容API时，OPENAI_COMPATIBLE_API_URL不能为空")
        
        if self.AI_SERVICE == "anthropic" and not self.ANTHROPIC_API_KEY:
            errors.append("使用Anthropic服务时，ANTHROPIC_API_KEY不能为空")
        
        if self.AI_SERVICE == "azure_openai" and not self.AZURE_OPENAI_API_KEY:
            errors.append("使用Azure OpenAI服务时，AZURE_OPENAI_API_KEY不能为空")
        
        if self.AI_SERVICE == "azure_openai" and not self.AZURE_OPENAI_ENDPOINT:
            errors.append("使用Azure OpenAI服务时，AZURE_OPENAI_ENDPOINT不能为空")
        
        # =============================================================================
        # 端口配置验证
        # =============================================================================
        if not (1 <= self.BACKEND_PORT <= 65535):
            errors.append(f"BACKEND_PORT必须在1-65535之间，当前值: {self.BACKEND_PORT}")
        
        if not (1 <= self.FRONTEND_PORT <= 65535):
            errors.append(f"FRONTEND_PORT必须在1-65535之间，当前值: {self.FRONTEND_PORT}")
        
        # =============================================================================
        # 安全配置验证
        # =============================================================================
        if self.SECRET_KEY == "dev-secret-key-change-this-in-production":
            warnings.append("SECRET_KEY使用默认值，生产环境请修改")
        
        if self.ENABLE_HTTPS and (not self.SSL_CERT_PATH or not self.SSL_KEY_PATH):
            errors.append("启用HTTPS时，SSL_CERT_PATH和SSL_KEY_PATH不能为空")
        
        # =============================================================================
        # 缓存配置验证
        # =============================================================================
        if self.CACHE_TYPE == "redis" and not self.REDIS_URL:
            warnings.append("使用Redis缓存时，建议设置REDIS_URL")
        
        # =============================================================================
        # 邮件配置验证
        # =============================================================================
        if self.ENABLE_EMAIL_NOTIFICATIONS and not self.SMTP_HOST:
            errors.append("启用邮件通知时，SMTP_HOST不能为空")
        
        # =============================================================================
        # 备份配置验证
        # =============================================================================
        if self.ENABLE_AUTO_BACKUP and not self.BACKUP_ENCRYPTION_KEY:
            warnings.append("启用自动备份时，建议设置BACKUP_ENCRYPTION_KEY")
        
        # =============================================================================
        # 输出验证结果
        # =============================================================================
        if errors:
            error_msg = "配置验证失败:\n" + "\n".join(f"  - {error}" for error in errors)
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        if warnings:
            warning_msg = "配置警告:\n" + "\n".join(f"  - {warning}" for warning in warnings)
            self.logger.warning(warning_msg)
    
    def get_ai_provider_config(self) -> dict:
        """获取AI提供者配置"""
        configs = {
            "deepseek": {
                "api_key": self.DEEPSEEK_API_KEY,
                "api_url": self.DEEPSEEK_API_URL,
                "model": self.DEEPSEEK_MODEL,
                "max_tokens": self.DEEPSEEK_MAX_TOKENS,
                "temperature": self.DEEPSEEK_TEMPERATURE
            },
            "siliconflow": {
                "api_key": self.SILICONFLOW_API_KEY,
                "api_url": self.SILICONFLOW_API_URL,
                "model": self.SILICONFLOW_MODEL,
                "max_tokens": self.SILICONFLOW_MAX_TOKENS,
                "temperature": self.SILICONFLOW_TEMPERATURE
            },
            "local": {
                "model_path": self.LOCAL_MODEL_PATH,
                "model_type": self.LOCAL_MODEL_TYPE,
                "device": self.LOCAL_MODEL_DEVICE,
                "max_length": self.LOCAL_MODEL_MAX_LENGTH,
                "temperature": self.LOCAL_MODEL_TEMPERATURE,
                "load_timeout": self.LOCAL_MODEL_LOAD_TIMEOUT
            },
            "openai_compatible": {
                "api_url": self.OPENAI_COMPATIBLE_API_URL,
                "api_key": self.OPENAI_COMPATIBLE_API_KEY,
                "model": self.OPENAI_COMPATIBLE_MODEL,
                "max_tokens": self.OPENAI_COMPATIBLE_MAX_TOKENS,
                "temperature": self.OPENAI_COMPATIBLE_TEMPERATURE
            },
            "anthropic": {
                "api_key": self.ANTHROPIC_API_KEY,
                "api_url": self.ANTHROPIC_API_URL,
                "model": self.ANTHROPIC_MODEL,
                "max_tokens": self.ANTHROPIC_MAX_TOKENS,
                "temperature": self.ANTHROPIC_TEMPERATURE
            },
            "azure_openai": {
                "api_key": self.AZURE_OPENAI_API_KEY,
                "endpoint": self.AZURE_OPENAI_ENDPOINT,
                "deployment_name": self.AZURE_OPENAI_DEPLOYMENT_NAME,
                "api_version": self.AZURE_OPENAI_API_VERSION,
                "model": self.AZURE_OPENAI_MODEL
            }
        }
        return configs.get(self.AI_SERVICE, {})
    
    def get_database_config(self) -> dict:
        """获取数据库配置"""
        return {
            "url": self.DATABASE_URL,
            "pool_size": self.DATABASE_POOL_SIZE,
            "timeout": self.DATABASE_TIMEOUT,
            "retry_attempts": self.DATABASE_RETRY_ATTEMPTS,
            "retry_delay": self.DATABASE_RETRY_DELAY,
            "pool_recycle": self.DB_POOL_RECYCLE
        }
    
    def get_server_config(self) -> dict:
        """获取服务器配置"""
        return {
            "host": self.BACKEND_HOST,
            "port": self.BACKEND_PORT,
            "frontend_port": self.FRONTEND_PORT,
            "worker_processes": self.WORKER_PROCESSES,
            "max_connections": self.MAX_CONNECTIONS,
            "request_timeout": self.REQUEST_TIMEOUT
        }
    
    def get_security_config(self) -> dict:
        """获取安全配置"""
        return {
            "secret_key": self.SECRET_KEY,
            "jwt_expiration_hours": self.JWT_EXPIRATION_HOURS,
            "jwt_refresh_hours": self.JWT_REFRESH_HOURS,
            "password_salt_rounds": self.PASSWORD_SALT_ROUNDS,
            "enable_https": self.ENABLE_HTTPS,
            "ssl_cert_path": self.SSL_CERT_PATH,
            "ssl_key_path": self.SSL_KEY_PATH,
            "session_timeout_minutes": self.SESSION_TIMEOUT_MINUTES,
            "max_login_attempts": self.MAX_LOGIN_ATTEMPTS,
            "login_lockout_minutes": self.LOGIN_LOCKOUT_MINUTES
        }
    
    def get_cache_config(self) -> dict:
        """获取缓存配置"""
        return {
            "enable_cache": self.ENABLE_CACHE,
            "cache_ttl": self.CACHE_TTL,
            "cache_max_entries": self.CACHE_MAX_ENTRIES,
            "cache_cleanup_interval": self.CACHE_CLEANUP_INTERVAL,
            "cache_type": self.CACHE_TYPE,
            "redis_url": self.REDIS_URL,
            "memcached_servers": self.MEMCACHED_SERVERS,
            "memory_cache_size": self.MEMORY_CACHE_SIZE
        }
    
    def get_email_config(self) -> dict:
        """获取邮件配置"""
        return {
            "smtp_host": self.SMTP_HOST,
            "smtp_port": self.SMTP_PORT,
            "smtp_username": self.SMTP_USERNAME,
            "smtp_password": self.SMTP_PASSWORD,
            "smtp_use_tls": self.SMTP_USE_TLS,
            "from_email": self.FROM_EMAIL,
            "smtp_timeout": self.SMTP_TIMEOUT,
            "smtp_retry_attempts": self.SMTP_RETRY_ATTEMPTS
        }
    
    def get_monitoring_config(self) -> dict:
        """获取监控配置"""
        return {
            "enable_monitoring": self.ENABLE_MONITORING,
            "monitoring_retention_days": self.MONITORING_RETENTION_DAYS,
            "enable_health_check": self.ENABLE_HEALTH_CHECK,
            "health_check_interval": self.HEALTH_CHECK_INTERVAL,
            "metrics_collection_interval": self.METRICS_COLLECTION_INTERVAL,
            "enable_apm": self.ENABLE_APM,
            "apm_server_url": self.APM_SERVER_URL
        }
    
    def get_backup_config(self) -> dict:
        """获取备份配置"""
        return {
            "enable_auto_backup": self.ENABLE_AUTO_BACKUP,
            "backup_dir": self.BACKUP_DIR,
            "backup_retention_days": self.BACKUP_RETENTION_DAYS,
            "backup_schedule": self.BACKUP_SCHEDULE,
            "backup_compression": self.BACKUP_COMPRESSION,
            "backup_encryption_key": self.BACKUP_ENCRYPTION_KEY
        }
    
    def get_oauth_config(self) -> dict:
        """获取OAuth配置"""
        return {
            "github_client_id": self.GITHUB_CLIENT_ID,
            "github_client_secret": self.GITHUB_CLIENT_SECRET,
            "google_client_id": self.GOOGLE_CLIENT_ID,
            "google_client_secret": self.GOOGLE_CLIENT_SECRET,
            "wechat_app_id": self.WECHAT_APP_ID,
            "wechat_app_secret": self.WECHAT_APP_SECRET
        }
    
    def get_feature_flags(self) -> dict:
        """获取功能开关配置"""
        return {
            "enable_auto_solve": self.ENABLE_AUTO_SOLVE,
            "enable_code_execution": self.ENABLE_CODE_EXECUTION,
            "enable_file_upload": self.ENABLE_FILE_UPLOAD,
            "enable_conversation": self.ENABLE_CONVERSATION,
            "enable_authentication": self.ENABLE_AUTHENTICATION,
            "enable_registration": self.ENABLE_REGISTRATION,
            "enable_rate_limiting": self.ENABLE_RATE_LIMITING,
            "enable_ip_whitelist": self.ENABLE_IP_WHITELIST
        }
    
    def is_production(self) -> bool:
        """判断是否为生产环境"""
        return not self.DEBUG and self.PRODUCTION_DOMAIN != "yourdomain.com"
    
    def is_development(self) -> bool:
        """判断是否为开发环境"""
        return self.DEBUG or self.PRODUCTION_DOMAIN == "yourdomain.com"
    
    def __str__(self):
        """配置信息字符串表示"""
        return f"Config(AI_SERVICE={self.AI_SERVICE}, DEBUG={self.DEBUG}, PORT={self.BACKEND_PORT})"

# 创建全局配置实例
config = Config() 