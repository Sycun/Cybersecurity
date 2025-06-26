import os
from logger import get_logger
from .deepseek import AIProvider

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    torch = None
    AutoModelForCausalLM = None
    AutoTokenizer = None

class LocalAIProvider(AIProvider):
    """本地AI模型提供者"""
    def __init__(self):
        if not TRANSFORMERS_AVAILABLE:
            raise ValueError("本地模型支持需要安装 transformers 和 torch。请运行: pip install torch transformers")
        self.model_path = os.getenv("LOCAL_MODEL_PATH")
        self.model_type = os.getenv("LOCAL_MODEL_TYPE", "auto")
        self.device = os.getenv("LOCAL_MODEL_DEVICE", "auto")
        self.max_length = int(os.getenv("LOCAL_MODEL_MAX_LENGTH", "4096"))
        self.temperature = float(os.getenv("LOCAL_MODEL_TEMPERATURE", "0.7"))
        if not self.model_path:
            raise ValueError("LOCAL_MODEL_PATH环境变量未设置")
        try:
            print(f"正在加载本地模型: {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path, trust_remote_code=True, padding_side="left"
            )
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            if self.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            print(f"✅ 本地模型加载成功，设备: {self.device}")
        except Exception as e:
            raise ValueError(f"本地模型加载失败: {str(e)}")
    def get_prompt_template(self, question_type: str) -> str:
        templates = {
            # ...（保留原有模板内容，略）...
        }
        return templates.get(question_type, templates["unknown"])
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        try:
            template = self.get_prompt_template(question_type)
            prompt = template.format(description=description)
            inputs = self.tokenizer(
                prompt, return_tensors="pt", truncation=True, max_length=2048, padding=True
            )
            if self.device == "cuda":
                inputs = {k: v.cuda() for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=2048,
                    min_length=len(inputs["input_ids"][0]) + 50,
                    temperature=self.temperature,
                    top_p=0.9,
                    top_k=50,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )
            input_length = len(inputs["input_ids"][0])
            generated_tokens = outputs[0][input_length:]
            response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            response = response.strip()
            if not response:
                response = "抱歉，本地模型未能生成有效分析结果，请检查模型配置或尝试其他AI提供者。"
            return response
        except Exception as e:
            error_msg = f"本地AI模型分析异常: {str(e)}"
            print(error_msg)
            return f"本地模型分析遇到问题，请检查模型配置或稍后重试。错误信息: {error_msg}" 