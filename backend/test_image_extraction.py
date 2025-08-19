#!/usr/bin/env python3
"""
Test script to debug image extraction from news sources
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.news_scraper import NewsScraper

async def test_image_extraction():
    """Test image extraction from various news sources"""
    async with NewsScraper() as scraper:
        print("Testing TechCrunch image extraction...")
        try:
            techcrunch_news = await scraper.scrape_techcrunch()
            if techcrunch_news:
                print(f"Found {len(techcrunch_news)} TechCrunch articles")
                for i, news in enumerate(techcrunch_news[:3]):  # Show first 3
                    print(f"  {i+1}. {news['title'][:60]}...")
                    print(f"     Image: {news['image_url']}")
                    print(f"     URL: {news['url']}")
                    print()
            else:
                print("No TechCrunch articles found")
        except Exception as e:
            print(f"Error testing TechCrunch: {e}")
        
        print("\nTesting Dev.to image extraction...")
        try:
            devto_news = await scraper.scrape_dev_to()
            if devto_news:
                print(f"Found {len(devto_news)} Dev.to articles")
                for i, news in enumerate(devto_news[:3]):  # Show first 3
                    print(f"  {i+1}. {news['title'][:60]}...")
                    print(f"     Image: {news['image_url']}")
                    print(f"     URL: {news['url']}")
                    print()
            else:
                print("No Dev.to articles found")
        except Exception as e:
            print(f"Error testing Dev.to: {e}")

if __name__ == "__main__":
    asyncio.run(test_image_extraction())
