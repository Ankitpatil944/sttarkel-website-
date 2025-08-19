import time
from typing import Any, Optional, Dict
import threading
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        
    def set(self, key: str, value: Any, expire: int = 3600) -> None:
        """
        Set a value in cache with expiration time in seconds
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds (default: 1 hour)
        """
        try:
            with self._lock:
                self._cache[key] = {
                    'value': value,
                    'expire_at': time.time() + expire,
                    'created_at': time.time()
                }
                logger.debug(f"Cached data for key: {key}, expires in {expire} seconds")
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        try:
            with self._lock:
                if key not in self._cache:
                    return None
                
                cache_entry = self._cache[key]
                
                # Check if expired
                if time.time() > cache_entry['expire_at']:
                    del self._cache[key]
                    logger.debug(f"Cache expired for key: {key}")
                    return None
                
                logger.debug(f"Cache hit for key: {key}")
                return cache_entry['value']
                
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if key was deleted, False if not found
        """
        try:
            with self._lock:
                if key in self._cache:
                    del self._cache[key]
                    logger.debug(f"Deleted cache key: {key}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    def clear(self) -> None:
        """Clear all cached data"""
        try:
            with self._lock:
                self._cache.clear()
                logger.info("Cache cleared")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    def clear_expired(self) -> int:
        """
        Clear expired entries from cache
        
        Returns:
            Number of expired entries removed
        """
        try:
            count = 0
            current_time = time.time()
            
            with self._lock:
                expired_keys = [
                    key for key, entry in self._cache.items()
                    if current_time > entry['expire_at']
                ]
                
                for key in expired_keys:
                    del self._cache[key]
                    count += 1
                
                if count > 0:
                    logger.info(f"Cleared {count} expired cache entries")
                
                return count
                
        except Exception as e:
            logger.error(f"Error clearing expired cache entries: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        try:
            with self._lock:
                current_time = time.time()
                total_entries = len(self._cache)
                expired_entries = sum(
                    1 for entry in self._cache.values()
                    if current_time > entry['expire_at']
                )
                
                # Calculate average age
                if total_entries > 0:
                    avg_age = sum(
                        current_time - entry['created_at']
                        for entry in self._cache.values()
                    ) / total_entries
                else:
                    avg_age = 0
                
                return {
                    'total_entries': total_entries,
                    'expired_entries': expired_entries,
                    'valid_entries': total_entries - expired_entries,
                    'average_age_seconds': round(avg_age, 2)
                }
                
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache and is not expired
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists and is valid, False otherwise
        """
        return self.get(key) is not None
    
    def get_ttl(self, key: str) -> Optional[int]:
        """
        Get time to live for a cache key
        
        Args:
            key: Cache key
            
        Returns:
            TTL in seconds or None if key doesn't exist
        """
        try:
            with self._lock:
                if key not in self._cache:
                    return None
                
                cache_entry = self._cache[key]
                ttl = cache_entry['expire_at'] - time.time()
                
                return max(0, int(ttl)) if ttl > 0 else None
                
        except Exception as e:
            logger.error(f"Error getting TTL for key {key}: {e}")
            return None 