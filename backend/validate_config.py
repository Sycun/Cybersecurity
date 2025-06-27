#!/usr/bin/env python3
"""
CTF智能分析平台配置验证脚本
用于验证环境变量配置是否正确
"""

import os
import sys
from dotenv import load_dotenv
from typing import List, Dict, Any

# 加载环境变量
load_dotenv()

class ConfigValidator:
    """配置验证器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
    
    def add_error(self, message: str):
        """添加错误信息"""
        self.errors.append(message)
    
    def add_warning(self, message: str):
        """添加警告信息"""
        self.warnings.append(message)
    
    def add_info(self, message: str):
        """添加信息"""
        self.info.append(message)
    
    def validate_ai_service_config(self):
        """验证AI服务配置"""
        ai_service = os.getenv("AI_SERVICE", "deepseek")
        self.add_info(f"当前AI服务: {ai_service}")
        
        if ai_service == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                self.add_error("使用DeepSeek服务时，DEEPSEEK_API_KEY不能为空")
            elif api_key == "your_deepseek_api_key_here":
                self.add_error("请设置有效的DEEPSEEK_API_KEY")
            else:
                self.add_info("DeepSeek API密钥已配置")
        
        elif ai_service == "siliconflow":
            api_key = os.getenv("SILICONFLOW_API_KEY")
            if not api_key:
                self.add_error("使用硅基流动服务时，SILICONFLOW_API_KEY不能为空")
            elif api_key == "your_siliconflow_api_key_here":
                self.add_error("请设置有效的SILICONFLOW_API_KEY")
            else:
                self.add_info("硅基流动API密钥已配置")
        
        elif ai_service == "local":
            model_path = os.getenv("LOCAL_MODEL_PATH")
            if not model_path:
                self.add_error("使用本地模型时，LOCAL_MODEL_PATH不能为空")
            elif model_path == "/path/to/local/model":
                self.add_error("请设置有效的LOCAL_MODEL_PATH")
            else:
                self.add_info(f"本地模型路径: {model_path}")
        
        elif ai_service == "openai_compatible":
            api_url = os.getenv("OPENAI_COMPATIBLE_API_URL")
            if not api_url:
                self.add_error("使用OpenAI兼容API时，OPENAI_COMPATIBLE_API_URL不能为空")
            elif api_url == "http://localhost:8000/v1/chat/completions":
                self.add_warning("OpenAI兼容API URL使用默认值，请确认是否正确")
            else:
                self.add_info(f"OpenAI兼容API URL: {api_url}")
        
        else:
            self.add_error(f"不支持的AI服务类型: {ai_service}")
    
    def validate_server_config(self):
        """验证服务器配置"""
        backend_port = int(os.getenv("BACKEND_PORT", "8000"))
        frontend_port = int(os.getenv("FRONTEND_PORT", "3000"))
        
        if not (1 <= backend_port <= 65535):
            self.add_error(f"BACKEND_PORT必须在1-65535之间，当前值: {backend_port}")
        else:
            self.add_info(f"后端端口: {backend_port}")
        
        if not (1 <= frontend_port <= 65535):
            self.add_error(f"FRONTEND_PORT必须在1-65535之间，当前值: {frontend_port}")
        else:
            self.add_info(f"前端端口: {frontend_port}")
        
        if backend_port == frontend_port:
            self.add_error("后端端口和前端端口不能相同")
    
    def validate_security_config(self):
        """验证安全配置"""
        secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-this-in-production")
        debug = os.getenv("DEBUG", "false").lower() == "true"
        
        if secret_key == "dev-secret-key-change-this-in-production" and not debug:
            self.add_warning("生产环境中应更改SECRET_KEY")
        
        if len(secret_key) < 32:
            self.add_warning("SECRET_KEY长度建议至少32位")
        
        # 检查HTTPS配置
        enable_https = os.getenv("ENABLE_HTTPS", "false").lower() == "true"
        if enable_https:
            ssl_cert = os.getenv("SSL_CERT_PATH")
            ssl_key = os.getenv("SSL_KEY_PATH")
            if not ssl_cert or not ssl_key:
                self.add_error("启用HTTPS时必须提供SSL证书路径")
    
    def validate_database_config(self):
        """验证数据库配置"""
        database_url = os.getenv("DATABASE_URL", "sqlite:///./ctf_analyzer.db")
        self.add_info(f"数据库URL: {database_url}")
        
        # 检查数据库连接池配置
        pool_size = int(os.getenv("DATABASE_POOL_SIZE", "10"))
        if pool_size < 1 or pool_size > 100:
            self.add_warning(f"数据库连接池大小建议在1-100之间，当前值: {pool_size}")
    
    def validate_performance_config(self):
        """验证性能配置"""
        max_file_size = int(os.getenv("MAX_FILE_SIZE", "10485760"))
        request_timeout = int(os.getenv("REQUEST_TIMEOUT", "60"))
        
        if max_file_size > 100 * 1024 * 1024:  # 100MB
            self.add_warning(f"最大文件大小设置较大: {max_file_size} 字节")
        
        if request_timeout > 300:  # 5分钟
            self.add_warning(f"请求超时时间设置较长: {request_timeout} 秒")
    
    def validate_cache_config(self):
        """验证缓存配置"""
        enable_cache = os.getenv("ENABLE_CACHE", "true").lower() == "true"
        cache_ttl = int(os.getenv("CACHE_TTL", "3600"))
        
        if enable_cache:
            self.add_info("缓存已启用")
            if cache_ttl < 60:
                self.add_warning(f"缓存TTL设置较短: {cache_ttl} 秒")
        else:
            self.add_info("缓存已禁用")
    
    def validate_email_config(self):
        """验证邮件配置"""
        smtp_host = os.getenv("SMTP_HOST")
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        if smtp_host and not smtp_username:
            self.add_warning("配置了SMTP_HOST但未配置SMTP_USERNAME")
        
        if smtp_host and not smtp_password:
            self.add_warning("配置了SMTP_HOST但未配置SMTP_PASSWORD")
        
        if smtp_host and smtp_username and smtp_password:
            self.add_info("邮件服务配置完整")
    
    def validate_oauth_config(self):
        """验证OAuth配置"""
        github_client_id = os.getenv("GITHUB_CLIENT_ID")
        github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        
        if github_client_id and not github_client_secret:
            self.add_warning("配置了GITHUB_CLIENT_ID但未配置GITHUB_CLIENT_SECRET")
        
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        if google_client_id and not google_client_secret:
            self.add_warning("配置了GOOGLE_CLIENT_ID但未配置GOOGLE_CLIENT_SECRET")
    
    def validate_environment(self):
        """验证环境配置"""
        debug = os.getenv("DEBUG", "false").lower() == "true"
        log_level = os.getenv("LOG_LEVEL", "INFO")
        
        if debug:
            self.add_info("调试模式已启用")
        else:
            self.add_info("生产模式")
        
        self.add_info(f"日志级别: {log_level}")
    
    def validate_all(self) -> bool:
        """验证所有配置"""
        print("=" * 60)
        print("CTF智能分析平台配置验证")
        print("=" * 60)
        
        self.validate_ai_service_config()
        self.validate_server_config()
        self.validate_security_config()
        self.validate_database_config()
        self.validate_performance_config()
        self.validate_cache_config()
        self.validate_email_config()
        self.validate_oauth_config()
        self.validate_environment()
        
        # 输出结果
        print("\n验证结果:")
        print("-" * 60)
        
        if self.info:
            print("\n✅ 信息:")
            for info in self.info:
                print(f"  • {info}")
        
        if self.warnings:
            print("\n⚠️  警告:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.errors:
            print("\n❌ 错误:")
            for error in self.errors:
                print(f"  • {error}")
        
        print("-" * 60)
        
        if self.errors:
            print(f"\n❌ 配置验证失败，发现 {len(self.errors)} 个错误")
            return False
        elif self.warnings:
            print(f"\n⚠️  配置验证通过，但有 {len(self.warnings)} 个警告")
            return True
        else:
            print(f"\n✅ 配置验证通过，所有配置正确")
            return True

def main():
    """主函数"""
    validator = ConfigValidator()
    success = validator.validate_all()
    
    if not success:
        print("\n请修复上述错误后重新验证")
        sys.exit(1)
    else:
        print("\n配置验证完成，可以启动服务")
        sys.exit(0)

if __name__ == "__main__":
    main() 