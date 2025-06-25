import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import asyncio
from ai_service import AIService
from logger import get_logger

@dataclass
class ConversationContext:
    """对话上下文数据类"""
    session_id: str
    messages: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class AdvancedPromptEngine:
    """高级提示词引擎"""
    
    def __init__(self):
        self.logger = get_logger("advanced_prompt_engine")
        self.context_templates = self._load_context_templates()
        self.dynamic_prompts = self._load_dynamic_prompts()
    
    def _load_context_templates(self) -> Dict[str, str]:
        """加载上下文模板"""
        return {
            "web": {
                "expert_context": """你是一位拥有10年Web安全经验的专家，精通：
- OWASP Top 10漏洞
- 现代Web框架安全
- 前后端分离架构安全
- 云原生安全
- 移动端Web安全
- 新兴技术安全（Web3、AI应用安全）

分析风格：系统性、深度、实用性强""",
                
                "beginner_context": """你是一位耐心的Web安全导师，擅长：
- 基础概念解释
- 循序渐进的教学
- 实际案例演示
- 常见错误提醒
- 学习路径指导

分析风格：通俗易懂、步骤详细、适合初学者""",
                
                "advanced_context": """你是一位CTF竞赛专家，专注于：
- 高级绕过技巧
- 0day漏洞利用
- 复杂链式攻击
- 反调试对抗
- 自动化工具开发

分析风格：技术深度、创新思维、竞赛导向"""
            },
            
            "pwn": {
                "expert_context": """你是一位二进制安全大师，专精：
- 现代操作系统安全机制
- 高级ROP/JOP技术
- 内核漏洞利用
- 硬件安全
- 逆向工程自动化

分析风格：技术前沿、深度分析、创新方法""",
                
                "beginner_context": """你是一位二进制安全导师，擅长：
- 基础概念讲解
- 工具使用指导
- 调试技巧传授
- 常见错误分析
- 学习资源推荐

分析风格：循序渐进、实例丰富、易于理解""",
                
                "advanced_context": """你是一位Pwn竞赛专家，专注于：
- 复杂漏洞链构造
- 高级利用技术
- 反调试对抗
- 自动化exploit开发
- 最新漏洞研究

分析风格：竞赛导向、技术深度、实用性强"""
            }
        }
    
    def _load_dynamic_prompts(self) -> Dict[str, str]:
        """加载动态提示词模板"""
        return {
            "code_analysis": """请分析以下代码片段，识别潜在的安全漏洞：

```{language}
{code}
```

分析要求：
1. 漏洞类型识别
2. 漏洞原理分析
3. 利用方法说明
4. 修复建议
5. 相关CVE参考""",
            
            "network_analysis": """请分析以下网络流量/配置，识别安全问题：

{network_data}

分析要求：
1. 协议分析
2. 安全风险识别
3. 攻击向量分析
4. 防护建议
5. 相关工具推荐""",
            
            "forensics_analysis": """请分析以下取证数据，寻找关键信息：

{forensics_data}

分析要求：
1. 数据特征识别
2. 时间线分析
3. 关键信息提取
4. 证据链构建
5. 工具使用建议"""
        }
    
    def build_enhanced_prompt(self, 
                             question_type: str, 
                             description: str, 
                             skill_level: str = "expert",
                             context_data: Optional[Dict[str, Any]] = None) -> str:
        """构建增强提示词"""
        
        # 获取基础上下文
        base_context = self.context_templates.get(question_type, {}).get(skill_level, "")
        
        # 构建动态内容
        dynamic_content = ""
        if context_data:
            if "code" in context_data:
                dynamic_content = self.dynamic_prompts["code_analysis"].format(
                    language=context_data.get("language", "text"),
                    code=context_data["code"]
                )
            elif "network_data" in context_data:
                dynamic_content = self.dynamic_prompts["network_analysis"].format(
                    network_data=context_data["network_data"]
                )
            elif "forensics_data" in context_data:
                dynamic_content = self.dynamic_prompts["forensics_analysis"].format(
                    forensics_data=context_data["forensics_data"]
                )
        
        # 构建完整提示词
        enhanced_prompt = f"""{base_context}

## 题目分析任务

题目描述：
{description}

{dynamic_content}

## 分析要求

请提供以下格式的详细分析：

### 1. 题目类型识别
- 主要漏洞类型：
- 涉及技术栈：
- 难度评估：

### 2. 深度分析
- 漏洞原理：
- 攻击向量：
- 利用条件：

### 3. 解题策略
- 分析步骤：
- 关键检查点：
- 工具使用：

### 4. 利用代码
```python
# 提供完整的利用代码
```

### 5. 防护建议
- 修复方案：
- 最佳实践：
- 学习资源：

### 6. 进阶思考
- 变种分析：
- 防御绕过：
- 自动化思路：

请确保分析的专业性、实用性和可操作性。"""

        return enhanced_prompt
    
    def extract_key_insights(self, ai_response: str) -> Dict[str, Any]:
        """从AI响应中提取关键洞察"""
        insights = {
            "vulnerability_types": [],
            "tools_mentioned": [],
            "difficulty_level": "",
            "key_techniques": [],
            "code_snippets": [],
            "learning_resources": []
        }
        
        # 提取漏洞类型
        vuln_pattern = r"漏洞类型[：:]\s*(.+)"
        vuln_matches = re.findall(vuln_pattern, ai_response)
        insights["vulnerability_types"] = [v.strip() for v in vuln_matches]
        
        # 提取工具
        tool_pattern = r"(工具|使用|推荐)[：:]\s*(.+)"
        tool_matches = re.findall(tool_pattern, ai_response)
        insights["tools_mentioned"] = [t[1].strip() for t in tool_matches]
        
        # 提取代码片段
        code_pattern = r"```(?:python|bash|sh|js|php|java|cpp|c|go|rust)?\n(.*?)```"
        code_matches = re.findall(code_pattern, ai_response, re.DOTALL)
        insights["code_snippets"] = code_matches
        
        # 提取学习资源
        resource_pattern = r"(学习|参考|资源)[：:]\s*(.+)"
        resource_matches = re.findall(resource_pattern, ai_response)
        insights["learning_resources"] = [r[1].strip() for r in resource_matches]
        
        return insights

class ConversationManager:
    """对话管理器"""
    
    def __init__(self):
        self.logger = get_logger("conversation_manager")
        self.conversations: Dict[str, ConversationContext] = {}
        self.max_context_length = 10  # 最大上下文长度
    
    def create_conversation(self, session_id: str, initial_context: Dict[str, Any] = None) -> str:
        """创建新对话"""
        now = datetime.now()
        conversation = ConversationContext(
            session_id=session_id,
            messages=[],
            metadata=initial_context or {},
            created_at=now,
            updated_at=now
        )
        self.conversations[session_id] = conversation
        self.logger.info(f"创建新对话: {session_id}")
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Dict[str, Any] = None):
        """添加消息到对话"""
        if session_id not in self.conversations:
            self.create_conversation(session_id)
        
        conversation = self.conversations[session_id]
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        conversation.messages.append(message)
        conversation.updated_at = datetime.now()
        
        # 限制上下文长度
        if len(conversation.messages) > self.max_context_length:
            conversation.messages = conversation.messages[-self.max_context_length:]
        
        self.logger.info(f"添加消息到对话 {session_id}: {role}")
    
    def get_conversation_context(self, session_id: str) -> List[Dict[str, Any]]:
        """获取对话上下文"""
        if session_id not in self.conversations:
            return []
        
        return self.conversations[session_id].messages
    
    def build_context_prompt(self, session_id: str, current_question: str) -> str:
        """构建带上下文的提示词"""
        context_messages = self.get_conversation_context(session_id)
        
        if not context_messages:
            return current_question
        
        context_prompt = "## 对话历史\n\n"
        for msg in context_messages[-5:]:  # 只使用最近5条消息
            context_prompt += f"**{msg['role']}**: {msg['content']}\n\n"
        
        context_prompt += f"## 当前问题\n\n{current_question}\n\n"
        context_prompt += "请基于以上对话历史，提供连贯且深入的解答。"
        
        return context_prompt

class AIEnhancementService:
    """AI增强服务"""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.prompt_engine = AdvancedPromptEngine()
        self.conversation_manager = ConversationManager()
        self.logger = get_logger("ai_enhancement_service")
    
    async def analyze_with_enhanced_prompt(self, 
                                         description: str, 
                                         question_type: str,
                                         skill_level: str = "expert",
                                         context_data: Optional[Dict[str, Any]] = None,
                                         session_id: Optional[str] = None) -> Dict[str, Any]:
        """使用增强提示词进行分析"""
        
        try:
            # 构建增强提示词
            enhanced_prompt = self.prompt_engine.build_enhanced_prompt(
                question_type, description, skill_level, context_data
            )
            
            # 如果有会话ID，添加上下文
            if session_id:
                enhanced_prompt = self.conversation_manager.build_context_prompt(
                    session_id, enhanced_prompt
                )
            
            # 调用AI服务
            ai_response = await self.ai_service.analyze_challenge(enhanced_prompt, question_type)
            
            # 提取关键洞察
            insights = self.prompt_engine.extract_key_insights(ai_response)
            
            # 保存到对话历史
            if session_id:
                self.conversation_manager.add_message(
                    session_id, "user", description, {"question_type": question_type}
                )
                self.conversation_manager.add_message(
                    session_id, "assistant", ai_response, insights
                )
            
            return {
                "response": ai_response,
                "insights": insights,
                "enhanced_prompt": enhanced_prompt,
                "session_id": session_id
            }
            
        except Exception as e:
            self.logger.error(f"增强分析失败: {str(e)}", exc_info=True)
            raise
    
    async def multi_turn_analysis(self, 
                                session_id: str,
                                messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """多轮对话分析"""
        
        try:
            # 创建或获取对话
            if session_id not in self.conversation_manager.conversations:
                self.conversation_manager.create_conversation(session_id)
            
            # 处理每条消息
            responses = []
            for msg in messages:
                if msg["role"] == "user":
                    # 分析用户消息
                    question_type = msg.get("question_type", "general")
                    response = await self.analyze_with_enhanced_prompt(
                        msg["content"], 
                        question_type,
                        msg.get("skill_level", "expert"),
                        msg.get("context_data"),
                        session_id
                    )
                    responses.append(response)
            
            return {
                "session_id": session_id,
                "responses": responses,
                "conversation_context": self.conversation_manager.get_conversation_context(session_id)
            }
            
        except Exception as e:
            self.logger.error(f"多轮分析失败: {str(e)}", exc_info=True)
            raise
    
    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """获取对话摘要"""
        if session_id not in self.conversation_manager.conversations:
            return {"error": "对话不存在"}
        
        conversation = self.conversation_manager.conversations[session_id]
        
        # 统计信息
        user_messages = [msg for msg in conversation.messages if msg["role"] == "user"]
        assistant_messages = [msg for msg in conversation.messages if msg["role"] == "assistant"]
        
        # 提取关键主题
        topics = []
        for msg in user_messages:
            if "metadata" in msg and "question_type" in msg["metadata"]:
                topics.append(msg["metadata"]["question_type"])
        
        return {
            "session_id": session_id,
            "total_messages": len(conversation.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "topics": list(set(topics)),
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "metadata": conversation.metadata
        } 