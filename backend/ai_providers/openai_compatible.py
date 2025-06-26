import os
import httpx
from logger import get_logger
from .deepseek import DeepSeekProvider, AIProvider

class OpenAICompatibleProvider(AIProvider):
    """OpenAI兼容API提供者（支持本地部署的OpenAI兼容服务）"""
    def __init__(self):
        self.api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY", "sk-no-key-required")
        self.api_url = os.getenv("OPENAI_COMPATIBLE_API_URL")
        self.model = os.getenv("OPENAI_COMPATIBLE_MODEL", "gpt-3.5-turbo")
        if not self.api_url:
            raise ValueError("OPENAI_COMPATIBLE_API_URL环境变量未设置")
    def get_prompt_template(self, question_type: str) -> str:
        deepseek_provider = DeepSeekProvider.__new__(DeepSeekProvider)
        return deepseek_provider.get_prompt_template(question_type)
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        try:
            template = self.get_prompt_template(question_type)
            prompt = template.format(description=description)
            request_data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "你是一个专业的CTF专家，具有丰富的网络安全知识和实战经验。请提供详细、专业且实用的分析。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 4000,
                "stream": False
            }
            headers = {"Content-Type": "application/json"}
            if self.api_key != "sk-no-key-required":
                headers["Authorization"] = f"Bearer {self.api_key}"
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=request_data
                )
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    error_msg = f"OpenAI兼容API调用失败: {response.status_code} - {response.text}"
                    print(error_msg)
                    return f"AI分析暂时不可用，请稍后重试。错误信息: {error_msg}"
        except Exception as e:
            error_msg = f"OpenAI兼容API服务异常: {str(e)}"
            print(error_msg)
            return f"AI分析遇到问题，请检查网络连接或稍后重试。错误信息: {error_msg}" 