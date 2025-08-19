# Frontend-Backend Integration Guide

This guide explains how the frontend and backend are connected for the Sttarkel News Scraper application.

## 🏗️ Architecture Overview

```
Frontend (React + TypeScript) ←→ Backend (FastAPI + Python)
     ↓                              ↓
  News Display                    News Scraping
  Search & Filter                 API Endpoints
  Real-time Updates               Caching System
```

## 🚀 Quick Start

### 1. Start the Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python start.py
```

The backend will be available at: http://localhost:8000

### 2. Start the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at: http://localhost:5173

### 3. Test the Connection

Open your browser console and run:
```javascript
// Test backend connection
import { testBackendConnection } from './src/utils/testConnection';
testBackendConnection();
```

## 📡 API Integration

### API Service (`src/lib/api.ts`)

The frontend uses a centralized API service to communicate with the backend:

```typescript
import { apiService } from '@/lib/api';

// Get latest news
const news = await apiService.getLatestNews({ limit: 20 });

// Search news
const results = await apiService.searchNews('python');

// Get trending news
const trending = await apiService.getTrendingNews(10);
```

### React Query Hooks (`src/hooks/useNews.ts`)

React Query hooks provide caching, loading states, and error handling:

```typescript
import { useLatestNews, useSearchNews } from '@/hooks/useNews';

// In your component
const { data: news, isLoading, error } = useLatestNews({ limit: 20 });
const { data: searchResults } = useSearchNews('python');
```

## 🎯 Key Features

### 1. Real-time News Display
- **Backend**: Scrapes news from multiple sources (TechCrunch, Hacker News, Dev.to, etc.)
- **Frontend**: Displays news in beautiful cards with loading states

### 2. Smart Search & Filtering
- **Backend**: Keyword-based search with category filtering
- **Frontend**: Real-time search with debounced input

### 3. Caching System
- **Backend**: In-memory caching (30-minute TTL)
- **Frontend**: React Query caching with automatic invalidation

### 4. Error Handling
- **Backend**: Comprehensive error handling with detailed logging
- **Frontend**: User-friendly error messages and retry mechanisms

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
# API Configuration
VITE_API_URL=http://localhost:8000

# Development Configuration
VITE_DEV_MODE=true
VITE_ENABLE_LOGGING=true
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/news/latest` | GET | Latest news with filtering |
| `/api/v1/news/category/{category}` | GET | News by category |
| `/api/v1/news/search` | GET | Search news by keyword |
| `/api/v1/news/trending` | GET | Trending news |
| `/api/v1/news/summary` | GET | News statistics |
| `/api/v1/news/refresh` | POST | Refresh cache |

## 🎨 UI Components

### NewsCard Component
```typescript
import NewsCard from '@/components/NewsCard';

<NewsCard 
  news={newsItem} 
  variant="featured" 
  showSource={true} 
  showCategory={true} 
/>
```

### Loading States
```typescript
import NewsCardSkeleton from '@/components/NewsCardSkeleton';

{isLoading ? (
  <NewsCardSkeleton variant="featured" />
) : (
  <NewsCard news={news} variant="featured" />
)}
```

## 🔍 Debugging

### Backend Debugging
```bash
# Check backend logs
cd backend
python start.py

# Test scraper manually
python test_scraper.py
```

### Frontend Debugging
```javascript
// Test API connection
import { testBackendConnection } from '@/utils/testConnection';
testBackendConnection();

// Check React Query cache
import { useQueryClient } from '@tanstack/react-query';
const queryClient = useQueryClient();
console.log(queryClient.getQueryCache().getAll());
```

## 🚀 Deployment

### Development
```bash
# Backend
cd backend && python start.py

# Frontend
cd frontend && npm run dev
```

### Production
```bash
# Backend
cd backend
export DEBUG=False
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend
cd frontend
npm run build
```

## 🔄 Data Flow

1. **User Interaction**: User searches or filters news
2. **Frontend**: React Query hook triggers API call
3. **Backend**: FastAPI endpoint processes request
4. **Scraper**: Fetches fresh data from news sources
5. **Cache**: Stores results for future requests
6. **Response**: Returns formatted data to frontend
7. **Display**: React component renders news cards

## 🛠️ Troubleshooting

### Common Issues

1. **Backend Not Starting**
   ```bash
   # Check Python version
   python --version  # Should be 3.8+
   
   # Check dependencies
   pip install -r requirements.txt
   ```

2. **Frontend Build Errors**
   ```bash
   # Clear cache
   npm run clean
   
   # Reinstall dependencies
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **API Connection Issues**
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   
   # Check CORS configuration
   # Ensure frontend origin is in backend CORS settings
   ```

4. **No News Data**
   ```bash
   # Test scraper manually
   cd backend && python test_scraper.py
   
   # Check network connectivity
   # Some websites may block automated requests
   ```

## 📈 Performance Optimization

### Backend
- Caching reduces API calls to news sources
- Concurrent scraping improves response times
- Background tasks for cache refresh

### Frontend
- React Query provides intelligent caching
- Skeleton loading states improve perceived performance
- Debounced search reduces API calls

## 🔮 Future Enhancements

- [ ] Real-time notifications for new articles
- [ ] User preferences and personalization
- [ ] Advanced filtering and sorting
- [ ] Offline support with service workers
- [ ] Analytics and usage tracking
- [ ] Social sharing features

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Query Documentation](https://tanstack.com/query/latest)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Test the connection using the provided utilities
4. Create an issue with detailed information 