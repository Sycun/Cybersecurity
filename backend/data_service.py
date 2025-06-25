import json
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import shutil

class DataService:
    """数据服务类，负责管理data文件夹中的数据读写"""
    
    def __init__(self):
        # 修改路径，使其指向项目根目录下的data文件夹
        self.data_root = Path("../data")
        self.challenges_dir = self.data_root / "challenges"
        self.history_dir = self.data_root / "analysis_history"
        self.configs_dir = self.data_root / "configs"
        self.cache_dir = self.data_root / "cache"
        self.exports_dir = self.data_root / "exports"
        
        # 确保目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保所有必要的目录存在"""
        directories = [
            self.data_root,
            self.challenges_dir,
            self.history_dir,
            self.configs_dir,
            self.cache_dir,
            self.exports_dir
        ]
        
        # 创建题目类型子目录
        challenge_types = ["web", "pwn", "reverse", "crypto", "misc"]
        for challenge_type in challenge_types:
            directories.append(self.challenges_dir / challenge_type)
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        return str(uuid.uuid4())
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        return datetime.now().isoformat()
    
    def _read_json_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """读取JSON文件"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"读取文件失败 {file_path}: {e}")
        return None
    
    def _write_json_file(self, file_path: Path, data: Dict[str, Any]) -> bool:
        """写入JSON文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"写入文件失败 {file_path}: {e}")
            return False
    
    # 题目相关操作
    def save_challenge(self, description: str, question_type: str, ai_response: str, 
                      file_name: Optional[str] = None) -> Dict[str, Any]:
        """保存题目分析记录"""
        challenge_id = self._generate_id()
        timestamp = self._get_timestamp()
        
        challenge_data = {
            "id": challenge_id,
            "description": description,
            "type": question_type,
            "ai_response": ai_response,
            "file_name": file_name,
            "timestamp": timestamp
        }
        
        # 保存到对应类型的目录
        file_path = self.challenges_dir / question_type / f"challenge_{challenge_id}.json"
        if self._write_json_file(file_path, challenge_data):
            return challenge_data
        else:
            raise Exception("保存题目失败")
    
    def get_challenge(self, challenge_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取题目"""
        # 在所有类型目录中查找
        for challenge_type in ["web", "pwn", "reverse", "crypto", "misc"]:
            type_dir = self.challenges_dir / challenge_type
            for file_path in type_dir.glob("*.json"):
                data = self._read_json_file(file_path)
                if data and data.get("id") == challenge_id:
                    return data
        return None
    
    def get_challenges(self, challenge_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取题目列表"""
        challenges = []
        
        if challenge_type:
            # 获取指定类型的题目
            type_dir = self.challenges_dir / challenge_type
            if type_dir.exists():
                for file_path in sorted(type_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
                    data = self._read_json_file(file_path)
                    if data:
                        challenges.append(data)
                        if len(challenges) >= limit:
                            break
        else:
            # 获取所有类型的题目
            for challenge_type in ["web", "pwn", "reverse", "crypto", "misc"]:
                type_dir = self.challenges_dir / challenge_type
                if type_dir.exists():
                    for file_path in sorted(type_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
                        data = self._read_json_file(file_path)
                        if data:
                            challenges.append(data)
                            if len(challenges) >= limit:
                                break
                    if len(challenges) >= limit:
                        break
        
        # 按时间戳排序
        challenges.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return challenges[:limit]
    
    def delete_challenge(self, challenge_id: str) -> bool:
        """删除题目"""
        for challenge_type in ["web", "pwn", "reverse", "crypto", "misc"]:
            type_dir = self.challenges_dir / challenge_type
            for file_path in type_dir.glob("*.json"):
                data = self._read_json_file(file_path)
                if data and data.get("id") == challenge_id:
                    try:
                        file_path.unlink()
                        return True
                    except Exception as e:
                        print(f"删除文件失败 {file_path}: {e}")
                        return False
        return False
    
    # 分析历史相关操作
    def save_analysis_history(self, challenge_id: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """保存分析历史"""
        history_id = self._generate_id()
        timestamp = self._get_timestamp()
        
        history_data = {
            "id": history_id,
            "challenge_id": challenge_id,
            "analysis_data": analysis_data,
            "timestamp": timestamp
        }
        
        file_path = self.history_dir / f"history_{history_id}.json"
        if self._write_json_file(file_path, history_data):
            return history_data
        else:
            raise Exception("保存分析历史失败")
    
    def get_analysis_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取分析历史"""
        history = []
        
        for file_path in sorted(self.history_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            data = self._read_json_file(file_path)
            if data:
                history.append(data)
                if len(history) >= limit:
                    break
        
        return history
    
    # 配置相关操作
    def save_config(self, config_name: str, config_data: Dict[str, Any]) -> bool:
        """保存配置"""
        file_path = self.configs_dir / f"{config_name}.json"
        return self._write_json_file(file_path, config_data)
    
    def get_config(self, config_name: str) -> Optional[Dict[str, Any]]:
        """获取配置"""
        file_path = self.configs_dir / f"{config_name}.json"
        return self._read_json_file(file_path)
    
    def get_all_configs(self) -> Dict[str, Any]:
        """获取所有配置"""
        configs = {}
        for file_path in self.configs_dir.glob("*.json"):
            config_name = file_path.stem
            config_data = self._read_json_file(file_path)
            if config_data:
                configs[config_name] = config_data
        return configs
    
    # 缓存相关操作
    def save_cache(self, key: str, data: Any, ttl: int = 3600) -> bool:
        """保存缓存"""
        cache_data = {
            "data": data,
            "timestamp": datetime.now().timestamp(),
            "ttl": ttl
        }
        
        # 使用key的hash作为文件名
        safe_key = "".join(c for c in key if c.isalnum() or c in ('-', '_')).rstrip()
        file_path = self.cache_dir / f"cache_{safe_key}.json"
        return self._write_json_file(file_path, cache_data)
    
    def get_cache(self, key: str) -> Optional[Any]:
        """获取缓存"""
        safe_key = "".join(c for c in key if c.isalnum() or c in ('-', '_')).rstrip()
        file_path = self.cache_dir / f"cache_{safe_key}.json"
        
        cache_data = self._read_json_file(file_path)
        if cache_data:
            timestamp = cache_data.get("timestamp", 0)
            ttl = cache_data.get("ttl", 3600)
            
            # 检查是否过期
            if datetime.now().timestamp() - timestamp < ttl:
                return cache_data.get("data")
            else:
                # 删除过期缓存
                try:
                    file_path.unlink()
                except:
                    pass
        
        return None
    
    def clear_expired_cache(self) -> int:
        """清理过期缓存，返回清理的文件数量"""
        cleared_count = 0
        current_time = datetime.now().timestamp()
        
        for file_path in self.cache_dir.glob("cache_*.json"):
            cache_data = self._read_json_file(file_path)
            if cache_data:
                timestamp = cache_data.get("timestamp", 0)
                ttl = cache_data.get("ttl", 3600)
                
                if current_time - timestamp >= ttl:
                    try:
                        file_path.unlink()
                        cleared_count += 1
                    except:
                        pass
        
        return cleared_count
    
    # 导出相关操作
    def export_data(self, data_type: str, data: List[Dict[str, Any]], format: str = "json") -> str:
        """导出数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{data_type}_{timestamp}.{format}"
        file_path = self.exports_dir / filename
        
        if format == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif format == "csv":
            if data:
                import csv
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
        
        return str(file_path)
    
    # 工具相关操作
    def save_tools(self, tools: List[Dict[str, Any]]) -> bool:
        """保存工具列表"""
        file_path = self.configs_dir / "tools.json"
        return self._write_json_file(file_path, {"tools": tools})
    
    def get_tools(self, category: str = None) -> List[Dict[str, Any]]:
        """获取工具列表"""
        file_path = self.configs_dir / "tools.json"
        data = self._read_json_file(file_path)
        
        if not data or "tools" not in data:
            return []
        
        tools = data["tools"]
        if category:
            tools = [tool for tool in tools if tool.get("category") == category]
        
        return tools
    
    def get_tool_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取工具"""
        tools = self.get_tools()
        for tool in tools:
            if tool.get("name") == name:
                return tool
        return None
    
    def add_tool(self, tool: Dict[str, Any]) -> bool:
        """添加工具"""
        tools = self.get_tools()
        tools.append(tool)
        return self.save_tools(tools)
    
    def update_tool(self, name: str, updated_tool: Dict[str, Any]) -> bool:
        """更新工具"""
        tools = self.get_tools()
        for i, tool in enumerate(tools):
            if tool.get("name") == name:
                tools[i] = updated_tool
                return self.save_tools(tools)
        return False
    
    def delete_tool(self, name: str) -> bool:
        """删除工具"""
        tools = self.get_tools()
        tools = [tool for tool in tools if tool.get("name") != name]
        return self.save_tools(tools)
    
    # 自动解题相关操作
    def save_auto_solve(self, auto_solve_data: Dict[str, Any]) -> Dict[str, Any]:
        """保存自动解题记录"""
        auto_solve_id = self._generate_id()
        timestamp = self._get_timestamp()
        
        auto_solve_record = {
            "id": auto_solve_id,
            "question_id": auto_solve_data.get("question_id"),
            "status": auto_solve_data.get("status", "pending"),
            "solve_method": auto_solve_data.get("solve_method"),
            "generated_code": auto_solve_data.get("generated_code"),
            "execution_result": auto_solve_data.get("execution_result"),
            "flag": auto_solve_data.get("flag"),
            "error_message": auto_solve_data.get("error_message"),
            "execution_time": auto_solve_data.get("execution_time", 0),
            "created_at": timestamp,
            "completed_at": auto_solve_data.get("completed_at")
        }
        
        # 创建auto_solve目录
        auto_solve_dir = self.data_root / "auto_solve"
        auto_solve_dir.mkdir(exist_ok=True)
        
        file_path = auto_solve_dir / f"auto_solve_{auto_solve_id}.json"
        if self._write_json_file(file_path, auto_solve_record):
            return auto_solve_record
        else:
            raise Exception("保存自动解题记录失败")
    
    def get_auto_solve(self, auto_solve_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取自动解题记录"""
        auto_solve_dir = self.data_root / "auto_solve"
        file_path = auto_solve_dir / f"auto_solve_{auto_solve_id}.json"
        return self._read_json_file(file_path)
    
    def get_auto_solves(self, question_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取自动解题记录列表"""
        auto_solve_dir = self.data_root / "auto_solve"
        if not auto_solve_dir.exists():
            return []
        
        auto_solves = []
        for file_path in sorted(auto_solve_dir.glob("auto_solve_*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            data = self._read_json_file(file_path)
            if data:
                if question_id is None or data.get("question_id") == question_id:
                    auto_solves.append(data)
                    if len(auto_solves) >= limit:
                        break
        
        return auto_solves
    
    def update_auto_solve(self, auto_solve_id: str, updates: Dict[str, Any]) -> bool:
        """更新自动解题记录"""
        auto_solve_dir = self.data_root / "auto_solve"
        file_path = auto_solve_dir / f"auto_solve_{auto_solve_id}.json"
        
        current_data = self._read_json_file(file_path)
        if not current_data:
            return False
        
        # 更新字段
        current_data.update(updates)
        
        # 如果是完成状态，添加完成时间
        if updates.get("status") in ["completed", "failed"] and not current_data.get("completed_at"):
            current_data["completed_at"] = self._get_timestamp()
        
        return self._write_json_file(file_path, current_data)
    
    def delete_auto_solve(self, auto_solve_id: str) -> bool:
        """删除自动解题记录"""
        auto_solve_dir = self.data_root / "auto_solve"
        file_path = auto_solve_dir / f"auto_solve_{auto_solve_id}.json"
        
        try:
            if file_path.exists():
                file_path.unlink()
                return True
        except Exception as e:
            print(f"删除自动解题记录失败 {file_path}: {e}")
        
        return False
    
    # 模板相关操作
    def save_templates(self, templates: List[Dict[str, Any]]) -> bool:
        """保存模板列表"""
        file_path = self.configs_dir / "solve_templates.json"
        return self._write_json_file(file_path, {"templates": templates})
    
    def get_templates(self, category: str = None) -> List[Dict[str, Any]]:
        """获取模板列表"""
        file_path = self.configs_dir / "solve_templates.json"
        data = self._read_json_file(file_path)
        
        if not data or "templates" not in data:
            return []
        
        templates = data["templates"]
        if category:
            templates = [template for template in templates if template.get("category") == category]
        
        # 只返回启用的模板
        templates = [template for template in templates if template.get("is_active", True)]
        
        return templates
    
    def get_template_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取模板"""
        templates = self.get_templates()
        for template in templates:
            if template.get("name") == name:
                return template
        return None
    
    def add_template(self, template: Dict[str, Any]) -> bool:
        """添加模板"""
        templates = self.get_templates()
        # 生成新的ID
        max_id = max([t.get('id', 0) for t in templates]) if templates else 0
        template['id'] = max_id + 1
        templates.append(template)
        return self.save_templates(templates)
    
    def update_template(self, name: str, updated_template: Dict[str, Any]) -> bool:
        """更新模板"""
        templates = self.get_templates()
        for i, template in enumerate(templates):
            if template.get("name") == name:
                templates[i] = updated_template
                return self.save_templates(templates)
        return False
    
    def delete_template(self, name: str) -> bool:
        """删除模板"""
        templates = self.get_templates()
        templates = [template for template in templates if template.get("name") != name]
        return self.save_templates(templates)
    
    def enable_template(self, name: str) -> bool:
        """启用模板"""
        templates = self.get_templates()
        for i, template in enumerate(templates):
            if template.get("name") == name:
                templates[i]["is_active"] = True
                return self.save_templates(templates)
        return False
    
    def disable_template(self, name: str) -> bool:
        """禁用模板"""
        templates = self.get_templates()
        for i, template in enumerate(templates):
            if template.get("name") == name:
                templates[i]["is_active"] = False
                return self.save_templates(templates)
        return False
    
    # 统计相关操作
    def get_stats(self) -> Dict[str, Any]:
        """获取统计数据"""
        stats = {
            "total_challenges": 0,
            "challenges_by_type": {},
            "total_history": 0,
            "cache_files": 0,
            "config_files": 0
        }
        
        # 统计题目数量
        for challenge_type in ["web", "pwn", "reverse", "crypto", "misc"]:
            type_dir = self.challenges_dir / challenge_type
            if type_dir.exists():
                count = len(list(type_dir.glob("*.json")))
                stats["challenges_by_type"][challenge_type] = count
                stats["total_challenges"] += count
        
        # 统计历史记录数量
        if self.history_dir.exists():
            stats["total_history"] = len(list(self.history_dir.glob("*.json")))
        
        # 统计缓存文件数量
        if self.cache_dir.exists():
            stats["cache_files"] = len(list(self.cache_dir.glob("*.json")))
        
        # 统计配置文件数量
        if self.configs_dir.exists():
            stats["config_files"] = len(list(self.configs_dir.glob("*.json")))
        
        return stats

    def save_template(self, template_data: Dict[str, Any]) -> bool:
        """保存解题模板"""
        try:
            templates = self.get_templates()
            template_id = template_data.get("id")
            
            if template_id:
                # 更新现有模板
                for i, template in enumerate(templates):
                    if template.get("id") == template_id:
                        templates[i] = template_data
                        break
            else:
                # 添加新模板
                template_data["id"] = str(uuid.uuid4())
                template_data["created_at"] = datetime.now().isoformat()
                templates.append(template_data)
            
            self._write_json_file(self.configs_dir / "solve_templates.json", {"templates": templates})
            return True
        except Exception as e:
            print(f"保存模板失败: {e}")
            return False

    def delete_template(self, template_id: str) -> bool:
        """删除解题模板"""
        try:
            templates = self.get_templates()
            templates = [t for t in templates if t.get("id") != template_id]
            self._write_json_file(self.configs_dir / "solve_templates.json", {"templates": templates})
            return True
        except Exception as e:
            print(f"删除模板失败: {e}")
            return False

    # 对话管理方法
    def save_conversation(self, conversation_data: Dict[str, Any]) -> bool:
        """保存对话数据"""
        try:
            conversations_dir = self.data_root / "conversations"
            conversations_dir.mkdir(exist_ok=True)
            
            conversation_id = conversation_data["id"]
            conversation_file = conversations_dir / f"{conversation_id}.json"
            
            self._write_json_file(conversation_file, conversation_data)
            return True
        except Exception as e:
            print(f"保存对话失败: {e}")
            return False

    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """获取对话数据"""
        try:
            conversations_dir = self.data_root / "conversations"
            conversation_file = conversations_dir / f"{conversation_id}.json"
            
            if conversation_file.exists():
                return self._read_json_file(conversation_file)
            return None
        except Exception as e:
            print(f"获取对话失败: {e}")
            return None

    def get_user_conversations(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取用户的对话列表"""
        try:
            conversations_dir = self.data_root / "conversations"
            if not conversations_dir.exists():
                return []
            
            conversations = []
            for filename in os.listdir(conversations_dir):
                if filename.endswith('.json'):
                    conversation_file = conversations_dir / filename
                    conversation = self._read_json_file(conversation_file)
                    if conversation and conversation.get("user_id") == user_id:
                        conversations.append(conversation)
            
            # 按更新时间排序
            conversations.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
            return conversations[:limit]
        except Exception as e:
            print(f"获取用户对话列表失败: {e}")
            return []

    def delete_conversation(self, conversation_id: str) -> bool:
        """删除对话"""
        try:
            conversations_dir = self.data_root / "conversations"
            conversation_file = conversations_dir / f"{conversation_id}.json"
            
            if conversation_file.exists():
                conversation_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"删除对话失败: {e}")
            return False

    def cleanup_expired_conversations(self, hours: int = 24) -> int:
        """清理过期的对话"""
        try:
            conversations_dir = self.data_root / "conversations"
            if not conversations_dir.exists():
                return 0
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            deleted_count = 0
            
            for filename in os.listdir(conversations_dir):
                if filename.endswith('.json'):
                    conversation_file = conversations_dir / filename
                    conversation = self._read_json_file(conversation_file)
                    
                    if conversation:
                        updated_at = datetime.fromisoformat(conversation.get("updated_at", "1970-01-01T00:00:00"))
                        if updated_at < cutoff_time:
                            conversation_file.unlink()
                            deleted_count += 1
            
            return deleted_count
        except Exception as e:
            print(f"清理过期对话失败: {e}")
            return 0

# 创建全局实例
data_service = DataService() 