import hashlib
import json
import time
from typing import Optional, Any, Dict
from logger import get_logger
from config import config

class MemoryCache:
    """内存缓存实现"""
    
    def __init__(self, ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
        self.logger = get_logger("cache")
        self.hit_count = 0
        self.miss_count = 0
    
    def _is_expired(self, item: Dict[str, Any]) -> bool:
        """检查缓存项是否过期"""
        return time.time() - item["timestamp"] > self.ttl
    
    def _cleanup_expired(self):
        """清理过期的缓存项"""
        current_time = time.time()
        expired_keys = [
            key for key, item in self.cache.items()
            if current_time - item["timestamp"] > self.ttl
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self.logger.info(f"清理了 {len(expired_keys)} 个过期缓存项")
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if not config.ENABLE_CACHE:
            return None
        
        self._cleanup_expired()
        
        if key in self.cache:
            item = self.cache[key]
            if not self._is_expired(item):
                self.hit_count += 1
                return item["value"]
            else:
                # 过期了，删除
                del self.cache[key]
        
        self.miss_count += 1
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存值"""
        if not config.ENABLE_CACHE:
            return
        
        self.cache[key] = {
            "value": value,
            "timestamp": time.time()
        }
    
    def delete(self, key: str):
        """删除缓存项"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """清空所有缓存"""
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0
        self.logger.info("缓存已清空")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "total_items": len(self.cache),
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": round(hit_rate, 2),
            "total_requests": total_requests
        }

class AIResponseCache:
    """AI响应专用缓存"""
    
    def __init__(self, cache: MemoryCache = None):
        self.cache = cache or MemoryCache(ttl=config.CACHE_TTL)
        self.logger = get_logger("ai_cache")
    
    def _generate_cache_key(self, description: str, question_type: str, provider: str) -> str:
        """生成缓存键"""
        # 使用内容哈希作为键，确保相同内容能复用缓存
        content = f"{description}|{question_type}|{provider}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def get_cached_response(self, description: str, question_type: str, provider: str) -> Optional[str]:
        """获取缓存的AI响应"""
        cache_key = self._generate_cache_key(description, question_type, provider)
        cached_response = self.cache.get(cache_key)
        
        if cached_response:
            self.logger.info(f"AI响应缓存命中，提供者: {provider}, 类型: {question_type}")
        
        return cached_response
    
    def cache_response(self, description: str, question_type: str, provider: str, response: str):
        """缓存AI响应"""
        cache_key = self._generate_cache_key(description, question_type, provider)
        self.cache.set(cache_key, response)
        
        self.logger.info(f"AI响应已缓存，提供者: {provider}, 类型: {question_type}")
    
    def invalidate_provider_cache(self, provider: str):
        """清空特定提供者的缓存"""
        # 这是一个简化实现，实际中可能需要更复杂的键管理
        self.cache.clear()
        self.logger.info(f"已清空提供者 {provider} 的缓存")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        return self.cache.get_stats()

# 全局缓存实例
memory_cache = MemoryCache(ttl=config.CACHE_TTL)
ai_response_cache = AIResponseCache(memory_cache) 