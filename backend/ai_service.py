import httpx
import json
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """DeepSeek AI服务类"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY环境变量未设置")
    
    # CTF题目类型对应的专业提示词模板
    PROMPT_TEMPLATES = {
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
    
    async def analyze_challenge(self, description: str, question_type: str) -> str:
        """调用DeepSeek API分析CTF题目"""
        try:
            # 选择合适的提示词模板
            template = self.PROMPT_TEMPLATES.get(question_type, self.PROMPT_TEMPLATES["unknown"])
            prompt = template.format(description=description)
            
            # 构造请求数据
            request_data = {
                "model": "deepseek-chat",
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
            
            # 发送请求
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
                    error_msg = f"API调用失败: {response.status_code} - {response.text}"
                    print(error_msg)
                    return f"AI分析暂时不可用，请稍后重试。错误信息: {error_msg}"
                    
        except Exception as e:
            error_msg = f"AI服务异常: {str(e)}"
            print(error_msg)
            return f"AI分析遇到问题，请检查网络连接或稍后重试。错误信息: {error_msg}"
    
    async def get_tool_recommendation(self, question_type: str, description: str) -> Dict[str, Any]:
        """根据题目类型和描述推荐工具"""
        tool_prompts = {
            "web": f"基于以下Web CTF题目，推荐最适合的工具和命令：\n{description}",
            "pwn": f"基于以下Pwn题目，推荐最适合的调试和利用工具：\n{description}",
            "reverse": f"基于以下逆向题目，推荐最适合的分析工具：\n{description}",
            "crypto": f"基于以下密码学题目，推荐最适合的分析工具：\n{description}",
            "misc": f"基于以下Misc题目，推荐最适合的分析工具：\n{description}"
        }
        
        prompt = tool_prompts.get(question_type, f"分析以下CTF题目并推荐工具：\n{description}")
        
        try:
            # 这里可以调用AI API获取工具推荐
            # 为了简化，先返回基础推荐
            return {"tools": [], "commands": []}
        except Exception as e:
            print(f"工具推荐失败: {str(e)}")
            return {"tools": [], "commands": []} 