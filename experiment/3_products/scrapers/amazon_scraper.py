#!/usr/bin/env python3
"""
Amazon scraper with pattern learning capabilities
"""

import json
import logging
import re
from typing import Dict, List, Any, Optional
from urllib.parse import quote_plus, urljoin
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
        self.pattern_learner = PatternLearner()
        
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
    
    def search_products_by_category(self, category: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for products on Amazon by category
        
        Args:
            category: Category data from database
            
        Returns:
            List of product URLs and basic info
        """
        category_name = category['name']
        logging.info(f"Searching Amazon for category: {category_name}")
        
        products = []
        
        try:
            # Construct search URL
            search_query = quote_plus(category_name)
            search_url = f"{self.base_url}/s?k={search_query}"
            
            logging.info(f"Search URL: {search_url}")
            
            # Make request
            response = self.session.get(
                search_url,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logging.error(f"Failed to search: HTTP {response.status_code}")
                return products
            
            # Parse search results
            tree = html.fromstring(response.content)
            
            # Find product links - Amazon uses various selectors
            product_selectors = [
                '//div[@data-component-type="s-search-result"]//h2/a/@href',
                '//div[contains(@class, "s-result-item")]//h2/a/@href',
                '//div[@data-asin]//a[contains(@class, "s-link-style")]/@href'
            ]
            
            product_urls = []
            for selector in product_selectors:
                urls = tree.xpath(selector)
                product_urls.extend(urls)
                if urls:
                    logging.info(f"Found {len(urls)} products with selector: {selector}")
            
            # Remove duplicates and limit
            product_urls = list(dict.fromkeys(product_urls))[:10]
            
            logging.info(f"Found {len(product_urls)} unique products for {category_name}")
            
            for idx, url in enumerate(product_urls):
                # Ensure full URL
                if url.startswith('/'):
                    full_url = urljoin(self.base_url, url)
                else:
                    full_url = url
                
                # Extract ASIN from URL if possible
                asin_match = re.search(r'/dp/([A-Z0-9]{10})', full_url)
                asin = asin_match.group(1) if asin_match else None
                
                products.append({
                    'url': full_url,
                    'asin': asin,
                    'position': idx + 1,
                    'category': category_name
                })
        
        except Exception as e:
            logging.error(f"Error searching for {category_name}: {e}")
            self.stats['errors'] += 1
        
        return products
    
    def scrape_product_details(self, product_url: str, category: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrape product details from Amazon product page
        
        Args:
            product_url: URL of the product page
            category: Category data
            
        Returns:
            Product details dictionary
        """
        logging.info(f"Scraping product: {product_url}")
        
        product_data = {
            'url': product_url,
            'category': category['name'],
            'category_id': category['id'],
            'title': None,
            'price': None,
            'attributes': {},
            'images': [],
            'description': None
        }
        
        try:
            # Make request
            response = self.session.get(
                product_url,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logging.error(f"Failed to fetch product: HTTP {response.status_code}")
                product_data['error'] = f"HTTP {response.status_code}"
                return product_data
            
            html_content = response.text
            tree = html.fromstring(response.content)
            
            # Extract basic info
            product_data['title'] = self._extract_title(tree)
            product_data['price'] = self._extract_price(tree)
            product_data['images'] = self._extract_images(tree)
            product_data['description'] = self._extract_description(tree)
            
            # Analyze page for patterns if we don't have rules for this category yet
            category_name = category['name']
            if category_name not in self.extraction_config:
                logging.info(f"Learning patterns for {category_name}")
                analysis = self.pattern_learner.analyze_product_page(html_content, product_url)
                product_data['_analysis'] = analysis
            else:
                logging.info(f"Using existing rules for {category_name}")
                analysis = None
            
            # Extract attributes using learned rules
            if category_name in self.extraction_config:
                rules = self.extraction_config[category_name].get('rules', [])
                attributes = self.pattern_learner.extract_with_rules(html_content, rules)
                product_data['attributes'] = attributes
            else:
                # Try to extract using analysis
                if analysis and analysis.get('success'):
                    rules = analysis.get('extraction_rules', [])
                    if rules:
                        attributes = self.pattern_learner.extract_with_rules(html_content, rules)
                        product_data['attributes'] = attributes
            
            # Store HTML snippet if no attributes found
            if not product_data['attributes']:
                logging.warning(f"No attributes extracted for {product_url}")
                product_data['_html_snippet'] = html_content[:5000]  # First 5000 chars
            
            self.stats['products_scraped'] += 1
            if product_data['attributes']:
                self.stats['products_with_attributes'] += 1
        
        except Exception as e:
            logging.error(f"Error scraping product {product_url}: {e}")
            product_data['error'] = str(e)
            self.stats['errors'] += 1
        
        return product_data
    
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
    
    def process_category(self, category: Dict[str, Any], max_products: int = 10) -> Dict[str, Any]:
        """
        Process a complete category: search, scrape, learn patterns
        
        Args:
            category: Category data from database
            max_products: Maximum number of products to scrape
            
        Returns:
            Processing results
        """
        category_name = category['name']
        logging.info(f"\n{'='*60}")
        logging.info(f"Processing category: {category_name}")
        logging.info(f"{'='*60}")
        
        log_data = {
            'category': category_name,
            'category_id': category['id'],
            'products_found': 0,
            'products_scraped': 0,
            'products_with_attributes': 0,
            'patterns_learned': False,
            'products': [],
            'errors': []
        }
        
        try:
            # Step 1: Search for products
            products = self.search_products_by_category(category)
            log_data['products_found'] = len(products)
            
            if not products:
                logging.warning(f"No products found for {category_name}")
                self.save_log(category_name, log_data)
                return log_data
            
            # Limit products
            products = products[:max_products]
            
            # Step 2: Scrape product details
            scraped_products = []
            analyses = []
            
            for idx, product_info in enumerate(products, 1):
                logging.info(f"\nScraping product {idx}/{len(products)}")
                
                product_data = self.scrape_product_details(product_info['url'], category)
                product_data.update(product_info)  # Add search info
                
                scraped_products.append(product_data)
                
                # Collect analysis if present
                if '_analysis' in product_data and product_data['_analysis'].get('success'):
                    analyses.append(product_data['_analysis'])
                
                # Wait between requests
                if idx < len(products):
                    self.wait_between_requests()
            
            log_data['products_scraped'] = len(scraped_products)
            log_data['products_with_attributes'] = sum(
                1 for p in scraped_products if p.get('attributes')
            )
            log_data['products'] = scraped_products
            
            # Step 3: Learn patterns if we have analyses
            if analyses and category_name not in self.extraction_config:
                logging.info(f"\nLearning patterns from {len(analyses)} products")
                learned_patterns = self.pattern_learner.learn_patterns(analyses, category_name)
                
                if learned_patterns['patterns_found']:
                    # Save learned patterns to config
                    self.extraction_config[category_name] = learned_patterns
                    self.save_config(self.extraction_config)
                    log_data['patterns_learned'] = True
                    log_data['learned_patterns'] = learned_patterns
                    
                    logging.info(f"✓ Learned {len(learned_patterns['rules'])} patterns for {category_name}")
                else:
                    logging.warning(f"No patterns learned for {category_name}")
                    
                    # Save HTML content for manual analysis
                    for product in scraped_products:
                        if '_html_snippet' in product:
                            self.save_analyze_content(
                                category_name,
                                product['_html_snippet'],
                                suffix=f"_{product.get('asin', 'unknown')}"
                            )
            
            # Step 4: Save products
            # Remove temporary analysis data before saving
            for product in scraped_products:
                product.pop('_analysis', None)
                product.pop('_html_snippet', None)
            
            self.save_products(scraped_products)
            
            # Step 5: Save log
            self.save_log(category_name, log_data)
            
            self.stats['categories_processed'] += 1
            
            logging.info(f"\n✓ Completed processing {category_name}")
            logging.info(f"  Products found: {log_data['products_found']}")
            logging.info(f"  Products scraped: {log_data['products_scraped']}")
            logging.info(f"  Products with attributes: {log_data['products_with_attributes']}")
            logging.info(f"  Patterns learned: {log_data['patterns_learned']}")
        
        except Exception as e:
            logging.error(f"Error processing category {category_name}: {e}")
            log_data['errors'].append(str(e))
            self.save_log(category_name, log_data)
            self.stats['errors'] += 1
        
        return log_data


def main():
    """Test the Amazon scraper"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Test configuration
    config = {
        'rate_limiting': {
            'delay_range': [2, 4],
            'max_retries': 3,
            'timeout': 15
        }
    }
    
    # Test categories
    test_categories = [
        {'id': 1, 'name': 'Laptop', 'product_def_id': 1},
        {'id': 2, 'name': 'Smartphone', 'product_def_id': 2}
    ]
    
    scraper = AmazonScraper(config, output_dir="../output")
    
    for category in test_categories:
        result = scraper.process_category(category, max_products=3)
        print(f"\nProcessed {category['name']}: {result['products_scraped']} products")


if __name__ == "__main__":
    main()

