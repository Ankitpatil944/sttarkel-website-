from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
import asyncio
from datetime import datetime, timedelta

from api.news_routes import router as news_router
from api.mentor_routes import router as mentor_router
from scrapers.news_scraper import NewsScraper
from utils.cache_manager import CacheManager

app = FastAPI(
    title="Sttarkel News Scraper API",
    description="Real-time news scraper for coding languages and interview preparation",
    version="1.0.0"
)

# CORS middleware - Updated to handle preflight requests properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:4173",  # Vite preview
        "http://127.0.0.1:4173",  # Vite preview
        "*"  # Allow all origins for development
    ],
    allow_credentials=False,  # Changed to False to avoid CORS issues
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)

# Initialize cache manager
cache_manager = CacheManager()

# Include routers
app.include_router(news_router, prefix="/api/v1")
app.include_router(mentor_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Sttarkel News Scraper API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/v1/news/sources")
async def get_news_sources():
    """Get list of available news sources"""
    sources = [
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com",
            "category": "tech",
            "description": "Latest technology news and startup information"
        },
        {
            "name": "Hacker News",
            "url": "https://news.ycombinator.com",
            "category": "tech",
            "description": "Social news website focusing on computer science and entrepreneurship"
        },
        {
            "name": "Stack Overflow Blog",
            "url": "https://stackoverflow.blog",
            "category": "programming",
            "description": "Programming and developer community blog"
        },
        {
            "name": "Dev.to",
            "url": "https://dev.to",
            "category": "programming",
            "description": "Developer community platform"
        },
        {
            "name": "Medium Programming",
            "url": "https://medium.com/topic/programming",
            "category": "programming",
            "description": "Programming articles and tutorials"
        },
        {
            "name": "LeetCode Blog",
            "url": "https://leetcode.com/blog",
            "category": "interview",
            "description": "Interview preparation and coding challenges"
        },
        {
            "name": "GeeksforGeeks",
            "url": "https://www.geeksforgeeks.org",
            "category": "interview",
            "description": "Computer science portal for geeks"
        }
    ]
    return {"sources": sources}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 