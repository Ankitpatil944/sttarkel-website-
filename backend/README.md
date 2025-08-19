# Sttarkel News Scraper Backend

A real-time news scraper API built with FastAPI that fetches and filters news related to coding languages and student interview preparation from multiple sources.

## 🚀 Features

- **Multi-source News Scraping**: Fetches news from TechCrunch, Hacker News, Dev.to, LeetCode Blog, GeeksforGeeks, and Stack Overflow Blog
- **Smart Content Filtering**: Automatically filters news based on coding and interview-related keywords
- **Caching System**: In-memory caching to improve performance and reduce API calls
- **RESTful API**: Clean and well-documented API endpoints
- **Real-time Updates**: Background tasks for cache refresh
- **CORS Support**: Configured for frontend integration
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

### Option 1: Using the startup script
```bash
python start.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using the main module
```bash
python main.py
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## 📚 API Endpoints

### Core Endpoints

#### 1. Get Latest News
```
GET /api/v1/news/latest
```
**Parameters:**
- `category` (optional): Filter by category (`tech`, `programming`, `interview`)
- `limit` (optional): Number of news items (1-100, default: 50)
- `source` (optional): Filter by specific source
- `use_cache` (optional): Use cached results (default: true)

**Example:**
```bash
curl "http://localhost:8000/api/v1/news/latest?category=programming&limit=20"
```

#### 2. Get News by Category
```
GET /api/v1/news/category/{category}
```
**Categories:** `tech`, `programming`, `interview`

**Example:**
```bash
curl "http://localhost:8000/api/v1/news/category/interview?limit=30"
```

#### 3. Get News by Source
```
GET /api/v1/news/source/{source_name}
```
**Sources:** `techcrunch`, `hackernews`, `dev_to`, `leetcode_blog`, `geeksforgeeks`, `stackoverflow_blog`

**Example:**
```bash
curl "http://localhost:8000/api/v1/news/source/hackernews?limit=25"
```

#### 4. Search News
```
GET /api/v1/news/search
```
**Parameters:**
- `query` (required): Search keyword
- `category` (optional): Filter by category
- `limit` (optional): Number of results (1-100, default: 50)

**Example:**
```bash
curl "http://localhost:8000/api/v1/news/search?query=python&category=programming"
```

#### 5. Get Trending News
```
GET /api/v1/news/trending
```
**Parameters:**
- `limit` (optional): Number of trending items (1-50, default: 20)

**Example:**
```bash
curl "http://localhost:8000/api/v1/news/trending?limit=15"
```

#### 6. Get News Summary
```
GET /api/v1/news/summary
```
Returns statistics about news from all sources.

#### 7. Refresh News Cache
```
POST /api/v1/news/refresh
```
Manually triggers a background cache refresh.

### Utility Endpoints

#### Health Check
```
GET /health
```

#### Get News Sources
```
GET /api/v1/news/sources
```

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file in the backend directory:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Cache Configuration
CACHE_DEFAULT_TTL=1800
CACHE_CLEANUP_INTERVAL=3600

# Scraper Configuration
SCRAPER_TIMEOUT=30
SCRAPER_MAX_RETRIES=3
SCRAPER_DELAY_MIN=1.0
SCRAPER_DELAY_MAX=3.0

# Logging
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## 📊 News Sources

The scraper fetches news from the following sources:

| Source | Category | Description |
|--------|----------|-------------|
| TechCrunch | Tech | Latest technology news and startup information |
| Hacker News | Tech | Social news website focusing on computer science |
| Dev.to | Programming | Developer community platform |
| LeetCode Blog | Interview | Interview preparation and coding challenges |
| GeeksforGeeks | Interview | Computer science portal for geeks |
| Stack Overflow Blog | Programming | Programming and developer community blog |

## 🎯 Content Filtering

The scraper automatically filters news based on relevant keywords:

### Coding Keywords
- Programming languages: Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, Kotlin, Swift
- Frameworks: React, Angular, Vue, Node.js, Django, Flask, Spring, Laravel, Express
- Technologies: Docker, Kubernetes, AWS, Azure, GCP, Machine Learning, AI, Blockchain, Web3
- And many more...

### Interview Keywords
- Interview types: Coding interview, Technical interview, Behavioral interview
- Platforms: LeetCode, HackerRank, Codeforces
- Topics: Data structures, Algorithms, System design, Resume, Career
- And many more...

## 🏗️ Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration settings
├── start.py               # Startup script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── api/
│   ├── __init__.py
│   └── news_routes.py    # API route definitions
├── scrapers/
│   ├── __init__.py
│   └── news_scraper.py   # News scraping logic
├── utils/
│   ├── __init__.py
│   └── cache_manager.py  # Caching utilities
└── tests/
    └── __init__.py       # Test files (to be added)
```

## 🧪 Testing

To run tests (when implemented):
```bash
pytest tests/
```

## 🔍 Monitoring and Logging

The application includes comprehensive logging:
- Request/response logging
- Scraper performance monitoring
- Error tracking
- Cache hit/miss statistics

Logs are output to the console and can be configured via the `LOG_LEVEL` environment variable.

## 🚀 Deployment

### Development
```bash
python start.py
```

### Production
```bash
# Set environment variables
export DEBUG=False
export LOG_LEVEL=WARNING

# Run with production settings
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Future Enhancement)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is part of the Sttarkel website backend.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the backend directory and have activated the virtual environment
2. **Port Already in Use**: Change the port in the configuration or kill the process using the port
3. **Scraping Failures**: Some websites may block automated requests. The scraper includes retry logic and delays
4. **Memory Issues**: The cache is in-memory. For production, consider using Redis

### Getting Help

- Check the logs for detailed error messages
- Verify your internet connection
- Ensure all dependencies are installed correctly
- Check the API documentation at `/docs` for endpoint details

## 🔮 Future Enhancements

- [ ] Database integration for persistent storage
- [ ] Redis caching for production
- [ ] User authentication and personalization
- [ ] Email notifications for new articles
- [ ] Advanced search with filters
- [ ] News sentiment analysis
- [ ] RSS feed generation
- [ ] Webhook support for real-time updates 