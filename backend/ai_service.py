import os
from typing import Dict, Any
from dotenv import load_dotenv
from ai_providers import AIProviderFactory, AIProvider

load_dotenv()

class AIService:
    """AI服务管理类"""
    
    def __init__(self, provider_type: str = None):
        """
        初始化AI服务
        
        Args:
            provider_type: AI提供者类型，如果为None则使用环境变量AI_SERVICE的值
        """
        self.provider_type = provider_type or os.getenv("AI_SERVICE", "deepseek")
        self.provider: AIProvider = AIProviderFactory.create_provider(self.provider_type)
    
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
            return await self.provider.analyze_challenge(description, question_type)
        except Exception as e:
            error_msg = f"AI服务异常: {str(e)}"
            print(error_msg)
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
        # 这个方法保持原有逻辑，或者可以扩展为AI驱动的工具推荐
        try:
            return {"tools": [], "commands": []}
        except Exception as e:
            print(f"工具推荐失败: {str(e)}")
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
            self.provider = new_provider
            self.provider_type = provider_type
            return True
        except Exception as e:
            print(f"切换AI提供者失败: {str(e)}")
            return False
    
    @staticmethod
    def get_available_providers() -> Dict[str, str]:
        """
        获取所有可用的AI提供者
        
        Returns:
            可用提供者字典
        """
        return AIProviderFactory.get_available_providers() 