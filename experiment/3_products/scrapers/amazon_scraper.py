#!/usr/bin/env python3
"""
Amazon scraper with pattern learning capabilities
"""

import json
import logging
import os
import re
from typing import Dict, List, Any, Optional
from urllib.parse import quote_plus, urljoin, urlparse, parse_qs, unquote
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from lxml import html

from .base_scraper import BaseScraper
from .pattern_learner import PatternLearner


class AmazonScraper(BaseScraper):
    """Scraper for Amazon products with learning capabilities"""
    
    def __init__(self, config: Dict[str, Any], output_dir: str = "./output"):
        """Initialize Amazon scraper"""
        super().__init__(config, output_dir)
        
        self.base_url = "https://www.amazon.com"
        # Pass config_dir to PatternLearner so it can load shared patterns
        config_dir = os.path.join(os.path.dirname(output_dir), "config")
        self.pattern_learner = PatternLearner(config_dir=config_dir)
        
        # Set up session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Headers to mimic a browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Load existing extraction rules
        self.extraction_config = self.load_config()
    
    def get_website_name(self) -> str:
        """Return website name"""
        return "amazon"
    
    def _extract_real_url(self, url: str) -> str:
        """
        Extract real product URL from Amazon tracking/redirect URLs
        
        Args:
            url: Potentially a redirect URL (e.g., /sspa/click?...)
            
        Returns:
            The actual product URL
        """
        # Handle /sspa/click redirect URLs
        if '/sspa/click' in url:
            try:
                parsed = urlparse(url)
                query_params = parse_qs(parsed.query)
                
                # Extract the 'url' parameter which contains the actual product URL
                if 'url' in query_params:
                    real_url = unquote(query_params['url'][0])
                    
                    # If it's a relative URL, make it absolute
                    if real_url.startswith('/'):
                        real_url = f"{self.base_url}{real_url}"
                    
                    return real_url
            except Exception as e:
                logging.warning(f"Failed to extract real URL from {url}: {e}")
        
        # If URL is relative, make it absolute
        if url.startswith('/'):
            return f"{self.base_url}{url}"
        
        return url
    
    def _extract_title(self, tree) -> Optional[str]:
        """Extract product title"""
        selectors = [
            '//span[@id="productTitle"]/text()',
            '//h1[@id="title"]//text()',
            '//h1[contains(@class, "product-title")]//text()'
        ]
        
        for selector in selectors:
            titles = tree.xpath(selector)
            if titles:
                return ' '.join(titles).strip()
        
        return None
    
    def _extract_price(self, tree) -> Optional[str]:
        """Extract product price"""
        selectors = [
            '//span[@class="a-price"]//span[@class="a-offscreen"]/text()',
            '//span[@id="priceblock_ourprice"]/text()',
            '//span[@id="priceblock_dealprice"]/text()',
            '//span[contains(@class, "a-price-whole")]/text()'
        ]
        
        for selector in selectors:
            prices = tree.xpath(selector)
            if prices:
                return prices[0].strip()
        
        return None
    
    def _extract_images(self, tree) -> List[str]:
        """Extract product images"""
        images = []
        
        # Try to find main image
        img_selectors = [
            '//img[@id="landingImage"]/@src',
            '//div[@id="imgTagWrapperId"]//img/@src',
            '//img[contains(@class, "a-dynamic-image")]/@src'
        ]
        
        for selector in img_selectors:
            img_urls = tree.xpath(selector)
            images.extend(img_urls)
            if img_urls:
                break
        
        return images[:5]  # Limit to 5 images
    
    def _extract_description(self, tree) -> Optional[str]:
        """Extract product description"""
        selectors = [
            '//div[@id="productDescription"]//text()',
            '//div[@id="feature-bullets"]//text()',
            '//div[contains(@class, "product-description")]//text()'
        ]
        
        for selector in selectors:
            desc_parts = tree.xpath(selector)
            if desc_parts:
                description = ' '.join([p.strip() for p in desc_parts if p.strip()])
                if description:
                    return description[:1000]  # Limit length
        
        return None
    