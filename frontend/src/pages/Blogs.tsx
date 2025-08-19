import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { motion } from 'framer-motion';
import './OutlinedText.css';
import { 
  Search, 
  Calendar, 
  Clock, 
  User, 
  ArrowRight,
  TrendingUp,
  BookOpen,
  Lightbulb,
  Briefcase,
  Users,
  Sparkles,
  RefreshCw,
  AlertCircle,
  Filter
} from "lucide-react";
import Footer from "@/components/Footer";
import NewsCard from "@/components/NewsCard";
import NewsCardSkeleton from "@/components/NewsCardSkeleton";
import { 
  useLatestNews, 
  useTrendingNews, 
  useSearchNews, 
  useNewsSummary,
  useRefreshNewsCache,
  useHealthCheck
} from "@/hooks/useNews";
import { NewsItem } from "@/lib/api";

const Blogs = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [isSearching, setIsSearching] = useState(false);

  // API hooks
  const { data: latestNews, isLoading: latestLoading, error: latestError } = useLatestNews({ limit: 9 });
  const { data: trendingNews, isLoading: trendingLoading, error: trendingError } = useTrendingNews(6);
  const { data: searchResults, isLoading: searchLoading } = useSearchNews(
    searchQuery, 
    { limit: 20, category: selectedCategory as any }
  );
  const { data: newsSummary } = useNewsSummary();
  const { mutate: refreshCache, isPending: isRefreshing } = useRefreshNewsCache();
  const { data: healthStatus } = useHealthCheck();

  // Handle search
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setIsSearching(true);
    }
  };

  // Handle category filter
  const handleCategoryFilter = (category: string) => {
    setSelectedCategory(selectedCategory === category ? null : category);
    setIsSearching(false);
  };

  // Clear search
  const handleClearSearch = () => {
    setSearchQuery("");
    setIsSearching(false);
  };

  // Get display data
  const getDisplayData = () => {
    if (isSearching && searchQuery.trim()) {
      return searchResults?.data || [];
    }
    return latestNews?.data || [];
  };

  const displayData = getDisplayData();
  const isLoading = latestLoading || trendingLoading || searchLoading;
  const hasError = latestError || trendingError;

  // Categories with counts from summary
  const categories = [
    { 
      name: "Tech", 
      icon: TrendingUp, 
      count: newsSummary?.data?.sources?.techcrunch?.count || 0,
      value: "tech"
    },
    { 
      name: "Programming", 
      icon: BookOpen, 
      count: newsSummary?.data?.sources?.dev_to?.count || 0,
      value: "programming"
    },
    { 
      name: "Interview", 
      icon: Users, 
      count: newsSummary?.data?.sources?.leetcode_blog?.count || 0,
      value: "interview"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-bg">
      <div
        className="min-h-screen max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8 
                    m-4 sm:m-6 lg:m-10 bg-gradient-bg border border-blue-300 rounded-3xl overflow-hidden bg-gradient-to-b from-slate-100 to-cyan-50
                    animate-fade-in mt-20"
        style={{ marginTop: '5rem' }}
      >
        {/* Header */}
        <div className="pt-20 mt-10 pb-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div className="inline-flex items-center space-x-2 bg-card/50 backdrop-blur-sm rounded-full px-4 py-2 mb-6 border border-primary/20">
              <Sparkles className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium">Latest Insights & Updates</span>
              {healthStatus && (
                <div className={`w-2 h-2 rounded-full ${healthStatus.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`} />
              )}
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-normal mb-6 leading-tight animate-fade-in text-[#2D3253]">
              Blogs & <span className="bg-gradient-primary bg-clip-text text-transparent">News</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed animate-fade-in">
              Stay updated with the latest career insights, interview tips, and industry trends to accelerate your professional growth.
            </p>
            
            {/* Search Bar */}
            <form onSubmit={handleSearch} className="max-w-md mx-auto relative animate-fade-in">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input
                type="text"
                placeholder="Search articles..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-card/60 border-primary/20 hover:border-primary/30 transition-colors"
              />
              <Button 
                type="submit" 
                size="sm" 
                className="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 hover-scale"
                disabled={!searchQuery.trim()}
              >
                Search
              </Button>
            </form>

            {/* Search Results Header */}
            {isSearching && searchQuery.trim() && (
              <div className="mt-4 flex items-center justify-center gap-2">
                <span className="text-sm text-muted-foreground">
                  Search results for "{searchQuery}"
                </span>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={handleClearSearch}
                  className="h-6 px-2"
                >
                  Clear
                </Button>
            </div>
            )}
          </div>

          {/* Categories */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            {categories.map((category, index) => (
              <Card 
                key={category.name} 
                className={`p-6 text-center hover:bg-card/80 transition-all duration-300 cursor-pointer border-primary/10 hover:border-primary/30 hover:shadow-glow-accent group hover-scale animate-fade-in ${
                  selectedCategory === category.value ? 'bg-primary/10 border-primary/30 shadow-glow-accent' : ''
                }`}
                style={{ animationDelay: `${index * 0.1}s` }}
                onClick={() => handleCategoryFilter(category.value)}
              >
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:bg-primary/20 transition-colors group-hover:animate-pulse">
                  <category.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="font-semibold text-lg mb-2 group-hover:text-primary transition-colors">{category.name}</h3>
                <p className="text-sm text-muted-foreground">{category.count} articles</p>
              </Card>
            ))}
          </div>

          {/* Error State */}
          {hasError && (
            <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-center gap-2 text-red-800">
                <AlertCircle className="h-4 w-4" />
                <span>Failed to load news. Please try again later.</span>
                      </div>
                    </div>
          )}

          {/* Featured Articles (Trending) */}
          {!isSearching && (
            <div className="mb-16">
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl md:text-3xl font-bold">
                  Trending <span className="bg-gradient-primary bg-clip-text text-transparent">Articles</span>
                </h2>
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={() => refreshCache()}
                  disabled={isRefreshing}
                  className="flex items-center gap-2 hover-scale"
                >
                  <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {trendingLoading ? (
                  Array.from({ length: 6 }).map((_, i) => (
                    <NewsCardSkeleton key={i} variant="featured" />
                  ))
                ) : trendingNews?.data?.length ? (
                  trendingNews.data.slice(0, 6).map((news, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 30 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, ease: "easeOut", delay: index * 0.1 }}
                      viewport={{ once: true }}
                    >
                      <NewsCard news={news} variant="featured" />
                    </motion.div>
                  ))
                ) : (
                  <div className="col-span-full text-center py-8 text-muted-foreground">
                    No trending articles available at the moment.
                  </div>
                )}
              </div>
            </div>
          )}

          {/* News Articles */}
          <div>
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl md:text-3xl font-bold">
                {isSearching ? 'Search Results' : (
                  <>
                    Latest <span className="bg-gradient-primary bg-clip-text text-transparent">Articles</span>
                  </>
                )}
              </h2>
              {isSearching && searchResults?.data && (
                <span className="text-sm text-muted-foreground">
                  {searchResults.data.length} results found
                </span>
              )}
            </div>
            
            {isLoading ? (
            <div className="grid md:grid-cols-2 gap-6">
                {Array.from({ length: 8 }).map((_, i) => (
                  <NewsCardSkeleton key={i} variant="default" />
                ))}
                        </div>
            ) : displayData.length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {displayData.map((news, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, ease: "easeOut", delay: index * 0.1 }}
                    viewport={{ once: true }}
                  >
                    <NewsCard news={news} variant="default" />
                  </motion.div>
              ))}
            </div>
            ) : (
              <div className="text-center py-12">
                <BookOpen className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <h3 className="text-lg font-medium mb-2">
                  {isSearching ? 'No search results found' : 'No articles available'}
                </h3>
                <p className="text-muted-foreground">
                  {isSearching 
                    ? 'Try adjusting your search terms or browse our latest articles.'
                    : 'Check back later for fresh content.'
                  }
                </p>
                {isSearching && (
                  <Button onClick={handleClearSearch} className="mt-4">
                    Browse All Articles
                  </Button>
                )}
              </div>
            )}
          </div>

          {/* Newsletter Signup */}
          <div className="mt-16 text-center">
            <Card className="p-8 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent">
              <h3 className="text-2xl font-bold mb-3">Stay Updated</h3>
              <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                Get the latest career insights and interview tips delivered to your inbox.
              </p>
              <div className="flex gap-2 max-w-md mx-auto">
                <Input type="email" placeholder="Enter your email" className="bg-card/60 border-primary/20 hover:border-primary/30 transition-colors" />
                <Button className="hover-scale">Subscribe</Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>

    <Footer />

    <div className="px-4 sm:px-6 lg:px-8 text-center">
      <h1
        className="outlined-text text-[3.5rem] sm:text-[6rem] md:text-[8rem] lg:text-[10rem] xl:text-[12rem] 2xl:text-[14rem] leading-none tracking-widest"
      >
        STTARKEL
      </h1>
    </div>
  </div>
  );
};

export default Blogs; 