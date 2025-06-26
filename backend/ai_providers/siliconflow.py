import os
import httpx
from logger import get_logger
from .deepseek import DeepSeekProvider, AIProvider

class SiliconFlowProvider(AIProvider):
    """硅基流动 AI提供者"""
    def __init__(self):
        self.api_key = os.getenv("SILICONFLOW_API_KEY")
        self.api_url = os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.cn/v1/chat/completions")
        self.model = os.getenv("SILICONFLOW_MODEL", "Qwen/QwQ-32B")
        if not self.api_key:
            raise ValueError("SILICONFLOW_API_KEY环境变量未设置")

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
                "stream": False,
                "max_tokens": 4000,
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {"type": "text"}
            }
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=request_data
                )
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    error_msg = f"硅基流动API调用失败: {response.status_code} - {response.text}"
                    print(error_msg)
                    return f"AI分析暂时不可用，请稍后重试。错误信息: {error_msg}"
        except Exception as e:
            error_msg = f"硅基流动AI服务异常: {str(e)}"
            print(error_msg)
            return f"AI分析遇到问题，请检查网络连接或稍后重试。错误信息: {error_msg}" 