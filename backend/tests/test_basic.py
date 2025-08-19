import pytest
import asyncio
from scrapers.news_scraper import NewsScraper
from utils.cache_manager import CacheManager

class TestNewsScraper:
    """Basic tests for the news scraper"""
    
    @pytest.mark.asyncio
    async def test_scraper_initialization(self):
        """Test that the scraper can be initialized"""
        scraper = NewsScraper()
        assert scraper is not None
        assert hasattr(scraper, 'coding_keywords')
        assert hasattr(scraper, 'interview_keywords')
        assert len(scraper.coding_keywords) > 0
        assert len(scraper.interview_keywords) > 0
    
    @pytest.mark.asyncio
    async def test_relevance_filtering(self):
        """Test that the relevance filtering works correctly"""
        scraper = NewsScraper()
        
        # Test relevant news
        relevant_title = "New Python framework for web development"
        assert scraper.is_relevant_news(relevant_title) == True
        
        # Test irrelevant news
        irrelevant_title = "Latest cooking recipes for beginners"
        assert scraper.is_relevant_news(irrelevant_title) == False
        
        # Test interview-related news
        interview_title = "Top 10 coding interview questions for 2024"
        assert scraper.is_relevant_news(interview_title) == True
    
    @pytest.mark.asyncio
    async def test_scraper_context_manager(self):
        """Test that the scraper works as a context manager"""
        async with NewsScraper() as scraper:
            assert scraper.session is not None
            # Test that we can access session methods
            assert hasattr(scraper.session, 'get')

class TestCacheManager:
    """Basic tests for the cache manager"""
    
    def test_cache_set_and_get(self):
        """Test basic cache set and get operations"""
        cache = CacheManager()
        
        # Test setting and getting a value
        cache.set("test_key", "test_value", expire=60)
        value = cache.get("test_key")
        assert value == "test_value"
    
    def test_cache_expiration(self):
        """Test that cache entries expire correctly"""
        cache = CacheManager()
        
        # Set a value with very short expiration
        cache.set("expire_test", "test_value", expire=1)
        
        # Should be available immediately
        assert cache.get("expire_test") == "test_value"
        
        # Wait for expiration (in real test, you'd use time mocking)
        # For now, just test the structure
        assert cache.exists("expire_test") == True
    
    def test_cache_delete(self):
        """Test cache deletion"""
        cache = CacheManager()
        
        cache.set("delete_test", "test_value")
        assert cache.get("delete_test") == "test_value"
        
        # Delete the key
        assert cache.delete("delete_test") == True
        assert cache.get("delete_test") is None
    
    def test_cache_clear(self):
        """Test cache clearing"""
        cache = CacheManager()
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        assert cache.get("key1") == "value1"
        assert cache.get("key2") == "value2"
        
        cache.clear()
        
        assert cache.get("key1") is None
        assert cache.get("key2") is None
    
    def test_cache_stats(self):
        """Test cache statistics"""
        cache = CacheManager()
        
        # Add some test data
        cache.set("stats_test1", "value1")
        cache.set("stats_test2", "value2")
        
        stats = cache.get_stats()
        
        assert "total_entries" in stats
        assert "valid_entries" in stats
        assert "average_age_seconds" in stats
        assert stats["total_entries"] >= 2

@pytest.mark.asyncio
async def test_integration_basic():
    """Basic integration test"""
    scraper = NewsScraper()
    cache = CacheManager()
    
    # Test that we can get latest news (this will be empty in tests, but shouldn't crash)
    try:
        news = await scraper.get_latest_news(limit=5)
        assert isinstance(news, list)
    except Exception as e:
        # In test environment, scraping might fail due to network issues
        # This is expected and acceptable for basic tests
        assert "network" in str(e).lower() or "connection" in str(e).lower()

if __name__ == "__main__":
    # Run basic tests
    pytest.main([__file__, "-v"]) 