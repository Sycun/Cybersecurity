import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional

def setup_logger(
    name: str = "ctf_analyzer",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    max_bytes: int = 10*1024*1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    设置统一的日志记录器
    
    Args:
        name: 日志器名称
        level: 日志级别
        log_file: 日志文件路径
        max_bytes: 单个日志文件最大大小
        backup_count: 备份文件数量
    
    Returns:
        配置好的日志器
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # 日志格式
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定了日志文件）
    if log_file:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
    
    return logger

# 创建默认日志器
default_logger = setup_logger(
    log_file=os.getenv("LOG_FILE", "logs/app.log")
)

# 便捷函数
def get_logger(name: str = None) -> logging.Logger:
    """获取日志器"""
    if name:
        return logging.getLogger(name)
    return default_logger

def log_ai_request(provider: str, request_data: dict, response_time: float):
    """记录AI请求日志"""
    logger = get_logger("ai_requests")
    logger.info(f"Provider: {provider}, Response Time: {response_time:.2f}s, Request: {str(request_data)[:200]}...")

def log_error(error: Exception, context: str = ""):
    """记录错误日志"""
    logger = get_logger("errors")
    logger.error(f"Error in {context}: {str(error)}", exc_info=True) 