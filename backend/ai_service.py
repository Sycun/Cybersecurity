import os
import hashlib
import json
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from ai_providers import AIProviderFactory, AIProvider
from config import config
from logger import get_logger
from data_service import data_service

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
    
    def _generate_cache_key(self, description: str, question_type: str, provider: str) -> str:
        content = f"{description}|{question_type}|{provider}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _collect_context(self, description: str, question_type: str, user_id: str = None) -> Dict[str, Any]:
        """收集上下文信息"""
        context = {
            "user_preferences": {},
            "history_summary": "",
            "similar_challenges": [],
            "tool_usage": [],
            "success_patterns": []
        }
        
        try:
            # 1. 获取用户偏好设置
            user_config = data_service.get_user_config()
            context["user_preferences"] = {
                "ai_provider": user_config.get("ai_provider", "deepseek"),
                "language": user_config.get("ai_settings", {}).get("language", "zh"),
                "analysis_style": user_config.get("analysis_settings", {}).get("style", "detailed")
            }
            
            # 2. 获取历史分析记录摘要
            history = data_service.get_analysis_history(limit=10)
            if history:
                # 提取相似题目的分析结果
                similar_history = [h for h in history if h.get("analysis_data", {}).get("type") == question_type]
                if similar_history:
                    context["history_summary"] = self._summarize_history(similar_history[:3])
                    context["similar_challenges"] = similar_history[:3]
            
            # 3. 获取工具使用历史
            tools = data_service.get_tools()
            if tools:
                # 根据题目类型推荐相关工具
                relevant_tools = [tool for tool in tools if tool.get("category") == question_type]
                context["tool_usage"] = relevant_tools[:5]
            
            # 4. 获取成功解题模式
            auto_solves = data_service.get_auto_solves(limit=10)
            if auto_solves:
                successful_solves = [solve for solve in auto_solves if solve.get("status") == "completed"]
                context["success_patterns"] = self._extract_success_patterns(successful_solves)
            
            self.logger.info(f"收集到上下文信息: {len(context)} 个维度")
            
        except Exception as e:
            self.logger.warning(f"收集上下文信息失败: {e}")
        
        return context
    
    def _summarize_history(self, history: List[Dict[str, Any]]) -> str:
        """总结历史分析记录"""
        if not history:
            return ""
        
        summary_parts = []
        for record in history:
            analysis_data = record.get("analysis_data", {})
            summary_parts.append(f"题目类型: {analysis_data.get('type', 'unknown')}")
            if analysis_data.get('ai_response'):
                # 提取AI响应的关键信息
                response = analysis_data['ai_response']
                if '## 分析思路' in response:
                    summary_parts.append("包含详细分析思路")
                if '## 解题步骤' in response:
                    summary_parts.append("包含具体解题步骤")
                if 'flag{' in response.lower():
                    summary_parts.append("包含flag信息")
        
        return " | ".join(summary_parts[:5])  # 限制长度
    
    def _extract_success_patterns(self, successful_solves: List[Dict[str, Any]]) -> List[str]:
        """提取成功解题模式"""
        patterns = []
        for solve in successful_solves:
            method = solve.get("solve_method", "")
            if method:
                patterns.append(f"成功使用 {method} 方法解题")
            
            if solve.get("flag"):
                patterns.append("成功获取flag")
        
        return patterns[:3]  # 限制数量
    
    def _build_context_prompt(self, description: str, question_type: str, context: Dict[str, Any]) -> str:
        """构建包含上下文的提示词"""
        base_prompt = self.provider.get_prompt_template(question_type)
        
        # 构建上下文信息
        context_info = []
        
        # 用户偏好
        if context.get("user_preferences"):
            prefs = context["user_preferences"]
            context_info.append(f"用户偏好: 使用{prefs.get('language', '中文')}分析，风格{prefs.get('analysis_style', '详细')}")
        
        # 历史分析摘要
        if context.get("history_summary"):
            context_info.append(f"历史分析摘要: {context['history_summary']}")
        
        # 相关工具推荐
        if context.get("tool_usage"):
            tools = [tool.get("name", "") for tool in context["tool_usage"]]
            context_info.append(f"推荐工具: {', '.join(tools)}")
        
        # 成功模式
        if context.get("success_patterns"):
            patterns = context["success_patterns"]
            context_info.append(f"成功模式: {'; '.join(patterns)}")
        
        # 组合上下文信息
        if context_info:
            context_section = "\n\n## 上下文信息\n" + "\n".join(f"- {info}" for info in context_info)
            enhanced_prompt = base_prompt.replace("{description}", f"{description}\n{context_section}")
        else:
            enhanced_prompt = base_prompt.replace("{description}", description)
        
        return enhanced_prompt

    async def analyze_challenge(self, description: str, question_type: str, user_id: str = None, use_context: bool = True) -> str:
        """
        分析CTF题目（支持上下文增强）
        
        Args:
            description: 题目描述
            question_type: 题目类型
            user_id: 用户ID（可选）
            use_context: 是否使用上下文增强
            
        Returns:
            AI分析结果
        """
        try:
            # 收集上下文信息
            context = self._collect_context(description, question_type, user_id) if use_context else {}
            
            # 生成缓存键（包含上下文哈希）
            context_hash = hashlib.md5(json.dumps(context, sort_keys=True).encode()).hexdigest()[:8]
            cache_key = self._generate_cache_key(description, question_type, self.provider_type)
            
            # 检查缓存
            cached_response = data_service.get_cache(cache_key)
            if cached_response:
                self.logger.info(f"使用上下文缓存响应，题目类型: {question_type}")
                return cached_response
            
            # 构建增强的提示词
            if use_context and context:
                enhanced_prompt = self._build_context_prompt(description, question_type, context)
                self.logger.info(f"使用上下文增强分析，题目类型: {question_type}, 提供者: {self.provider_type}")
            else:
                enhanced_prompt = self.provider.get_prompt_template(question_type).format(description=description)
                self.logger.info(f"使用标准分析，题目类型: {question_type}, 提供者: {self.provider_type}")
            
            # 调用AI分析
            response = await self.provider.analyze_challenge(enhanced_prompt, question_type)
            
            # 缓存结果
            data_service.save_cache(cache_key, response, ttl=config.CACHE_TTL)
            
            return response
            
        except Exception as e:
            error_msg = f"AI服务异常: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return f"AI分析遇到问题，请检查配置或稍后重试。错误信息: {error_msg}"
    
    async def generate_solve_code(self, description: str, question_type: str) -> str:
        """
        生成解题代码
        
        Args:
            description: 题目描述
            question_type: 题目类型
            
        Returns:
            生成的解题代码
        """
        try:
            self.logger.info(f"生成解题代码，类型: {question_type}, 提供者: {self.provider_type}")
            
            # 获取代码生成专用的提示词模板
            if hasattr(self.provider, 'get_code_generation_template'):
                template = self.provider.get_code_generation_template(question_type)
            else:
                # 如果没有专门的代码生成模板，使用通用模板
                template = f"""你是一个专业的CTF解题专家。请为以下CTF题目生成完整的Python解题代码：

题目描述：{description}
题目类型：{question_type}

要求：
1. 生成完整可执行的Python代码
2. 包含所有必要的导入
3. 实现完整的解题逻辑
4. 包含错误处理
5. 输出结果要清晰

代码要求：
- 使用标准库和常见库
- 包含详细的注释
- 处理异常情况
- 输出flag或关键信息

请只返回Python代码，不要包含其他说明文字。"""
            
            prompt = template.format(description=description)
            
            # 调用AI生成代码
            response = await self.provider.analyze_challenge(prompt, question_type)
            
            # 提取代码部分
            code = self._extract_code_from_response(response)
            
            if not code:
                raise ValueError("AI未能生成有效的解题代码")
            
            return code
            
        except Exception as e:
            error_msg = f"代码生成失败: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise ValueError(f"代码生成遇到问题: {error_msg}")
    
    def _extract_code_from_response(self, response: str) -> str:
        """从AI响应中提取代码"""
        import re
        
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
        # 文件缓存不统计命中率，仅返回缓存文件数
        cache_files = len(list(data_service.cache_dir.glob("cache_*.json")))
        return {
            "provider": self.provider_type,
            "provider_stats": provider_stats,
            "cache_files": cache_files
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
            # 清理旧提供者的缓存（可选：这里只清理过期缓存）
            data_service.clear_expired_cache()
            self.logger.info(f"AI提供者切换成功: {old_provider} -> {provider_type}")
            return True
        except Exception as e:
            self.logger.error(f"切换AI提供者失败: {str(e)}")
            return False
    
    def clear_cache(self):
        """清空缓存"""
        cleared = data_service.clear_expired_cache()
        self.logger.info(f"AI响应缓存已清空，清理了{cleared}个过期缓存文件")
    
    @staticmethod
    def get_available_providers() -> Dict[str, str]:
        """
        获取所有可用的AI提供者
        
        Returns:
            可用提供者字典
        """
        return AIProviderFactory.get_available_providers() 