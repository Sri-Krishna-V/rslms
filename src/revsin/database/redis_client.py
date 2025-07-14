"""
Redis client configuration for Upstash Redis
"""

import redis
import json
import logging
from typing import Optional, Any
from ..config import settings

logger = logging.getLogger(__name__)

# Redis client instance
redis_client = None


def get_redis_client() -> Optional[redis.Redis]:
    """Get Redis client instance"""
    global redis_client
    if redis_client is None:
        try:
            # Check if Redis URL is properly configured
            if not settings.redis_url or "hostname" in settings.redis_url or "port" in settings.redis_url:
                logger.warning("Redis URL not properly configured. Caching will be disabled.")
                return None
            
            redis_client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            # Test connection
            redis_client.ping()
            logger.info("Redis connection established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            logger.warning("Redis connection failed. Caching will be disabled.")
            redis_client = None
    return redis_client


class Cache:
    """Redis cache utility class"""
    
    def __init__(self):
        self.client = get_redis_client()
        self.default_expire = settings.cache_expire_time
        self.enabled = self.client is not None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set value in cache"""
        if not self.enabled:
            return False
        
        try:
            expire_time = expire or self.default_expire
            serialized_value = json.dumps(value, default=str)
            return self.client.setex(key, expire_time, serialized_value)
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.enabled:
            return False
        
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete keys matching pattern"""
        if not self.enabled:
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Error deleting cache pattern {pattern}: {e}")
            return 0
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.enabled:
            return False
        
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {e}")
            return False
    
    def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for key"""
        if not self.enabled:
            return False
        
        try:
            return bool(self.client.expire(key, seconds))
        except Exception as e:
            logger.error(f"Error setting expiration for key {key}: {e}")
            return False
    
    def flush_all(self) -> bool:
        """Clear all cache"""
        if not self.enabled:
            return False
        
        try:
            return self.client.flushall()
        except Exception as e:
            logger.error(f"Error flushing cache: {e}")
            return False


# Cache instance
cache = Cache()


def get_cache() -> Cache:
    """Get cache instance"""
    return cache


# Cache key generators
def get_user_cache_key(user_id: int) -> str:
    """Generate cache key for user"""
    return f"user:{user_id}"


def get_book_cache_key(book_id: int) -> str:
    """Generate cache key for book"""
    return f"book:{book_id}"


def get_books_list_cache_key(offset: int = 0, limit: int = 10, category: str = None) -> str:
    """Generate cache key for books list"""
    if category:
        return f"books:list:{category}:{offset}:{limit}"
    return f"books:list:{offset}:{limit}"


def get_user_loans_cache_key(user_id: int) -> str:
    """Generate cache key for user loans"""
    return f"user:{user_id}:loans"


def get_overdue_loans_cache_key() -> str:
    """Generate cache key for overdue loans"""
    return "loans:overdue"
