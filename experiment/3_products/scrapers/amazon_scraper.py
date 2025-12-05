#!/usr/bin/env python3
"""
Amazon-specific scraper implementation
"""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus
from base_scraper import BaseScraper


class AmazonScraper(BaseScraper):
    """Scraper for Amazon.com"""
    
    def __init__(self, delay_range=(2.0, 4.0), max_retries=3):
        super().__init__(delay_range, max_retries)
        self.base_url = "https://www.amazon.com"
    
    def get_website_name(self) -> str:
        return "amazon"
    
    def build_search_url(self, category: str, page: int = 1) -> str:
        """Build Amazon search URL"""
        search_query = f"{category}"
        return f"{self.base_url}/s?k={quote_plus(search_query)}&i=electronics"
    
    def scrape_listing_page(self, category: str, max_products: int = 20) -> List[str]:
        """Scrape product URLs from Amazon search results"""
        print(f"      📋 Building search URL for category: {category}")
        search_url = self.build_search_url(category)
        
        # First visit homepage to establish session
        print(f"      🏠 Visiting homepage to establish session...")
        try:
            homepage_response = self._fetch_with_retry(self.base_url)
        except:
            pass
        
        print(f"      🔍 Searching for products...")
        response = self._fetch_with_retry(search_url)
        if not response:
            print(f"      ✗ Failed to fetch search results")
            return []
        
        soup = self._parse_html(response.content)
        
        # Check page title for debugging
        title = soup.find('title')
        if title:
            print(f"      📄 Page title: {title.get_text()[:80]}")
        
        # Find product containers
        print(f"      🔎 Looking for product containers...")
        product_containers = soup.select('div[data-component-type="s-search-result"]')
        print(f"      → Method 1 (data-component-type): {len(product_containers)} containers")
        
        if not product_containers:
            product_containers = soup.select('div.s-result-item')
            print(f"      → Method 2 (s-result-item): {len(product_containers)} containers")
        
        if not product_containers:
            product_containers = soup.select('div[data-asin]')
            print(f"      → Method 3 (data-asin): {len(product_containers)} containers")
        
        if not product_containers:
            print(f"      ⚠ No product containers found - page structure may have changed")
        
        # Extract product URLs
        product_urls = []
        print(f"      🔗 Extracting product URLs from {len(product_containers)} containers...")
        for i, container in enumerate(product_containers[:max_products], 1):
            link = None
            
            # Method 1: Look for h2 > a structure
            h2_elem = container.find('h2')
            if h2_elem:
                link = h2_elem.find('a')
            
            # Method 2: Find any link with /dp/ in href
            if not link:
                link = container.find('a', href=re.compile(r'/dp/[A-Z0-9]{10}'))
            
            # Method 3: Find link in product image container
            if not link:
                img_container = container.find('div', class_=lambda x: x and 'image' in str(x).lower())
                if img_container:
                    link = img_container.find('a')
            
            # Method 4: Find any link with specific Amazon classes
            if not link:
                link = container.find('a', class_=lambda x: x and ('link-normal' in str(x) or 'product' in str(x)))
            
            if link and link.get('href'):
                href = link['href']
                if href.startswith('/'):
                    url = f"{self.base_url}{href}"
                else:
                    url = href
                
                # Ensure it's a product page
                if '/dp/' in url or '/gp/product/' in url:
                    product_urls.append(url)
                    print(f"         [{i}] ✓ Found product URL")
                else:
                    print(f"         [{i}] ✗ Skipped non-product URL: {url[:60]}")
            else:
                print(f"         [{i}] ✗ No link found in container")
        
        print(f"      ✓ Extracted {len(product_urls)} product URLs")
        return product_urls
    
    def scrape_product_page(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape product information from Amazon product page"""
        response = self._fetch_with_retry(url)
        if not response:
            return None
        
        soup = self._parse_html(response.content)
        return self.extract_product_info(soup, url)
    
    def extract_product_info(self, soup, url: str) -> Optional[Dict[str, Any]]:
        """Extract product information from Amazon page"""
        print(f"      📦 Extracting product info...")
        product = {'url': url, 'source': 'amazon'}
        
        # Extract ASIN
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if asin_match:
            product['asin'] = asin_match.group(1)
            print(f"         ASIN: {product['asin']}")
        
        # Extract title
        title_elem = soup.find('span', id='productTitle')
        if not title_elem:
            title_elem = soup.find('h1', class_='a-size-large')
        
        if title_elem:
            product['name'] = self._clean_text(title_elem.get_text())
            print(f"         Title: {product['name'][:60]}...")
        else:
            print(f"         ✗ Title not found")
            return None
        
        # Extract price
        price_elem = soup.find('span', class_='a-price')
        if price_elem:
            price_whole = price_elem.find('span', class_='a-price-whole')
            price_fraction = price_elem.find('span', class_='a-price-fraction')
            if price_whole:
                price = self._clean_text(price_whole.get_text()).replace(',', '')
                if price_fraction:
                    price += '.' + self._clean_text(price_fraction.get_text())
                product['price'] = f"${price}"
                print(f"         Price: {product['price']}")
        
        if 'price' not in product:
            print(f"         ⚠ Price not found")
        
        # Extract rating
        rating_elem = soup.find('span', class_='a-icon-alt')
        if rating_elem:
            rating_text = rating_elem.get_text()
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            if rating_match:
                product['rating'] = rating_match.group(1)
                print(f"         Rating: {product['rating']}")
        
        # Extract review count
        reviews_elem = soup.find('span', id='acrCustomerReviewText')
        if reviews_elem:
            reviews_text = reviews_elem.get_text()
            reviews_match = re.search(r'([\d,]+)', reviews_text)
            if reviews_match:
                product['review_count'] = reviews_match.group(1).replace(',', '')
                print(f"         Reviews: {product['review_count']}")
        
        # Extract images
        image_elem = soup.find('img', id='landingImage')
        if image_elem and image_elem.get('src'):
            product['image_url'] = image_elem['src']
            print(f"         Image: ✓")
        
        print(f"      ✓ Product info extracted")
        return product

