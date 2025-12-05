#!/usr/bin/env python3
"""
Base scraper framework with common functionality for all website scrapers
"""

import time
import random
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urljoin, quote_plus


class BaseScraper(ABC):
    """Abstract base class for website scrapers"""
    
    def __init__(self, delay_range: Tuple[float, float] = (1.0, 3.0), max_retries: int = 3):
        """
        Initialize base scraper
        
        Args:
            delay_range: Tuple of (min_delay, max_delay) in seconds between requests
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.session = self._create_session()
        self.last_request_time = 0
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with realistic headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
        })
        return session
    
    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        delay = random.uniform(*self.delay_range)
        
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        self.last_request_time = time.time()
    
    def _fetch_with_retry(self, url: str, timeout: int = 15) -> Optional[requests.Response]:
        """
        Fetch URL with retry logic and exponential backoff
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
        
        Returns:
            Response object or None if all retries failed
        """
        print(f"      → Fetching: {url[:100]}")
        
        for attempt in range(self.max_retries):
            try:
                self._rate_limit()
                
                response = self.session.get(url, timeout=timeout, allow_redirects=True)
                
                if response.status_code == 200:
                    print(f"      ✓ Success (200) - Content length: {len(response.content)} bytes")
                    return response
                elif response.status_code == 503:
                    # Service unavailable - wait longer and retry
                    wait_time = (2 ** attempt) * random.uniform(2, 4)
                    print(f"      ⚠ Got 503 Service Unavailable, waiting {wait_time:.1f}s before retry {attempt + 1}/{self.max_retries}")
                    time.sleep(wait_time)
                elif response.status_code == 403:
                    print(f"      ⚠ Got 403 Forbidden (possible blocking) - attempt {attempt + 1}/{self.max_retries}")
                    if attempt < self.max_retries - 1:
                        wait_time = (2 ** attempt) * random.uniform(3, 5)
                        time.sleep(wait_time)
                elif response.status_code == 404:
                    print(f"      ✗ Got 404 Not Found - skipping retries")
                    return None
                else:
                    print(f"      ⚠ Got status code {response.status_code} - attempt {attempt + 1}/{self.max_retries}")
                    if attempt < self.max_retries - 1:
                        wait_time = (2 ** attempt) * random.uniform(1, 2)
                        time.sleep(wait_time)
            
            except requests.exceptions.Timeout:
                print(f"      ⚠ Timeout on attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep((2 ** attempt) * random.uniform(1, 2))
            
            except requests.exceptions.RequestException as e:
                error_msg = str(e)
                if len(error_msg) > 100:
                    error_msg = error_msg[:100] + "..."
                print(f"      ✗ Request error (attempt {attempt + 1}/{self.max_retries}): {error_msg}")
                if attempt < self.max_retries - 1:
                    time.sleep((2 ** attempt) * random.uniform(1, 2))
        
        print(f"      ✗ All {self.max_retries} attempts failed")
        return None
    
    def _parse_html(self, content: bytes) -> BeautifulSoup:
        """
        Parse HTML content with BeautifulSoup
        
        Args:
            content: Raw HTML content
        
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(content, 'html.parser')
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing extra whitespace
        
        Args:
            text: Raw text
        
        Returns:
            Cleaned text
        """
        import re
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @abstractmethod
    def get_website_name(self) -> str:
        """Return the name of the website (e.g., 'amazon', 'flipkart')"""
        pass
    
    @abstractmethod
    def build_search_url(self, category: str, page: int = 1) -> str:
        """
        Build search URL for a category
        
        Args:
            category: Category name to search
            page: Page number (default 1)
        
        Returns:
            Search URL
        """
        pass
    
    @abstractmethod
    def scrape_listing_page(self, category: str, max_products: int = 20) -> List[str]:
        """
        Scrape product URLs from listing page
        
        Args:
            category: Category name to search
            max_products: Maximum number of product URLs to return
        
        Returns:
            List of product URLs
        """
        pass
    
    @abstractmethod
    def scrape_product_page(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape detailed product information from product page
        
        Args:
            url: Product page URL
        
        Returns:
            Dictionary with product information or None if failed
        """
        pass
    
    @abstractmethod
    def extract_product_info(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract product information from parsed HTML
        
        Args:
            soup: BeautifulSoup object of product page
            url: Product URL
        
        Returns:
            Dictionary with basic product information
        """
        pass
    
    def scrape_category(self, category: str, max_products: int = 20) -> List[Dict[str, Any]]:
        """
        High-level method to scrape products from a category
        
        Args:
            category: Category name
            max_products: Maximum number of products to scrape
        
        Returns:
            List of product dictionaries
        """
        print(f"\n  Scraping {self.get_website_name()} for category: {category}")
        
        # Get product URLs from listing
        product_urls = self.scrape_listing_page(category, max_products)
        
        if not product_urls:
            print(f"    ✗ No products found")
            return []
        
        print(f"    Found {len(product_urls)} product URLs")
        
        # Scrape each product
        products = []
        for i, url in enumerate(product_urls, 1):
            print(f"    [{i}/{len(product_urls)}] Scraping: {url[:80]}...")
            
            product = self.scrape_product_page(url)
            if product:
                products.append(product)
                print(f"      ✓ Success")
            else:
                print(f"      ✗ Failed")
        
        print(f"    Total scraped: {len(products)}/{len(product_urls)} products")
        return products


class ScraperError(Exception):
    """Custom exception for scraper errors"""
    pass


class RateLimitError(ScraperError):
    """Exception raised when rate limit is exceeded"""
    pass


class ParsingError(ScraperError):
    """Exception raised when HTML parsing fails"""
    pass

