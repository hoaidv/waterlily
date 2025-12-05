#!/usr/bin/env python3
"""
Flipkart-specific scraper implementation
"""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus
from base_scraper import BaseScraper


class FlipkartScraper(BaseScraper):
    """Scraper for Flipkart.com"""
    
    def __init__(self, delay_range=(1.0, 3.0), max_retries=3):
        super().__init__(delay_range, max_retries)
        self.base_url = "https://www.flipkart.com"
    
    def get_website_name(self) -> str:
        return "flipkart"
    
    def build_search_url(self, category: str, page: int = 1) -> str:
        """Build Flipkart search URL"""
        search_query = f"{category}"
        return f"{self.base_url}/search?q={quote_plus(search_query)}"
    
    def scrape_listing_page(self, category: str, max_products: int = 20) -> List[str]:
        """Scrape product URLs from Flipkart search results"""
        search_url = self.build_search_url(category)
        
        response = self._fetch_with_retry(search_url)
        if not response:
            return []
        
        soup = self._parse_html(response.content)
        
        # Find product links
        product_links = soup.find_all('a', href=re.compile(r'/p/'))
        
        # Extract unique product URLs
        product_urls = []
        seen_urls = set()
        
        for link in product_links:
            href = link.get('href', '')
            if href and href not in seen_urls:
                if href.startswith('/'):
                    url = f"{self.base_url}{href}"
                else:
                    url = href
                
                # Extract clean URL (remove query params)
                clean_url = url.split('?')[0]
                
                if clean_url not in seen_urls:
                    product_urls.append(url)
                    seen_urls.add(clean_url)
                
                if len(product_urls) >= max_products:
                    break
        
        return product_urls
    
    def scrape_product_page(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape product information from Flipkart product page"""
        response = self._fetch_with_retry(url)
        if not response:
            return None
        
        soup = self._parse_html(response.content)
        return self.extract_product_info(soup, url)
    
    def extract_product_info(self, soup, url: str) -> Optional[Dict[str, Any]]:
        """Extract product information from Flipkart page"""
        product = {'url': url, 'source': 'flipkart'}
        
        # Extract product ID
        product_id_match = re.search(r'/p/([a-zA-Z0-9]+)', url)
        if product_id_match:
            product['product_id'] = product_id_match.group(1)
        
        # Extract title - try multiple selectors
        title_elem = soup.find('span', class_='B_NuCI')
        if not title_elem:
            title_elem = soup.find('h1', class_='yhB1nd')
        if not title_elem:
            # Try finding by text pattern
            h1_tags = soup.find_all('h1')
            for h1 in h1_tags:
                text = h1.get_text(strip=True)
                if len(text) > 10:
                    title_elem = h1
                    break
        
        if title_elem:
            product['name'] = self._clean_text(title_elem.get_text())
        else:
            return None
        
        # Extract price (Flipkart uses ₹)
        price_elem = soup.find('div', class_='_30jeq3')
        if not price_elem:
            price_elem = soup.find('div', class_='_1_WHN1')
        if not price_elem:
            # Try finding by rupee symbol
            price_elem = soup.find(string=re.compile(r'₹'))
            if price_elem:
                price_elem = price_elem.find_parent()
        
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            price_match = re.search(r'₹\s*([\d,]+)', price_text)
            if price_match:
                product['price'] = f"₹{price_match.group(1)}"
        
        # Extract rating
        rating_elem = soup.find('div', class_='_3LWZlK')
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            if rating_match:
                product['rating'] = rating_match.group(1)
        
        # Extract review count
        reviews_elem = soup.find('span', class_='_2_R_DZ')
        if reviews_elem:
            reviews_text = reviews_elem.get_text(strip=True)
            reviews_match = re.search(r'([\d,]+)', reviews_text)
            if reviews_match:
                product['review_count'] = reviews_match.group(1).replace(',', '')
        
        # Extract images
        image_elem = soup.find('img', class_='_396cs4')
        if not image_elem:
            image_elem = soup.find('img', attrs={'itemprop': 'image'})
        
        if image_elem and image_elem.get('src'):
            product['image_url'] = image_elem['src']
        
        return product

