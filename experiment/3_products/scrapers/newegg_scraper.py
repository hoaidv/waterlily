#!/usr/bin/env python3
"""
Newegg-specific scraper implementation
"""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus
from base_scraper import BaseScraper


class NeweggScraper(BaseScraper):
    """Scraper for Newegg.com"""
    
    def __init__(self, delay_range=(1.0, 3.0), max_retries=3):
        super().__init__(delay_range, max_retries)
        self.base_url = "https://www.newegg.com"
    
    def get_website_name(self) -> str:
        return "newegg"
    
    def build_search_url(self, category: str, page: int = 1) -> str:
        """Build Newegg search URL"""
        search_query = f"{category}"
        return f"{self.base_url}/p/pl?d={quote_plus(search_query)}"
    
    def scrape_listing_page(self, category: str, max_products: int = 20) -> List[str]:
        """Scrape product URLs from Newegg search results"""
        # First visit homepage
        try:
            homepage_response = self._fetch_with_retry(self.base_url)
        except:
            pass
        
        search_url = self.build_search_url(category)
        response = self._fetch_with_retry(search_url)
        if not response:
            return []
        
        soup = self._parse_html(response.content)
        
        # Check for blocking
        title_tag = soup.find('title')
        if title_tag:
            page_title = title_tag.get_text(strip=True).lower()
            if 'blocked' in page_title or 'access denied' in page_title:
                print("      Warning: Newegg may be blocking requests")
                return []
        
        # Find product containers
        product_containers = soup.select('div.item-cell')
        if not product_containers:
            product_containers = soup.select('div.item-container')
        
        # Extract product URLs
        product_urls = []
        for container in product_containers[:max_products]:
            link = container.find('a', class_=lambda x: x and 'title' in str(x).lower())
            if not link:
                link = container.find('a', href=re.compile(r'/p/'))
            
            if link and link.get('href'):
                href = link['href']
                if href.startswith('/'):
                    url = f"{self.base_url}{href}"
                else:
                    url = href
                
                product_urls.append(url)
        
        return product_urls
    
    def scrape_product_page(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape product information from Newegg product page"""
        response = self._fetch_with_retry(url)
        if not response:
            return None
        
        soup = self._parse_html(response.content)
        return self.extract_product_info(soup, url)
    
    def extract_product_info(self, soup, url: str) -> Optional[Dict[str, Any]]:
        """Extract product information from Newegg page"""
        product = {'url': url, 'source': 'newegg'}
        
        # Extract product ID
        product_id_match = re.search(r'/p/([A-Z0-9-]+)', url)
        if product_id_match:
            product['product_id'] = product_id_match.group(1)
        
        # Extract title
        title_elem = soup.find('h1', class_='product-title')
        if not title_elem:
            title_elem = soup.find('h1')
        
        if title_elem:
            product['name'] = self._clean_text(title_elem.get_text())
        else:
            return None
        
        # Extract price
        price_elem = soup.find('li', class_='price-current')
        if not price_elem:
            price_elem = soup.find('span', class_='price-current')
        
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            price_match = re.search(r'\$([\d,]+\.?\d*)', price_text)
            if price_match:
                product['price'] = f"${price_match.group(1)}"
        
        # Extract rating
        rating_elem = soup.find('a', class_=lambda x: x and 'rating' in str(x).lower())
        if rating_elem:
            rating_text = rating_elem.get('title', '') or rating_elem.get_text()
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            if rating_match:
                product['rating'] = rating_match.group(1)
        
        # Extract review count
        reviews_elem = soup.find('a', class_=lambda x: x and 'review' in str(x).lower())
        if reviews_elem:
            reviews_text = reviews_elem.get_text(strip=True)
            reviews_match = re.search(r'\((\d+)\)', reviews_text)
            if reviews_match:
                product['review_count'] = reviews_match.group(1)
        
        # Extract shipping
        shipping_elem = soup.find('li', class_=lambda x: x and 'shipping' in str(x).lower())
        if shipping_elem:
            shipping_text = self._clean_text(shipping_elem.get_text())
            if 'free' in shipping_text.lower():
                product['shipping'] = 'Free Shipping'
        
        # Extract images
        image_elem = soup.find('img', class_='product-view-img-original')
        if not image_elem:
            image_elem = soup.find('img', attrs={'itemprop': 'image'})
        
        if image_elem and image_elem.get('src'):
            product['image_url'] = image_elem['src']
        
        return product

