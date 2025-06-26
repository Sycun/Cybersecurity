import os
import time
import httpx
from typing import Dict, Any
from logger import get_logger, log_ai_request, log_error
from abc import ABC, abstractmethod

class AIProvider(ABC):
    def __init__(self):
        self.logger = get_logger(f"ai_provider_{self.__class__.__name__}")
        self.request_count = 0
        self.total_response_time = 0.0

    @abstractmethod
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        pass

    @abstractmethod
    def get_prompt_template(self, question_type: str) -> str:
        pass

    def get_performance_stats(self) -> Dict[str, Any]:
        avg_response_time = self.total_response_time / self.request_count if self.request_count > 0 else 0
        return {
            "request_count": self.request_count,
            "total_response_time": self.total_response_time,
            "average_response_time": avg_response_time
        }

class DeepSeekProvider(AIProvider):
    """DeepSeek AI提供者"""
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY环境变量未设置")
        self.logger.info("DeepSeek提供者初始化成功")

    def get_prompt_template(self, question_type: str) -> str:
        templates = {
            # ...（保留原有模板内容，略）...
        }
        return templates.get(question_type, templates["unknown"])

    def get_code_generation_template(self, question_type: str) -> str:
        templates = {
            # ...（保留原有模板内容，略）...
        }
        return templates.get(question_type, templates["unknown"])

    async def analyze_challenge(self, description: str, question_type: str) -> str:
        try:
            start_time = time.time()
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
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            log_ai_request("deepseek", request_data)
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=request_data
                )
                response_time = time.time() - start_time
                self.request_count += 1
                self.total_response_time += response_time
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    self.logger.info(f"DeepSeek分析完成，响应时间: {response_time:.2f}s")
                    return ai_response
                else:
                    error_msg = f"DeepSeek API调用失败: {response.status_code} - {response.text}"
                    log_error("deepseek_api_error", error_msg)
                    return f"AI分析暂时不可用，请稍后重试。错误信息: {error_msg}"
        except Exception as e:
            error_msg = f"DeepSeek API服务异常: {str(e)}"
            log_error("deepseek_service_error", error_msg, exc_info=True)
            return f"AI分析遇到问题，请检查网络连接或稍后重试。错误信息: {error_msg}" 