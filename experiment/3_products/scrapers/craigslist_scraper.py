#!/usr/bin/env python3
"""
Craigslist-specific scraper implementation
"""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus
from base_scraper import BaseScraper


class CraigslistScraper(BaseScraper):
    """Scraper for Craigslist classified ads"""
    
    def __init__(self, delay_range=(1.0, 3.0), max_retries=3, location='sfbay'):
        super().__init__(delay_range, max_retries)
        self.location = location
        self.base_url = f"https://{location}.craigslist.org"
    
    def get_website_name(self) -> str:
        return "craigslist"
    
    def build_search_url(self, category: str, page: int = 1) -> str:
        """Build Craigslist search URL"""
        search_query = f"{category}"
        return f"{self.base_url}/search/sss?query={quote_plus(search_query)}&sort=rel"
    
    def scrape_listing_page(self, category: str, max_products: int = 20) -> List[str]:
        """Scrape product URLs from Craigslist search results"""
        search_url = self.build_search_url(category)
        
        response = self._fetch_with_retry(search_url)
        if not response:
            return []
        
        soup = self._parse_html(response.content)
        
        # Find product listings - try different selectors
        product_rows = []
        
        selectors = [
            ('li', {'class': 'result-row'}),
            ('li', {'class': lambda x: x and 'result' in str(x).lower()}),
            ('li', {'data-pid': True}),
        ]
        
        for tag, attrs in selectors:
            rows = soup.find_all(tag, attrs)
            if rows:
                product_rows = rows
                break
        
        # Alternative: find by post links
        if not product_rows:
            post_links = soup.find_all('a', href=re.compile(r'/\d+\.html'))
            seen_links = set()
            for link in post_links:
                href = link.get('href', '')
                if href and href not in seen_links:
                    parent = link.find_parent(['li', 'div'])
                    if parent:
                        product_rows.append(parent)
                        seen_links.add(href)
                        if len(product_rows) >= max_products:
                            break
        
        # Extract product URLs
        product_urls = []
        for row in product_rows[:max_products]:
            # Find title link
            title_elem = row.find('a', class_='result-title')
            if not title_elem:
                title_elem = row.find('a', href=re.compile(r'/\d+\.html'))
            
            if title_elem and title_elem.get('href'):
                href = title_elem['href']
                if href.startswith('/'):
                    url = f"{self.base_url}{href}"
                elif href.startswith('http'):
                    url = href
                else:
                    url = f"{self.base_url}/{href}"
                
                product_urls.append(url)
        
        return product_urls
    
    def scrape_product_page(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape product information from Craigslist listing page"""
        response = self._fetch_with_retry(url)
        if not response:
            return None
        
        soup = self._parse_html(response.content)
        return self.extract_product_info(soup, url)
    
    def extract_product_info(self, soup, url: str) -> Optional[Dict[str, Any]]:
        """Extract product information from Craigslist page"""
        product = {'url': url, 'source': 'craigslist', 'location_code': self.location}
        
        # Extract post ID
        post_id_match = re.search(r'/(\d+)\.html', url)
        if post_id_match:
            product['post_id'] = post_id_match.group(1)
        
        # Extract title
        title_elem = soup.find('span', id='titletextonly')
        if not title_elem:
            title_elem = soup.find('h1', class_='postingtitle')
        
        if title_elem:
            title = self._clean_text(title_elem.get_text())
            product['name'] = title
        else:
            return None
        
        # Extract price
        price_elem = soup.find('span', class_='price')
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            price_match = re.search(r'\$([\d,]+)', price_text)
            if price_match:
                product['price'] = f"${price_match.group(1)}"
        
        # Extract location
        location_elem = soup.find('div', class_='mapaddress')
        if not location_elem:
            location_elem = soup.find('small')
        
        if location_elem:
            location_text = self._clean_text(location_elem.get_text())
            if location_text:
                product['location'] = location_text
        
        # Extract post date
        date_elem = soup.find('time', class_='date')
        if not date_elem:
            date_elem = soup.find('time')
        
        if date_elem:
            date_text = date_elem.get('datetime', '') or date_elem.get_text()
            if date_text:
                product['date'] = date_text
        
        # Extract description
        description_elem = soup.find('section', id='postingbody')
        if description_elem:
            description = self._clean_text(description_elem.get_text())
            # Remove "QR Code Link to This Post" text
            description = re.sub(r'QR Code Link to This Post.*$', '', description, flags=re.IGNORECASE)
            product['description'] = description[:500]  # Limit length
        
        # Extract images
        image_elems = soup.find_all('img', attrs={'src': re.compile(r'images\.craigslist\.org')})
        if image_elems:
            product['images'] = [img['src'] for img in image_elems if img.get('src')]
            if product['images']:
                product['image_url'] = product['images'][0]
        
        return product

