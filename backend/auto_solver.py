import asyncio
import subprocess
import tempfile
import os
import time
import json
import re
from typing import Dict, Any, Optional, List, Tuple
from data_service import data_service
from logger import get_logger
from ai_service import AIService

class AutoSolver:
    """自动解题引擎"""
    
    def __init__(self, db=None, ai_service: AIService = None):
        self.db = db
        self.ai_service = ai_service
        self.logger = get_logger("auto_solver")
        
        # 支持的编程语言
        self.supported_languages = {
            'python': {'ext': '.py', 'cmd': 'python3'},
            'javascript': {'ext': '.js', 'cmd': 'node'},
            'bash': {'ext': '.sh', 'cmd': 'bash'},
            'php': {'ext': '.php', 'cmd': 'php'},
            'ruby': {'ext': '.rb', 'cmd': 'ruby'},
            'go': {'ext': '.go', 'cmd': 'go run'},
            'rust': {'ext': '.rs', 'cmd': 'rustc'},
            'c': {'ext': '.c', 'cmd': 'gcc'},
            'cpp': {'ext': '.cpp', 'cmd': 'g++'}
        }
    
    async def solve_challenge(self, question_id: str, solve_method: str = None, 
                            custom_code: str = None, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """自动解题主函数"""
        
        # 获取题目信息
        question = data_service.get_challenge(question_id)
        if not question:
            raise ValueError(f"题目ID {question_id} 不存在")
        
        # 创建解题记录
        auto_solve_data = {
            "question_id": question_id,
            "status": "running",
            "solve_method": solve_method or "ai_generated"
        }
        
        auto_solve_record = data_service.save_auto_solve(auto_solve_data)
        
        try:
            start_time = time.time()
            
            # 根据解题方法选择策略
            if custom_code:
                # 使用用户自定义代码
                generated_code = custom_code
                language = self._detect_language(custom_code)
            elif solve_method == "template":
                # 使用解题模板
                generated_code, language = await self._generate_from_template(question, parameters)
            else:
                # 使用AI生成代码
                generated_code, language = await self._generate_ai_code(question)
            
            # 更新生成的代码
            data_service.update_auto_solve(auto_solve_record["id"], {
                "generated_code": generated_code
            })
            
            # 执行代码
            execution_result, flag, error = await self._execute_code(generated_code, language, parameters)
            
            # 计算执行时间
            execution_time = int(time.time() - start_time)
            
            # 更新结果
            status = "completed" if not error else "failed"
            updates = {
                "status": status,
                "execution_result": execution_result,
                "flag": flag,
                "error_message": error,
                "execution_time": execution_time
            }
            
            data_service.update_auto_solve(auto_solve_record["id"], updates)
            
            # 获取更新后的记录
            updated_record = data_service.get_auto_solve(auto_solve_record["id"])
            
            self.logger.info(f"自动解题完成，ID: {auto_solve_record['id']}, 状态: {status}")
            
            return updated_record
            
        except Exception as e:
            error_msg = f"自动解题失败: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            
            data_service.update_auto_solve(auto_solve_record["id"], {
                "status": "failed",
                "error_message": error_msg
            })
            
            return data_service.get_auto_solve(auto_solve_record["id"])
    
    async def _generate_ai_code(self, question: Dict[str, Any]) -> tuple[str, str]:
        """使用AI生成解题代码"""
        
        # 构建代码生成提示词
        code_prompt = f"""你是一个专业的CTF解题专家。请为以下CTF题目生成完整的解题代码：

题目描述：{question['description']}
题目类型：{question['type']}

请生成可以直接运行的完整Python代码，包括：
1. 必要的导入和依赖
2. 完整的解题逻辑
3. 错误处理
4. 结果输出

代码要求：
- 使用Python 3
- 代码要完整可执行
- 包含详细的注释
- 输出格式要清晰

请只返回代码，不要包含其他说明文字。"""

        # 调用AI生成代码
        ai_response = await self.ai_service.analyze_challenge(code_prompt, question['type'])
        
        # 提取代码部分
        code = self._extract_code_from_response(ai_response)
        if not code:
            raise ValueError("AI未能生成有效的解题代码")
        
        return code, "python"
    
    async def _generate_from_template(self, question: Dict[str, Any], parameters: Dict[str, Any] = None) -> tuple[str, str]:
        """从模板生成代码"""
        
        # 从文件存储中获取对应类型的模板
        templates = data_service.get_templates(category=question['type'])
        
        if not templates:
            # 如果没有找到对应类型的模板，使用默认模板
            template_code = self._get_default_template(question['type'])
        else:
            # 使用第一个可用的模板
            template_code = templates[0].get('template_code', '')
        
        if not template_code:
            raise ValueError(f"未找到题目类型 {question['type']} 的解题模板")
        
        # 替换模板参数
        code = template_code
        if parameters:
            for key, value in parameters.items():
                code = code.replace(f"{{{key}}}", str(value))
        
        # 检测语言
        language = self._detect_language(code)
        
        return code, language
    
    def _get_default_template(self, question_type: str) -> str:
        """获取默认模板"""
        templates = {
            "web": """import requests
import re

def solve_web_challenge():
    url = "{target_url}"
    
    # 发送请求
    response = requests.get(url)
    
    # 查找flag
    flag_pattern = r'flag{[^}]+}'
    flags = re.findall(flag_pattern, response.text)
    
    if flags:
        print(f"找到flag: {flags[0]}")
        return flags[0]
    else:
        print("未找到flag")
        return None

if __name__ == "__main__":
    solve_web_challenge()""",
            
            "crypto": """import hashlib
import base64

def solve_crypto_challenge():
    data = "{encrypted_data}"
    
    # 尝试不同的解密方法
    try:
        # Base64解码
        decoded = base64.b64decode(data)
        print(f"Base64解码结果: {decoded}")
    except:
        pass
    
    try:
        # MD5哈希
        md5_hash = hashlib.md5(data.encode()).hexdigest()
        print(f"MD5哈希: {md5_hash}")
    except:
        pass
    
    return "flag{placeholder}"

if __name__ == "__main__":
    solve_crypto_challenge()""",
            
            "pwn": """from pwn import *

def solve_pwn_challenge():
    # 连接到目标
    p = process("./{binary_name}")
    # p = remote("target.com", 1337)
    
    # 构造payload
    payload = b"A" * 64 + p64(0xdeadbeef)
    
    # 发送payload
    p.sendline(payload)
    
    # 获取响应
    response = p.recvall()
    print(f"响应: {response}")
    
    p.close()

if __name__ == "__main__":
    solve_pwn_challenge()"""
        }
        
        return templates.get(question_type, "# 默认模板\nprint('Hello, CTF!')")
    
    async def _execute_code(self, code: str, language: str, parameters: Dict[str, Any] = None) -> tuple[str, str, str]:
        """执行代码"""
        
        if language not in self.supported_languages:
            raise ValueError(f"不支持的语言: {language}")
        
        lang_config = self.supported_languages[language]
        
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix=lang_config['ext'],
                delete=False,
                encoding='utf-8'
            ) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            
            # 准备执行命令
            if language in ['c', 'cpp']:
                # 编译后执行
                output_file = temp_file_path.replace(lang_config['ext'], '')
                compile_cmd = f"{lang_config['cmd']} {temp_file_path} -o {output_file}"
                
                # 编译
                compile_result = subprocess.run(
                    compile_cmd.split(),
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if compile_result.returncode != 0:
                    return "", "", f"编译失败: {compile_result.stderr}"
                
                # 执行
                exec_cmd = [output_file]
                if parameters and 'input' in parameters:
                    exec_cmd = ['echo', parameters['input'], '|', output_file]
                
                result = subprocess.run(
                    exec_cmd,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                # 清理编译文件
                try:
                    os.unlink(output_file)
                except:
                    pass
                    
            else:
                # 直接解释执行
                cmd = lang_config['cmd'].split() + [temp_file_path]
                
                # 准备输入
                input_data = None
                if parameters and 'input' in parameters:
                    input_data = parameters['input'].encode()
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    input=input_data,
                    timeout=60
                )
            
            # 清理临时文件
            try:
                os.unlink(temp_file_path)
            except:
                pass
            
            # 分析输出
            output = result.stdout.strip()
            error = result.stderr.strip() if result.stderr else None
            
            # 提取flag
            flag = self._extract_flag(output)
            
            return output, flag, error
            
        except subprocess.TimeoutExpired:
            return "", "", "代码执行超时"
        except Exception as e:
            return "", "", f"执行异常: {str(e)}"
    
    def _extract_code_from_response(self, response: str) -> str:
        """从AI响应中提取代码"""
        
        # 尝试提取代码块
        code_patterns = [
            r'```python\n(.*?)\n```',
            r'```py\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```(.*?)```'
        ]
        
        for pattern in code_patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # 如果没有找到代码块，尝试提取整个响应
        lines = response.strip().split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                in_code = True
            if in_code:
                code_lines.append(line)
        
        if code_lines:
            return '\n'.join(code_lines)
        
        return response.strip()
    
    def _extract_flag(self, output: str) -> str:
        """从输出中提取flag"""
        
        # 常见的flag格式
        flag_patterns = [
            r'flag{[^}]+}',
            r'FLAG{[^}]+}',
            r'ctf{[^}]+}',
            r'CTF{[^}]+}',
            r'key{[^}]+}',
            r'KEY{[^}]+}'
        ]
        
        for pattern in flag_patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return ""
    
    def _detect_language(self, code: str) -> str:
        """检测代码语言"""
        
        # 简单的语言检测
        if 'import ' in code or 'from ' in code or 'def ' in code:
            return 'python'
        elif 'function ' in code or 'const ' in code or 'let ' in code:
            return 'javascript'
        elif '<?php' in code or '$' in code:
            return 'php'
        elif '#!/bin/bash' in code or 'echo ' in code:
            return 'bash'
        elif 'package main' in code or 'import "' in code:
            return 'go'
        elif 'fn main' in code or 'use ' in code:
            return 'rust'
        elif '#include' in code:
            return 'c'
        else:
            return 'python'  # 默认Python
    
    async def get_solve_templates(self, category: str = None) -> List[Dict[str, Any]]:
        """获取解题模板"""
        return data_service.get_templates(category=category)
    
    async def create_solve_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建解题模板"""
        success = data_service.add_template(template_data)
        if not success:
            raise Exception("创建模板失败")
        
        # 返回创建的模板
        template_name = template_data.get('name')
        return data_service.get_template_by_name(template_name)
    
    async def update_solve_template(self, name: str, template_data: Dict[str, Any]) -> bool:
        """更新解题模板"""
        return data_service.update_template(name, template_data)
    
    async def delete_solve_template(self, name: str) -> bool:
        """删除解题模板"""
        return data_service.delete_template(name)
    
    async def enable_solve_template(self, name: str) -> bool:
        """启用解题模板"""
        return data_service.enable_template(name)
    
    async def disable_solve_template(self, name: str) -> bool:
        """禁用解题模板"""
        return data_service.disable_template(name) 