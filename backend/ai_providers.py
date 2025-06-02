import httpx
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any
from dotenv import load_dotenv

# 添加本地模型支持的导入
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    torch = None
    AutoModelForCausalLM = None
    AutoTokenizer = None

load_dotenv()

class AIProvider(ABC):
    """AI提供者基础接口"""
    
    @abstractmethod
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        """分析CTF题目"""
        pass
    
    @abstractmethod
    def get_prompt_template(self, question_type: str) -> str:
        """获取提示词模板"""
        pass

class DeepSeekProvider(AIProvider):
    """DeepSeek AI提供者"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY环境变量未设置")
    
    def get_prompt_template(self, question_type: str) -> str:
        """获取DeepSeek的提示词模板"""
        templates = {
            "web": """你是一个专业的Web安全专家和CTF选手。请分析以下Web CTF题目：

题目描述：
{description}

请按照以下格式提供详细分析：

## 题目类型识别
- 主要漏洞类型：
- 可能涉及的技术：

## 分析思路
1. 初步分析步骤
2. 关键检查点
3. 可能的攻击向量

## 解题步骤
1. 详细的操作步骤
2. 需要使用的工具
3. 关键的payload或命令

## 常见陷阱
- 需要注意的问题
- 可能的绕过技巧

## 相关知识点
- 涉及的安全概念
- 推荐学习资源

请提供专业、详细且实用的分析。""",

            "pwn": """你是一个专业的二进制安全专家和CTF选手。请分析以下Pwn CTF题目：

题目描述：
{description}

请按照以下格式提供详细分析：

## 二进制分析
- 架构和保护机制：
- 可能的漏洞类型：

## 漏洞分析
1. 漏洞定位方法
2. 漏洞利用原理
3. 利用条件分析

## 利用思路
1. 信息泄露方法
2. 控制流劫持
3. ROP/JOP链构造
4. Shellcode编写

## 利用代码
```python
# 提供完整的exploit代码框架
```

## 调试技巧
- GDB调试命令
- 内存布局分析
- 动态调试方法

## 相关工具
- 推荐使用的工具
- 工具使用方法

请提供专业的二进制漏洞分析和利用方案。""",

            "reverse": """你是一个专业的逆向工程专家和CTF选手。请分析以下Reverse CTF题目：

题目描述：
{description}

请按照以下格式提供详细分析：

## 文件分析
- 文件类型和架构：
- 加壳/混淆检测：
- 关键字符串分析：

## 逆向分析策略
1. 静态分析方法
2. 动态分析方法
3. 关键函数定位

## 算法分析
1. 加密/编码算法识别
2. 算法逆向方法
3. 密钥/种子提取

## 解题步骤
1. 详细的分析流程
2. 关键代码片段
3. 算法还原过程

## 工具使用
- IDA Pro/Ghidra使用技巧
- 动态调试方法
- 脚本编写建议

## 解密/解码
```python
# 提供解密脚本
```

请提供专业的逆向工程分析方案。""",

            "crypto": """你是一个专业的密码学专家和CTF选手。请分析以下Crypto CTF题目：

题目描述：
{description}

请按照以下格式提供详细分析：

## 密码学分析
- 加密算法识别：
- 密钥长度和类型：
- 可能的攻击方向：

## 漏洞分析
1. 算法实现缺陷
2. 密钥管理问题
3. 随机数生成问题
4. 侧信道攻击可能性

## 攻击策略
1. 数学攻击方法
2. 暴力破解可行性
3. 已知明文攻击
4. 频率分析等统计方法

## 解题步骤
1. 详细的分析过程
2. 数学计算方法
3. 编程实现思路

## 解密代码
```python
# 提供完整的解密脚本
```

## 相关工具
- SageMath使用
- 在线工具推荐
- 专业密码学库

请提供专业的密码学分析和攻击方案。""",

            "misc": """你是一个全能的CTF专家。请分析以下Misc CTF题目：

题目描述：
{description}

请按照以下格式提供详细分析：

## 题目类型判断
- 可能的题目类型：
- 涉及的技术领域：

## 分析方向
1. 隐写术分析
2. 编码解码
3. 取证分析
4. 协议分析
5. 其他可能方向

## 解题思路
1. 初步信息收集
2. 工具选择和使用
3. 数据提取方法
4. 信息还原过程

## 详细步骤
1. 具体操作命令
2. 工具使用方法
3. 脚本编写建议

## 常用工具
- 文件分析工具
- 隐写术工具
- 编码解码工具
- 取证分析工具

## 解题脚本
```python
# 提供相关的处理脚本
```

请提供全面的Misc题目分析方案。""",

            "unknown": """你是一个经验丰富的CTF专家。请分析以下CTF题目：

题目描述：
{description}

请按照以下格式提供分析：

## 题目类型推测
根据题目描述，推测可能的题目类型：
- Web安全
- 二进制漏洞(Pwn)
- 逆向工程(Reverse)
- 密码学(Crypto)
- 杂项(Misc)

## 初步分析
1. 关键信息提取
2. 可能的解题方向
3. 需要的技能和工具

## 建议步骤
1. 信息收集方法
2. 初步尝试方向
3. 深入分析策略

## 工具推荐
根据可能的题目类型推荐相应工具

请提供专业的CTF题目分析。"""
        }
        return templates.get(question_type, templates["unknown"])
    
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        """调用DeepSeek API分析CTF题目"""
        try:
            template = self.get_prompt_template(question_type)
            prompt = template.format(description=description)
            
            request_data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的CTF专家，具有丰富的网络安全知识和实战经验。请提供详细、专业且实用的分析。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000,
                "stream": False
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
                    error_msg = f"DeepSeek API调用失败: {response.status_code} - {response.text}"
                    print(error_msg)
                    return f"AI分析暂时不可用，请稍后重试。错误信息: {error_msg}"
                    
        except Exception as e:
            error_msg = f"DeepSeek AI服务异常: {str(e)}"
            print(error_msg)
            return f"AI分析遇到问题，请检查网络连接或稍后重试。错误信息: {error_msg}"

class SiliconFlowProvider(AIProvider):
    """硅基流动 AI提供者"""
    
    def __init__(self):
        self.api_key = os.getenv("SILICONFLOW_API_KEY")
        self.api_url = os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.cn/v1/chat/completions")
        self.model = os.getenv("SILICONFLOW_MODEL", "Qwen/QwQ-32B")
        
        if not self.api_key:
            raise ValueError("SILICONFLOW_API_KEY环境变量未设置")
    
    def get_prompt_template(self, question_type: str) -> str:
        """获取硅基流动的提示词模板（与DeepSeek相同的模板）"""
        # 复用DeepSeek的模板，因为都是中文CTF分析
        deepseek_provider = DeepSeekProvider.__new__(DeepSeekProvider)
        return deepseek_provider.get_prompt_template(question_type)
    
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        """调用硅基流动API分析CTF题目"""
        try:
            template = self.get_prompt_template(question_type)
            prompt = template.format(description=description)
            
            # 根据硅基流动API文档构造请求
            request_data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的CTF专家，具有丰富的网络安全知识和实战经验。请提供详细、专业且实用的分析。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "max_tokens": 4000,
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {
                    "type": "text"
                }
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
            
            # 加载分词器
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path, 
                trust_remote_code=True,
                padding_side="left"
            )
            
            # 设置pad_token（如果没有的话）
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # 设备配置
            if self.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # 加载模型
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
        """获取本地模型的提示词模板"""
        # 使用优化后的提示词模板，适合本地模型
        templates = {
            "web": """作为CTF Web安全专家，分析以下题目：

题目描述：{description}

请提供：
1. 漏洞类型识别
2. 攻击思路分析
3. 具体解题步骤
4. 工具推荐
5. 注意事项

分析：""",

            "pwn": """作为CTF二进制安全专家，分析以下题目：

题目描述：{description}

请提供：
1. 二进制保护机制分析
2. 漏洞利用思路
3. ROP/Shellcode构造
4. 调试方法
5. 工具推荐

分析：""",

            "reverse": """作为CTF逆向工程专家，分析以下题目：

题目描述：{description}

请提供：
1. 文件格式分析
2. 逆向分析策略
3. 关键算法识别
4. 解密方法
5. 工具推荐

分析：""",

            "crypto": """作为CTF密码学专家，分析以下题目：

题目描述：{description}

请提供：
1. 加密算法识别
2. 攻击方法分析
3. 数学原理解释
4. 解密步骤
5. 工具推荐

分析：""",

            "misc": """作为CTF综合题专家，分析以下题目：

题目描述：{description}

请提供：
1. 题目类型判断
2. 分析方向指导
3. 工具使用建议
4. 解题步骤
5. 相关技术点

分析：""",

            "unknown": """作为CTF专家，分析以下题目：

题目描述：{description}

请从以下方面分析：
1. 题目类型推测（Web/Pwn/Reverse/Crypto/Misc）
2. 关键信息提取
3. 可能的解题方向
4. 推荐工具和方法

分析："""
        }
        return templates.get(question_type, templates["unknown"])
    
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        """使用本地模型分析CTF题目"""
        try:
            template = self.get_prompt_template(question_type)
            prompt = template.format(description=description)
            
            # 编码输入
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                truncation=True, 
                max_length=2048,
                padding=True
            )
            
            # 移动到正确的设备
            if self.device == "cuda":
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # 生成响应
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
            
            # 解码响应，只保留新生成的部分
            input_length = len(inputs["input_ids"][0])
            generated_tokens = outputs[0][input_length:]
            response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            # 清理响应
            response = response.strip()
            if not response:
                response = "抱歉，本地模型未能生成有效分析结果，请检查模型配置或尝试其他AI提供者。"
            
            return response
            
        except Exception as e:
            error_msg = f"本地AI模型分析异常: {str(e)}"
            print(error_msg)
            return f"本地模型分析遇到问题，请检查模型配置或稍后重试。错误信息: {error_msg}"

class OpenAICompatibleProvider(AIProvider):
    """OpenAI兼容API提供者（支持本地部署的OpenAI兼容服务）"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY", "sk-no-key-required")
        self.api_url = os.getenv("OPENAI_COMPATIBLE_API_URL")
        self.model = os.getenv("OPENAI_COMPATIBLE_MODEL", "gpt-3.5-turbo")
        
        if not self.api_url:
            raise ValueError("OPENAI_COMPATIBLE_API_URL环境变量未设置")
    
    def get_prompt_template(self, question_type: str) -> str:
        """获取OpenAI兼容API的提示词模板"""
        # 复用DeepSeek的模板
        deepseek_provider = DeepSeekProvider.__new__(DeepSeekProvider)
        return deepseek_provider.get_prompt_template(question_type)
    
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        """调用OpenAI兼容API分析CTF题目"""
        try:
            template = self.get_prompt_template(question_type)
            prompt = template.format(description=description)
            
            request_data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的CTF专家，具有丰富的网络安全知识和实战经验。请提供详细、专业且实用的分析。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000,
                "stream": False
            }
            
            # 构建headers
            headers = {
                "Content-Type": "application/json"
            }
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

class AIProviderFactory:
    """AI提供者工厂类"""
    
    @staticmethod
    def create_provider(provider_type: str = None) -> AIProvider:
        """创建AI提供者实例"""
        if provider_type is None:
            provider_type = os.getenv("AI_SERVICE", "deepseek")
        
        if provider_type.lower() == "deepseek":
            return DeepSeekProvider()
        elif provider_type.lower() == "siliconflow":
            return SiliconFlowProvider()
        elif provider_type.lower() == "local":
            return LocalAIProvider()
        elif provider_type.lower() == "openai_compatible":
            return OpenAICompatibleProvider()
        else:
            raise ValueError(f"不支持的AI服务类型: {provider_type}")
    
    @staticmethod
    def get_available_providers() -> Dict[str, str]:
        """获取可用的AI提供者列表"""
        providers = {
            "deepseek": "DeepSeek",
            "siliconflow": "硅基流动",
            "openai_compatible": "OpenAI兼容API"
        }
        
        # 检查本地模型支持
        if TRANSFORMERS_AVAILABLE:
            providers["local"] = "本地模型"
        
        return providers 