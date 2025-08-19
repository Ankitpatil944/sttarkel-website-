from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, Depends, Response
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import logging
import aiohttp

from scrapers.news_scraper import NewsScraper
from utils.cache_manager import CacheManager

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize cache manager
cache_manager = CacheManager()

@router.get("/news/latest")
async def get_latest_news(
    category: Optional[str] = Query(None, description="Filter by category: tech, programming, interview"),
    limit: int = Query(50, ge=1, le=100, description="Number of news items to return"),
    source: Optional[str] = Query(None, description="Filter by specific source"),
    use_cache: bool = Query(True, description="Use cached results if available")
):
    """
    Get latest news from all sources or filtered by category
    """
    try:
        # Check cache first
        cache_key = f"latest_news_{category}_{limit}_{source}"
        if use_cache:
            cached_data = cache_manager.get(cache_key)
            if cached_data:
                return {
                    "success": True,
                    "data": cached_data,
                    "cached": True,
                    "timestamp": datetime.now().isoformat()
                }

        # Scrape fresh data
        scraper = NewsScraper()
        news_items = await scraper.get_latest_news(category=category, limit=limit)
        
        # Filter by source if specified
        if source:
            news_items = [item for item in news_items if item.get('source_name') == source]
        
        # Cache the results
        cache_manager.set(cache_key, news_items, expire=1800)  # Cache for 30 minutes
        
        return {
            "success": True,
            "data": news_items,
            "cached": False,
            "count": len(news_items),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching latest news: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")

@router.get("/news/category/{category}")
async def get_news_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=100, description="Number of news items to return")
):
    """
    Get news filtered by specific category
    """
    try:
        valid_categories = ["tech", "programming", "interview"]
        if category not in valid_categories:
            raise HTTPException(status_code=400, detail=f"Invalid category. Must be one of: {valid_categories}")
        
        scraper = NewsScraper()
        news_items = await scraper.get_latest_news(category=category, limit=limit)
        
        return {
            "success": True,
            "data": news_items,
            "category": category,
            "count": len(news_items),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching news by category: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")

@router.get("/news/source/{source_name}")
async def get_news_by_source(
    source_name: str,
    limit: int = Query(50, ge=1, le=100, description="Number of news items to return")
):
    """
    Get news from a specific source
    """
    try:
        valid_sources = [
            "techcrunch", "hackernews", "dev_to", "leetcode_blog", 
            "geeksforgeeks", "stackoverflow_blog"
        ]
        if source_name not in valid_sources:
            raise HTTPException(status_code=400, detail=f"Invalid source. Must be one of: {valid_sources}")
        
        scraper = NewsScraper()
        all_news = await scraper.scrape_all_sources()
        
        news_items = all_news.get(source_name, [])
        news_items = news_items[:limit]
        
        return {
            "success": True,
            "data": news_items,
            "source": source_name,
            "count": len(news_items),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching news by source: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")

@router.get("/news/search")
async def search_news(
    query: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=100, description="Number of results to return")
):
    """
    Search news by keyword
    """
    try:
        scraper = NewsScraper()
        all_news = await scraper.get_latest_news(category=category, limit=200)  # Get more for searching
        
        # Simple keyword search
        query_lower = query.lower()
        filtered_news = []
        
        for news in all_news:
            title = news.get('title', '').lower()
            description = news.get('description', '').lower()
            
            if query_lower in title or query_lower in description:
                filtered_news.append(news)
        
        filtered_news = filtered_news[:limit]
        
        return {
            "success": True,
            "data": filtered_news,
            "query": query,
            "category": category,
            "count": len(filtered_news),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error searching news: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to search news: {str(e)}")

@router.get("/news/summary")
async def get_news_summary():
    """
    Get a summary of news from all sources
    """
    try:
        scraper = NewsScraper()
        all_news = await scraper.scrape_all_sources()
        
        summary = {
            "total_sources": len(all_news),
            "total_articles": sum(len(news_list) for news_list in all_news.values()),
            "sources": {}
        }
        
        for source, news_list in all_news.items():
            summary["sources"][source] = {
                "count": len(news_list),
                "categories": {}
            }
            
            # Count by category
            for news in news_list:
                category = news.get('category', 'unknown')
                if category not in summary["sources"][source]["categories"]:
                    summary["sources"][source]["categories"][category] = 0
                summary["sources"][source]["categories"][category] += 1
        
        return {
            "success": True,
            "data": summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting news summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get news summary: {str(e)}")

@router.post("/news/refresh")
async def refresh_news_cache(background_tasks: BackgroundTasks):
    """
    Manually refresh the news cache
    """
    try:
        # Add background task to refresh cache
        background_tasks.add_task(refresh_cache_task)
        
        return {
            "success": True,
            "message": "News cache refresh started in background",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error starting cache refresh: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start cache refresh: {str(e)}")

async def refresh_cache_task():
    """
    Background task to refresh news cache
    """
    try:
        logger.info("Starting background cache refresh...")
        scraper = NewsScraper()
        
        # Refresh all categories
        categories = ["tech", "programming", "interview"]
        for category in categories:
            news_items = await scraper.get_latest_news(category=category, limit=50)
            cache_key = f"latest_news_{category}_50_None"
            cache_manager.set(cache_key, news_items, expire=1800)
        
        logger.info("Background cache refresh completed")
        
    except Exception as e:
        logger.error(f"Error in background cache refresh: {e}")

@router.get("/news/trending")
async def get_trending_news(limit: int = Query(20, ge=1, le=50)):
    """
    Get trending news based on relevance and recency
    """
    try:
        scraper = NewsScraper()
        all_news = await scraper.get_latest_news(limit=100)
        
        # Simple trending algorithm: prioritize recent news with more keywords
        for news in all_news:
            title = news.get('title', '').lower()
            description = news.get('description', '').lower()
            
            # Count keyword matches
            coding_keywords = scraper.coding_keywords
            interview_keywords = scraper.interview_keywords
            
            coding_matches = sum(1 for keyword in coding_keywords if keyword.lower() in title + " " + description)
            interview_matches = sum(1 for keyword in interview_keywords if keyword.lower() in title + " " + description)
            
            news['relevance_score'] = coding_matches + interview_matches
        
        # Sort by relevance score and take top results
        trending_news = sorted(all_news, key=lambda x: x.get('relevance_score', 0), reverse=True)
        trending_news = trending_news[:limit]
        
        return {
            "success": True,
            "data": trending_news,
            "count": len(trending_news),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting trending news: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get trending news: {str(e)}")

@router.get("/proxy/image")
async def proxy_image(url: str = Query(..., description="URL of the image to proxy")):
    """Proxy image from external sources to avoid CORS issues"""
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid URL")
        
        # Fetch image from external source
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    content = await response.read()
                    content_type = response.headers.get('content-type', 'image/jpeg')
                    
                    # Return image with appropriate headers
                    return Response(
                        content=content,
                        media_type=content_type,
                        headers={
                            'Cache-Control': 'public, max-age=3600',  # Cache for 1 hour
                            'Access-Control-Allow-Origin': '*'
                        }
                    )
                else:
                    raise HTTPException(status_code=response.status, detail="Failed to fetch image")
                    
    except Exception as e:
        logger.error(f"Error proxying image {url}: {e}")
        raise HTTPException(status_code=500, detail="Failed to proxy image") 