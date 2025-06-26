from .deepseek import DeepSeekProvider, AIProvider
from .siliconflow import SiliconFlowProvider
from .local import LocalAIProvider
from .openai_compatible import OpenAICompatibleProvider

class AIProviderFactory:
    @staticmethod
    def create_provider(provider_type: str = None) -> AIProvider:
        if provider_type is None:
            import os
            provider_type = os.getenv("AI_SERVICE", "deepseek")
        provider_type = provider_type.lower()
        if provider_type == "deepseek":
            return DeepSeekProvider()
        elif provider_type == "siliconflow":
            return SiliconFlowProvider()
        elif provider_type == "local":
            return LocalAIProvider()
        elif provider_type == "openai_compatible":
            return OpenAICompatibleProvider()
        else:
            raise ValueError(f"不支持的AI服务类型: {provider_type}") 