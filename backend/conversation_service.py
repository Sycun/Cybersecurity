import uuid
import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from data_service import data_service
from logger import get_logger

class ConversationService:
    """多轮对话管理服务"""
    
    def __init__(self):
        self.logger = get_logger("conversation_service")
        self.max_context_length = 4000  # 最大上下文长度
        self.max_history_messages = 10   # 最大历史消息数
        self.context_decay_hours = 24    # 上下文衰减时间（小时）
    
    def create_conversation(self, user_id: str = None, initial_context: Dict[str, Any] = None) -> str:
        """创建新的对话会话"""
        conversation_id = str(uuid.uuid4())
        
        conversation_data = {
            "id": conversation_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": [],
            "context": initial_context or {},
            "metadata": {
                "question_type": None,
                "challenge_id": None,
                "ai_provider": None
            }
        }
        
        # 保存到文件
        data_service.save_conversation(conversation_data)
        
        self.logger.info(f"创建新对话会话: {conversation_id}")
        return conversation_id
    
    def add_message(self, conversation_id: str, role: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """添加消息到对话"""
        try:
            conversation = data_service.get_conversation(conversation_id)
            if not conversation:
                return False
            
            message = {
                "id": str(uuid.uuid4()),
                "role": role,  # "user" 或 "assistant"
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            conversation["messages"].append(message)
            conversation["updated_at"] = datetime.now().isoformat()
            
            # 更新元数据
            if metadata:
                if "question_type" in metadata:
                    conversation["metadata"]["question_type"] = metadata["question_type"]
                if "challenge_id" in metadata:
                    conversation["metadata"]["challenge_id"] = metadata["challenge_id"]
                if "ai_provider" in metadata:
                    conversation["metadata"]["ai_provider"] = metadata["ai_provider"]
            
            # 限制消息数量
            if len(conversation["messages"]) > self.max_history_messages:
                conversation["messages"] = conversation["messages"][-self.max_history_messages:]
            
            # 保存更新
            data_service.save_conversation(conversation)
            
            self.logger.info(f"添加消息到对话 {conversation_id}: {role}")
            return True
            
        except Exception as e:
            self.logger.error(f"添加消息失败: {e}")
            return False
    
    def get_conversation_context(self, conversation_id: str) -> Dict[str, Any]:
        """获取对话上下文"""
        try:
            conversation = data_service.get_conversation(conversation_id)
            if not conversation:
                return {}
            
            # 检查上下文是否过期
            updated_at = datetime.fromisoformat(conversation["updated_at"])
            if datetime.now() - updated_at > timedelta(hours=self.context_decay_hours):
                self.logger.info(f"对话上下文已过期: {conversation_id}")
                return {}
            
            return conversation.get("context", {})
            
        except Exception as e:
            self.logger.error(f"获取对话上下文失败: {e}")
            return {}
    
    def update_conversation_context(self, conversation_id: str, context_updates: Dict[str, Any]) -> bool:
        """更新对话上下文"""
        try:
            conversation = data_service.get_conversation(conversation_id)
            if not conversation:
                return False
            
            # 更新上下文
            current_context = conversation.get("context", {})
            current_context.update(context_updates)
            conversation["context"] = current_context
            conversation["updated_at"] = datetime.now().isoformat()
            
            # 保存更新
            data_service.save_conversation(conversation)
            
            self.logger.info(f"更新对话上下文: {conversation_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"更新对话上下文失败: {e}")
            return False
    
    def get_conversation_history(self, conversation_id: str, limit: int = None) -> List[Dict[str, Any]]:
        """获取对话历史"""
        try:
            conversation = data_service.get_conversation(conversation_id)
            if not conversation:
                return []
            
            messages = conversation.get("messages", [])
            if limit:
                messages = messages[-limit:]
            
            return messages
            
        except Exception as e:
            self.logger.error(f"获取对话历史失败: {e}")
            return []
    
    def build_conversation_prompt(self, conversation_id: str, current_question: str, question_type: str) -> str:
        """构建多轮对话的提示词"""
        try:
            conversation = data_service.get_conversation(conversation_id)
            if not conversation:
                return current_question
            
            messages = conversation.get("messages", [])
            context = conversation.get("context", {})
            
            conversation_history = []
            for msg in messages[-6:]:
                role = "用户" if msg["role"] == "user" else "AI助手"
                conversation_history.append(f"{role}: {msg['content']}")
            
            prompt_parts = []
            
            if conversation_history:
                prompt_parts.append("## 对话历史")
                prompt_parts.extend(conversation_history)
                prompt_parts.append("")
            
            prompt_parts.append("## 当前问题")
            prompt_parts.append(f"题目类型: {question_type}")
            prompt_parts.append(f"题目描述: {current_question}")
            prompt_parts.append("请基于对话历史提供更精准的分析。")
            
            return "\n".join(prompt_parts)
            
        except Exception as e:
            self.logger.error(f"构建对话提示词失败: {e}")
            return current_question
    
    def get_user_conversations(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取用户的对话列表"""
        try:
            conversations = data_service.get_user_conversations(user_id, limit)
            return conversations
        except Exception as e:
            self.logger.error(f"获取用户对话列表失败: {e}")
            return []
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """删除对话"""
        try:
            success = data_service.delete_conversation(conversation_id)
            if success:
                self.logger.info(f"删除对话: {conversation_id}")
            return success
        except Exception as e:
            self.logger.error(f"删除对话失败: {e}")
            return False
    
    def cleanup_expired_conversations(self) -> int:
        """清理过期的对话"""
        try:
            expired_count = data_service.cleanup_expired_conversations(self.context_decay_hours)
            self.logger.info(f"清理了 {expired_count} 个过期对话")
            return expired_count
        except Exception as e:
            self.logger.error(f"清理过期对话失败: {e}")
            return 0

# 全局实例
conversation_service = ConversationService() 