import os
from typing import Dict, Any
from dotenv import load_dotenv
from ai_providers import AIProviderFactory, AIProvider
from cache import ai_response_cache
from config import config
from logger import get_logger

load_dotenv()

class AIService:
    """AI服务管理类"""
    
    def __init__(self, provider_type: str = None):
        """
        初始化AI服务
        
        Args:
            provider_type: AI提供者类型，如果为None则使用环境变量AI_SERVICE的值
        """
        self.provider_type = provider_type or config.AI_SERVICE
        self.provider: AIProvider = AIProviderFactory.create_provider(self.provider_type)
        self.logger = get_logger("ai_service")
        self.logger.info(f"AI服务初始化，使用提供者: {self.provider_type}")
    
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        """
        分析CTF题目
        
        Args:
            description: 题目描述
            question_type: 题目类型
            
        Returns:
            AI分析结果
        """
        try:
            # 尝试从缓存获取结果
            cached_response = ai_response_cache.get_cached_response(
                description, question_type, self.provider_type
            )
            
            if cached_response:
                self.logger.info(f"使用缓存响应，题目类型: {question_type}")
                return cached_response
            
            # 缓存未命中，调用AI提供者
            self.logger.info(f"调用AI提供者分析，类型: {question_type}, 提供者: {self.provider_type}")
            response = await self.provider.analyze_challenge(description, question_type)
            
            # 缓存响应
            ai_response_cache.cache_response(description, question_type, self.provider_type, response)
            
            return response
            
        except Exception as e:
            error_msg = f"AI服务异常: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return f"AI分析遇到问题，请检查配置或稍后重试。错误信息: {error_msg}"
    
    async def get_tool_recommendation(self, question_type: str, description: str) -> Dict[str, Any]:
        """
        根据题目类型和描述推荐工具
        
        Args:
            question_type: 题目类型
            description: 题目描述
            
        Returns:
            工具推荐信息
        """
        try:
            # 这个方法保持原有逻辑，可以后续扩展为AI驱动的工具推荐
            return {"tools": [], "commands": []}
        except Exception as e:
            self.logger.error(f"工具推荐失败: {str(e)}")
            return {"tools": [], "commands": []}
    
    def get_provider_info(self) -> Dict[str, str]:
        """
        获取当前AI提供者信息
        
        Returns:
            提供者信息字典
        """
        available_providers = AIProviderFactory.get_available_providers()
        return {
            "current_provider": self.provider_type,
            "current_provider_name": available_providers.get(self.provider_type, "未知"),
            "available_providers": available_providers
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        获取性能统计信息
        
        Returns:
            性能统计字典
        """
        provider_stats = self.provider.get_performance_stats()
        cache_stats = ai_response_cache.get_cache_stats()
        
        return {
            "provider": self.provider_type,
            "provider_stats": provider_stats,
            "cache_stats": cache_stats
        }
    
    def switch_provider(self, provider_type: str) -> bool:
        """
        切换AI提供者
        
        Args:
            provider_type: 新的提供者类型
            
        Returns:
            切换是否成功
        """
        try:
            new_provider = AIProviderFactory.create_provider(provider_type)
            old_provider = self.provider_type
            
            self.provider = new_provider
            self.provider_type = provider_type
            
            # 清理旧提供者的缓存
            ai_response_cache.invalidate_provider_cache(old_provider)
            
            self.logger.info(f"AI提供者切换成功: {old_provider} -> {provider_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"切换AI提供者失败: {str(e)}")
            return False
    
    def clear_cache(self):
        """清空缓存"""
        ai_response_cache.cache.clear()
        self.logger.info("AI响应缓存已清空")
    
    @staticmethod
    def get_available_providers() -> Dict[str, str]:
        """
        获取所有可用的AI提供者
        
        Returns:
            可用提供者字典
        """
        return AIProviderFactory.get_available_providers() 