// API service for connecting to the backend news scraper

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface NewsItem {
  title: string;
  description: string;
  url: string;
  published_date: string;
  source: string;
  category: string;
  source_name?: string;
  author?: string;
  relevance_score?: number;
  image_url?: string;
}

export interface NewsResponse {
  success: boolean;
  data: NewsItem[];
  cached?: boolean;
  count?: number;
  timestamp: string;
}

export interface NewsSummary {
  total_sources: number;
  total_articles: number;
  sources: Record<string, {
    count: number;
    categories: Record<string, number>;
  }>;
}

export interface NewsSource {
  name: string;
  url: string;
  category: string;
  description: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async makeRequest<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Get latest news with optional filtering
  async getLatestNews(params?: {
    category?: 'tech' | 'programming' | 'interview';
    limit?: number;
    source?: string;
    use_cache?: boolean;
  }): Promise<NewsResponse> {
    const searchParams = new URLSearchParams();
    
    if (params?.category) searchParams.append('category', params.category);
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.source) searchParams.append('source', params.source);
    if (params?.use_cache !== undefined) searchParams.append('use_cache', params.use_cache.toString());

    const endpoint = `/api/v1/news/latest${searchParams.toString() ? `?${searchParams.toString()}` : ''}`;
    return this.makeRequest<NewsResponse>(endpoint);
  }

  // Get news by category
  async getNewsByCategory(category: 'tech' | 'programming' | 'interview', limit: number = 50): Promise<NewsResponse> {
    return this.makeRequest<NewsResponse>(`/api/v1/news/category/${category}?limit=${limit}`);
  }

  // Get news by source
  async getNewsBySource(source: string, limit: number = 50): Promise<NewsResponse> {
    return this.makeRequest<NewsResponse>(`/api/v1/news/source/${source}?limit=${limit}`);
  }

  // Search news
  async searchNews(query: string, params?: {
    category?: 'tech' | 'programming' | 'interview';
    limit?: number;
  }): Promise<NewsResponse> {
    const searchParams = new URLSearchParams({ query });
    
    if (params?.category) searchParams.append('category', params.category);
    if (params?.limit) searchParams.append('limit', params.limit.toString());

    return this.makeRequest<NewsResponse>(`/api/v1/news/search?${searchParams.toString()}`);
  }

  // Get trending news
  async getTrendingNews(limit: number = 20): Promise<NewsResponse> {
    return this.makeRequest<NewsResponse>(`/api/v1/news/trending?limit=${limit}`);
  }

  // Get news summary
  async getNewsSummary(): Promise<{ success: boolean; data: NewsSummary; timestamp: string }> {
    return this.makeRequest(`/api/v1/news/summary`);
  }

  // Get news sources
  async getNewsSources(): Promise<{ sources: NewsSource[] }> {
    return this.makeRequest(`/api/v1/news/sources`);
  }

  // Refresh news cache
  async refreshNewsCache(): Promise<{ success: boolean; message: string; timestamp: string }> {
    return this.makeRequest(`/api/v1/news/refresh`, { method: 'POST' });
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.makeRequest(`/health`);
  }
}

// Create and export a singleton instance
export const apiService = new ApiService();

// Export the class for testing or custom instances
export default ApiService; 