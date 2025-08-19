#!/usr/bin/env python3
"""
Simple test script to verify the news scraper functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from scrapers.news_scraper import NewsScraper
from utils.cache_manager import CacheManager

async def test_scraper():
    """Test the news scraper functionality"""
    print("🧪 Testing News Scraper...")
    print("=" * 50)
    
    # Test cache manager
    print("📦 Testing Cache Manager...")
    cache = CacheManager()
    cache.set("test", "Hello World", expire=60)
    result = cache.get("test")
    print(f"✅ Cache test: {result}")
    
    # Test scraper initialization
    print("\n🔍 Testing Scraper Initialization...")
    scraper = NewsScraper()
    print(f"✅ Scraper initialized with {len(scraper.coding_keywords)} coding keywords")
    print(f"✅ Scraper initialized with {len(scraper.interview_keywords)} interview keywords")
    
    # Test relevance filtering
    print("\n🎯 Testing Relevance Filtering...")
    test_titles = [
        "New Python framework for web development",
        "Latest cooking recipes for beginners",
        "Top 10 coding interview questions for 2024",
        "React vs Angular: Which to choose in 2024",
        "How to make the perfect pasta"
    ]
    
    for title in test_titles:
        is_relevant = scraper.is_relevant_news(title)
        status = "✅" if is_relevant else "❌"
        print(f"{status} '{title}' -> {'Relevant' if is_relevant else 'Not Relevant'}")
    
    # Test actual scraping (this might take some time)
    print("\n🌐 Testing News Scraping...")
    print("⚠️  This might take a few minutes and requires internet connection...")
    
    try:
        async with scraper:
            print("📡 Testing TechCrunch scraping...")
            techcrunch_news = await scraper.scrape_techcrunch()
            print(f"✅ Found {len(techcrunch_news)} relevant articles from TechCrunch")
            
            if techcrunch_news:
                print("📰 Sample article:")
                sample = techcrunch_news[0]
                print(f"   Title: {sample['title']}")
                print(f"   Source: {sample['source']}")
                print(f"   Category: {sample['category']}")
            
            print("\n📡 Testing Hacker News scraping...")
            hn_news = await scraper.scrape_hackernews()
            print(f"✅ Found {len(hn_news)} relevant articles from Hacker News")
            
            if hn_news:
                print("📰 Sample article:")
                sample = hn_news[0]
                print(f"   Title: {sample['title']}")
                print(f"   Source: {sample['source']}")
                print(f"   Category: {sample['category']}")
            
            print("\n📡 Testing Dev.to scraping...")
            dev_news = await scraper.scrape_dev_to()
            print(f"✅ Found {len(dev_news)} relevant articles from Dev.to")
            
            if dev_news:
                print("📰 Sample article:")
                sample = dev_news[0]
                print(f"   Title: {sample['title']}")
                print(f"   Source: {sample['source']}")
                print(f"   Category: {sample['category']}")
            
            # Test getting latest news
            print("\n📡 Testing Latest News Aggregation...")
            latest_news = await scraper.get_latest_news(limit=10)
            print(f"✅ Found {len(latest_news)} total relevant articles")
            
            # Test category filtering
            print("\n📡 Testing Category Filtering...")
            programming_news = await scraper.get_latest_news(category="programming", limit=5)
            print(f"✅ Found {len(programming_news)} programming articles")
            
            interview_news = await scraper.get_latest_news(category="interview", limit=5)
            print(f"✅ Found {len(interview_news)} interview articles")
            
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        print("💡 This might be due to network issues or website blocking")
        print("💡 The scraper is designed to handle such issues gracefully")
    
    print("\n" + "=" * 50)
    print("🎉 Scraper test completed!")
    print("💡 If you see errors, they're likely due to network issues or website blocking")
    print("💡 The scraper includes retry logic and error handling for production use")

def test_cache_manager():
    """Test cache manager functionality"""
    print("📦 Testing Cache Manager...")
    cache = CacheManager()
    
    # Test basic operations
    cache.set("key1", "value1", expire=60)
    cache.set("key2", "value2", expire=60)
    
    assert cache.get("key1") == "value1"
    assert cache.get("key2") == "value2"
    
    # Test deletion
    cache.delete("key1")
    assert cache.get("key1") is None
    
    # Test stats
    stats = cache.get_stats()
    assert "total_entries" in stats
    assert "valid_entries" in stats
    
    print("✅ Cache manager tests passed!")

if __name__ == "__main__":
    print("🚀 Starting News Scraper Tests...")
    
    # Test cache manager
    test_cache_manager()
    
    # Test scraper
    asyncio.run(test_scraper())
    
    print("\n🎯 All tests completed!")
    print("📚 Check the README.md for more information about the API endpoints")
    print("🌐 The API will be available at http://localhost:8000 when you run the server") 
 