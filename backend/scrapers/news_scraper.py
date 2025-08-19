import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import feedparser
import re
from typing import List, Dict, Optional, Any
import logging
from urllib.parse import urljoin, urlparse
import time
import random
import html

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Keywords for filtering relevant news
        self.coding_keywords = [
            'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust', 'kotlin', 'swift',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'laravel', 'express',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'machine learning', 'ai', 'artificial intelligence',
            'data science', 'blockchain', 'web3', 'cybersecurity', 'devops', 'git', 'github'
        ]
        
        self.interview_keywords = [
            'interview', 'coding interview', 'technical interview', 'leetcode', 'hackerrank', 'codeforces',
            'data structures', 'algorithms', 'system design', 'behavioral interview', 'resume', 'career',
            'job search', 'placement', 'campus recruitment', 'internship', 'software engineer', 'developer'
        ]

    async def __aenter__(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None

    async def _ensure_session(self):
        """Ensure session is created"""
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)

    def clean_html_content(self, html_content: str) -> str:
        """Clean HTML content and extract plain text"""
        if not html_content:
            return ""
        
        # First decode HTML entities
        decoded = html.unescape(html_content)
        
        # Use BeautifulSoup to extract text
        soup = BeautifulSoup(decoded, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit length to avoid very long descriptions
        if len(text) > 300:
            text = text[:300] + "..."
        
        return text

    async def extract_image_url(self, entry, soup=None) -> str:
        """Extract image URL from RSS entry or HTML content"""
        try:
            # Try to get image from RSS media content
            if hasattr(entry, 'media_content') and entry.media_content:
                return entry.media_content[0]['url']
            
            # Try to get image from RSS enclosures
            if hasattr(entry, 'enclosures') and entry.enclosures:
                for enclosure in entry.enclosures:
                    if enclosure.get('type', '').startswith('image/'):
                        return enclosure.get('href', '')
            
            # Try to get image from RSS links
            if hasattr(entry, 'links') and entry.links:
                for link in entry.links:
                    if link.get('type', '').startswith('image/'):
                        return link.get('href', '')
            
            # Try to extract from HTML content if available
            if soup:
                # Look for common image selectors
                img_selectors = [
                    'img[src]',
                    'meta[property="og:image"]',
                    'meta[name="twitter:image"]',
                    'meta[property="twitter:image"]'
                ]
                
                for selector in img_selectors:
                    img_elem = soup.select_one(selector)
                    if img_elem:
                        src = img_elem.get('src') or img_elem.get('content')
                        if src:
                            return src
            
            # If we have an entry with a link, try to visit the actual article page
            if hasattr(entry, 'link') and entry.link:
                try:
                    await self._ensure_session()
                    # Reduced timeout for faster response
                    async with self.session.get(entry.link, timeout=5) as response:
                        if response.status == 200:
                            article_content = await response.text()
                            article_soup = BeautifulSoup(article_content, 'html.parser')
                            
                            # Look for images in the article content
                            img_selectors = [
                                'meta[property="og:image"]',
                                'meta[name="twitter:image"]',
                                'meta[property="twitter:image"]',
                                'meta[property="image"]',
                                'meta[name="image"]'
                            ]
                            
                            for selector in img_selectors:
                                img_elem = article_soup.select_one(selector)
                                if img_elem:
                                    content_attr = img_elem.get('content')
                                    if content_attr:
                                        # Make sure it's an absolute URL
                                        if content_attr.startswith('http'):
                                            return content_attr
                                        elif content_attr.startswith('//'):
                                            return 'https:' + content_attr
                                        else:
                                            # Try to construct absolute URL
                                            try:
                                                from urllib.parse import urljoin
                                                return urljoin(entry.link, content_attr)
                                            except:
                                                continue
                            
                            # Look for any img tag with a reasonable src
                            for img in article_soup.find_all('img'):
                                src = img.get('src')
                                if src and not src.startswith('data:') and len(src) > 10:
                                    if src.startswith('http'):
                                        return src
                                    elif src.startswith('//'):
                                        return 'https:' + src
                                    else:
                                        try:
                                            from urllib.parse import urljoin
                                            return urljoin(entry.link, src)
                                        except:
                                            continue
                                    
                except Exception as e:
                    logger.debug(f"Could not fetch article content for image extraction: {e}")
            
            # Default placeholder image - using a working URL
            return "https://picsum.photos/400/200?random=1"
            
        except Exception as e:
            logger.warning(f"Error extracting image: {e}")
            return "https://picsum.photos/400/200?random=1"

    async def extract_image_from_url(self, url: str) -> str:
        """Extract image from a given article URL"""
        try:
            await self._ensure_session()
            async with self.session.get(url, timeout=5) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Look for Open Graph and Twitter meta images first
                    meta_selectors = [
                        'meta[property="og:image"]',
                        'meta[name="twitter:image"]',
                        'meta[property="twitter:image"]',
                        'meta[property="image"]',
                        'meta[name="image"]'
                    ]
                    
                    for selector in meta_selectors:
                        meta_elem = soup.select_one(selector)
                        if meta_elem:
                            content_attr = meta_elem.get('content')
                            if content_attr:
                                if content_attr.startswith('http'):
                                    return content_attr
                                elif content_attr.startswith('//'):
                                    return 'https:' + content_attr
                    
                    # Look for any img tag with a reasonable src
                    for img in soup.find_all('img'):
                        src = img.get('src')
                        if src and not src.startswith('data:') and len(src) > 10:
                            if src.startswith('http'):
                                return src
                            elif src.startswith('//'):
                                return 'https:' + src
                            else:
                                try:
                                    from urllib.parse import urljoin
                                    return urljoin(url, src)
                                except:
                                    continue
                    
        except Exception as e:
            logger.debug(f"Could not extract image from URL {url}: {e}")
        
        return "https://picsum.photos/400/200?random=1"

    def is_relevant_news(self, title: str, content: str = "") -> bool:
        """Check if the news is relevant to coding or interview preparation"""
        text = (title + " " + content).lower()
        
        # Check for coding-related keywords
        coding_matches = sum(1 for keyword in self.coding_keywords if keyword.lower() in text)
        
        # Check for interview-related keywords
        interview_matches = sum(1 for keyword in self.interview_keywords if keyword.lower() in text)
        
        return coding_matches > 0 or interview_matches > 0

    async def scrape_techcrunch(self) -> List[Dict[str, Any]]:
        """Scrape TechCrunch for tech news"""
        try:
            await self._ensure_session()
            url = "https://techcrunch.com/feed/"
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    feed = feedparser.parse(content)
                    
                    news_items = []
                    for entry in feed.entries[:20]:  # Get latest 20 articles
                        if self.is_relevant_news(entry.title, entry.get('summary', '')):
                            # Clean the description
                            clean_description = self.clean_html_content(entry.get('summary', ''))
                            
                            # Extract image
                            image_url = await self.extract_image_url(entry)
                            
                            news_items.append({
                                'title': entry.title,
                                'description': clean_description,
                                'url': entry.link,
                                'published_date': entry.get('published', ''),
                                'source': 'TechCrunch',
                                'category': 'tech',
                                'image_url': image_url
                            })
                    return news_items
                else:
                    logger.warning(f"TechCrunch returned status {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error scraping TechCrunch: {e}")
            return []

    async def scrape_hackernews(self) -> List[Dict[str, Any]]:
        """Scrape Hacker News"""
        try:
            await self._ensure_session()
            url = "https://news.ycombinator.com/"
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    news_items = []
                    # Find all story rows
                    stories = soup.find_all('tr', class_='athing')
                    
                    for story in stories[:30]:  # Get top 30 stories
                        title_elem = story.find('span', class_='titleline')
                        if title_elem:
                            title_link = title_elem.find('a')
                            if title_link:
                                title = title_link.get_text(strip=True)
                                url = title_link.get('href', '')
                                
                                if title and self.is_relevant_news(title):
                                    # Extract image from the actual article page
                                    image_url = await self.extract_image_from_url(url)
                                    
                                    news_items.append({
                                        'title': title,
                                        'description': f"Hacker News story: {title}",
                                        'url': url,
                                        'published_date': datetime.now().strftime('%Y-%m-%d'),
                                        'source': 'Hacker News',
                                        'category': 'tech',
                                        'image_url': image_url
                                    })
                    return news_items
                else:
                    logger.warning(f"Hacker News returned status {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error scraping Hacker News: {e}")
            return []

    async def scrape_dev_to(self) -> List[Dict[str, Any]]:
        """Scrape Dev.to for programming articles"""
        try:
            await self._ensure_session()
            url = "https://dev.to/feed"
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    feed = feedparser.parse(content)
                    
                    news_items = []
                    for entry in feed.entries[:20]:
                        if self.is_relevant_news(entry.title, entry.get('summary', '')):
                            # Clean the description
                            clean_description = self.clean_html_content(entry.get('summary', ''))
                            
                            # Extract image
                            image_url = await self.extract_image_url(entry)
                            
                            news_items.append({
                                'title': entry.title,
                                'description': clean_description,
                                'url': entry.link,
                                'published_date': entry.get('published', ''),
                                'source': 'Dev.to',
                                'category': 'programming',
                                'image_url': image_url
                            })
                    return news_items
                else:
                    logger.warning(f"Dev.to returned status {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error scraping Dev.to: {e}")
            return []

    async def scrape_leetcode_blog(self) -> List[Dict[str, Any]]:
        """Scrape LeetCode blog for interview preparation"""
        try:
            await self._ensure_session()
            url = "https://leetcode.com/blog/"
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    news_items = []
                    # Look for blog post links
                    articles = soup.find_all('article') or soup.find_all('div', class_='post')
                    
                    for article in articles[:15]:
                        title_elem = article.find('h2') or article.find('h3')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            if title and self.is_relevant_news(title):
                                link = title_elem.find('a') or article.find('a')
                                url = urljoin("https://leetcode.com/blog", link.get('href', '')) if link else ""
                                
                                # Get description
                                desc_elem = article.find('p')
                                description = desc_elem.get_text(strip=True) if desc_elem else ""
                                
                                # Extract image from the actual article page if we have a URL
                                if url and url.startswith('http'):
                                    image_url = await self.extract_image_from_url(url)
                                else:
                                    image_url = await self.extract_image_url(None, article)
                                
                                news_items.append({
                                    'title': title,
                                    'description': description,
                                    'url': url,
                                    'published_date': datetime.now().strftime('%Y-%m-%d'),
                                    'source': 'LeetCode Blog',
                                    'category': 'interview',
                                    'image_url': image_url
                                })
                    return news_items
                else:
                    logger.warning(f"LeetCode blog returned status {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error scraping LeetCode blog: {e}")
            return []

    async def scrape_geeksforgeeks(self) -> List[Dict[str, Any]]:
        """Scrape GeeksforGeeks for interview preparation"""
        try:
            await self._ensure_session()
            url = "https://www.geeksforgeeks.org/"
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    news_items = []
                    # Look for article links
                    articles = soup.find_all('article') or soup.find_all('div', class_='post')
                    
                    for article in articles[:15]:
                        title_elem = article.find('h2') or article.find('h3')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            if title and self.is_relevant_news(title):
                                link = title_elem.find('a') or article.find('a')
                                url = urljoin("https://www.geeksforgeeks.org", link.get('href', '')) if link else ""
                                
                                # Get description
                                desc_elem = article.find('p')
                                description = desc_elem.get_text(strip=True) if desc_elem else ""
                                
                                # Extract image from the actual article page if we have a URL
                                if url and url.startswith('http'):
                                    image_url = await self.extract_image_from_url(url)
                                else:
                                    image_url = await self.extract_image_url(None, article)
                                
                                news_items.append({
                                    'title': title,
                                    'description': description,
                                    'url': url,
                                    'published_date': datetime.now().strftime('%Y-%m-%d'),
                                    'source': 'GeeksforGeeks',
                                    'category': 'interview',
                                    'image_url': image_url
                                })
                    return news_items
                else:
                    logger.warning(f"GeeksforGeeks returned status {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error scraping GeeksforGeeks: {e}")
            return []

    async def scrape_stackoverflow_blog(self) -> List[Dict[str, Any]]:
        """Scrape Stack Overflow blog"""
        try:
            await self._ensure_session()
            url = "https://stackoverflow.blog/"
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    news_items = []
                    # Look for blog post links
                    articles = soup.find_all('article') or soup.find_all('div', class_='post')
                    
                    for article in articles[:15]:
                        title_elem = article.find('h2') or article.find('h3')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            if title and self.is_relevant_news(title):
                                link = title_elem.find('a') or article.find('a')
                                url = urljoin("https://stackoverflow.blog", link.get('href', '')) if link else ""
                                
                                # Get description
                                desc_elem = article.find('p')
                                description = desc_elem.get_text(strip=True) if desc_elem else ""
                                
                                # Extract image from the actual article page if we have a URL
                                if url and url.startswith('http'):
                                    image_url = await self.extract_image_from_url(url)
                                else:
                                    image_url = await self.extract_image_url(None, article)
                                
                                news_items.append({
                                    'title': title,
                                    'description': description,
                                    'url': url,
                                    'published_date': datetime.now().strftime('%Y-%m-%d'),
                                    'source': 'Stack Overflow Blog',
                                    'category': 'programming',
                                    'image_url': image_url
                                })
                    return news_items
                else:
                    logger.warning(f"Stack Overflow blog returned status {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error scraping Stack Overflow blog: {e}")
            return []

    async def scrape_all_sources(self) -> Dict[str, List[Dict[str, Any]]]:
        """Scrape all news sources concurrently"""
        await self._ensure_session()
        
        tasks = [
            self.scrape_techcrunch(),
            self.scrape_hackernews(),
            self.scrape_dev_to(),
            self.scrape_leetcode_blog(),
            self.scrape_geeksforgeeks(),
            self.scrape_stackoverflow_blog()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and filter out exceptions
        news_data = {
            'techcrunch': results[0] if not isinstance(results[0], Exception) else [],
            'hackernews': results[1] if not isinstance(results[1], Exception) else [],
            'dev_to': results[2] if not isinstance(results[2], Exception) else [],
            'leetcode_blog': results[3] if not isinstance(results[3], Exception) else [],
            'geeksforgeeks': results[4] if not isinstance(results[4], Exception) else [],
            'stackoverflow_blog': results[5] if not isinstance(results[5], Exception) else []
        }
        
        return news_data

    async def get_latest_news(self, category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get latest news with optional category filtering"""
        all_news = await self.scrape_all_sources()
        
        # Flatten all news items
        flat_news = []
        for source, news_list in all_news.items():
            if news_list:  # Only process if news_list is not empty
                for news in news_list:
                    news['source_name'] = source
                    flat_news.append(news)
        
        # Filter by category if specified
        if category:
            flat_news = [news for news in flat_news if news.get('category') == category]
        
        # Sort by date (newest first) and limit results
        flat_news.sort(key=lambda x: x.get('published_date', ''), reverse=True)
        
        return flat_news[:limit]

    def add_delay(self):
        """Add random delay to avoid being blocked"""
        time.sleep(random.uniform(1, 3)) 