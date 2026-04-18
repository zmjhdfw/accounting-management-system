"""
缓存管理模块
"""
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, Optional


class CacheItem:
    """缓存项"""
    
    def __init__(self, value: Any, ttl: Optional[int] = None):
        self.value = value
        self.created_at = datetime.now()
        self.ttl = ttl  # 生存时间（秒）
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.ttl is None:
            return False
        return datetime.now() > self.created_at + timedelta(seconds=self.ttl)


class CacheManager:
    """缓存管理器"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'cache'):
            self.cache: Dict[str, CacheItem] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key not in self.cache:
            return None
        
        item = self.cache[key]
        if item.is_expired():
            del self.cache[key]
            return None
        
        return item.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """设置缓存值"""
        self.cache[key] = CacheItem(value, ttl)
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
    
    def clear_expired(self):
        """清除过期缓存"""
        expired_keys = [
            key for key, item in self.cache.items()
            if item.is_expired()
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def invalidate_by_prefix(self, prefix: str):
        """按前缀失效缓存"""
        keys_to_delete = [
            key for key in self.cache.keys()
            if key.startswith(prefix)
        ]
        for key in keys_to_delete:
            del self.cache[key]
    
    def get_stats(self) -> Dict:
        """获取缓存统计信息"""
        total = len(self.cache)
        expired = sum(1 for item in self.cache.values() if item.is_expired())
        return {
            'total': total,
            'active': total - expired,
            'expired': expired
        }


# 全局缓存管理器实例
cache_manager = CacheManager()


def cached(ttl: Optional[int] = None, key_prefix: str = ''):
    """缓存装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 尝试从缓存获取
            cached_value = cache_manager.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
