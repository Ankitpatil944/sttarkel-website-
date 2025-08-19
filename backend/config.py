import os
from typing import List

class Config:
    """Application configuration"""
    
    # API Configuration
    API_TITLE = "Sttarkel News Scraper API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "Real-time news scraper for coding languages and interview preparation"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS Configuration
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Cache Configuration
    CACHE_DEFAULT_TTL = int(os.getenv("CACHE_DEFAULT_TTL", 1800))  # 30 minutes
    CACHE_CLEANUP_INTERVAL = int(os.getenv("CACHE_CLEANUP_INTERVAL", 3600))  # 1 hour
    
    # Scraper Configuration
    SCRAPER_TIMEOUT = int(os.getenv("SCRAPER_TIMEOUT", 30))  # seconds
    SCRAPER_MAX_RETRIES = int(os.getenv("SCRAPER_MAX_RETRIES", 3))
    SCRAPER_DELAY_MIN = float(os.getenv("SCRAPER_DELAY_MIN", 1.0))  # seconds
    SCRAPER_DELAY_MAX = float(os.getenv("SCRAPER_DELAY_MAX", 3.0))  # seconds
    
    # News Sources Configuration
    NEWS_SOURCES = {
        "techcrunch": {
            "url": "https://techcrunch.com/feed/",
            "enabled": True,
            "category": "tech"
        },
        "hackernews": {
            "url": "https://news.ycombinator.com/",
            "enabled": True,
            "category": "tech"
        },
        "dev_to": {
            "url": "https://dev.to/t/programming",
            "enabled": True,
            "category": "programming"
        },
        "leetcode_blog": {
            "url": "https://leetcode.com/blog/",
            "enabled": True,
            "category": "interview"
        },
        "geeksforgeeks": {
            "url": "https://www.geeksforgeeks.org/",
            "enabled": True,
            "category": "interview"
        },
        "stackoverflow_blog": {
            "url": "https://stackoverflow.blog/",
            "enabled": True,
            "category": "programming"
        }
    }
    
    # Keywords for filtering relevant news
    CODING_KEYWORDS = [
        'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust', 'kotlin', 'swift',
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'laravel', 'express',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'machine learning', 'ai', 'artificial intelligence',
        'data science', 'blockchain', 'web3', 'cybersecurity', 'devops', 'git', 'github',
        'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
        'microservices', 'api', 'rest', 'graphql', 'websocket', 'serverless'
    ]
    
    INTERVIEW_KEYWORDS = [
        'interview', 'coding interview', 'technical interview', 'leetcode', 'hackerrank', 'codeforces',
        'data structures', 'algorithms', 'system design', 'behavioral interview', 'resume', 'career',
        'job search', 'placement', 'campus recruitment', 'internship', 'software engineer', 'developer',
        'array', 'linked list', 'stack', 'queue', 'tree', 'graph', 'hash table', 'binary search',
        'dynamic programming', 'recursion', 'sorting', 'searching', 'complexity', 'big o notation'
    ]
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 100))  # requests per minute
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))  # seconds

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    CACHE_DEFAULT_TTL = 3600  # 1 hour

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    CACHE_DEFAULT_TTL = 60  # 1 minute for testing

# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")
    
    return config.get(config_name, config["default"])() 