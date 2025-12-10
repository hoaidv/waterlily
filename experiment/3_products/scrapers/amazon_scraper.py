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
    
    def scrape_product_details(self, product_url: str, category: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrape product details from Amazon product page
        
        Note: This implementation does not work due to bot detection.
        Use SeleniumAmazonScraper instead.
        
        Args:
            product_url: URL of the product page
            category: Category data
            
        Returns:
            Product details dictionary
        """
        raise NotImplementedError(
            "AmazonScraper.scrape_product_details does not work due to bot detection. "
            "Please use SeleniumAmazonScraper instead."
        )
    
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
    
    def scrape_products_from_asins(self, category: Dict[str, Any], max_products: Optional[int] = None, asin_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Scrape products for a category by loading ASINs from JSON file
        
        Args:
            category: Category data from database
            max_products: Maximum number of products to scrape (None = all)
            asin_dir: Optional directory where ASIN files are located (default: self.output_dir)
            
        Returns:
            Processing results dictionary
        """
        category_name = category['name']
        logging.info(f"\n{'='*60}")
        logging.info(f"Scraping products from ASINs for category: {category_name}")
        logging.info(f"{'='*60}")
        
        log_data = {
            'category': category_name,
            'category_id': category['id'],
            'asins_loaded': 0,
            'products_scraped': 0,
            'products_with_attributes': 0,
            'patterns_learned': False,
            'products': [],
            'errors': []
        }
        
        try:
            # Step 1: Load ASINs from JSON file
            safe_name = self._sanitize_filename(category_name)
            asin_directory = asin_dir if asin_dir else self.output_dir
            asin_file = os.path.join(asin_directory, f"amazon_asin_{safe_name}.json")
            
            if not os.path.exists(asin_file):
                logging.warning(f"ASIN file not found: {asin_file}")
                log_data['errors'].append(f"ASIN file not found: {asin_file}")
                self.save_log(category_name, log_data)
                return log_data
            
            with open(asin_file, 'r', encoding='utf-8') as f:
                asins = json.load(f)
            
            if not isinstance(asins, list):
                logging.error(f"Invalid ASIN file format: expected list, got {type(asins)}")
                log_data['errors'].append("Invalid ASIN file format")
                self.save_log(category_name, log_data)
                return log_data
            
            log_data['asins_loaded'] = len(asins)
            logging.info(f"Loaded {len(asins)} ASINs from {asin_file}")
            
            if not asins:
                logging.warning(f"No ASINs found in {asin_file}")
                self.save_log(category_name, log_data)
                return log_data
            
            # Limit ASINs if specified
            if max_products:
                asins = asins[:max_products]
                logging.info(f"Limiting to {max_products} products")
            
            # Step 2: Scrape product details for each ASIN
            scraped_products = []
            analyses = []
            
            for idx, asin in enumerate(asins, 1):
                if not asin or not isinstance(asin, str):
                    logging.warning(f"Invalid ASIN at index {idx-1}: {asin}")
                    continue
                
                # Construct product URL
                product_url = f"{self.base_url}/dp/{asin}"
                logging.info(f"\nScraping product {idx}/{len(asins)}: {product_url}")
                
                try:
                    product_data = self.scrape_product_details(product_url, category)
                    product_data['asin'] = asin
                    product_data['position'] = idx
                    
                    scraped_products.append(product_data)
                    
                    # Collect analysis if present
                    if '_analysis' in product_data and product_data['_analysis'].get('success'):
                        analyses.append(product_data['_analysis'])
                    
                    # Wait between requests
                    if idx < len(asins):
                        self.wait_between_requests()
                        
                except Exception as e:
                    logging.error(f"Error scraping ASIN {asin}: {e}")
                    log_data['errors'].append(f"ASIN {asin}: {str(e)}")
                    self.stats['errors'] += 1
            
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
            
            logging.info(f"\n✓ Completed scraping {category_name}")
            logging.info(f"  ASINs loaded: {log_data['asins_loaded']}")
            logging.info(f"  Products scraped: {log_data['products_scraped']}")
            logging.info(f"  Products with attributes: {log_data['products_with_attributes']}")
            logging.info(f"  Patterns learned: {log_data['patterns_learned']}")
        
        except Exception as e:
            logging.error(f"Error scraping products from ASINs for {category_name}: {e}")
            log_data['errors'].append(str(e))
            self.save_log(category_name, log_data)
            self.stats['errors'] += 1
        
        return log_data
    
    def process_category(self, category: Dict[str, Any], max_products: int = 10, asin_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a complete category by scraping from ASINs (backward compatibility wrapper)
        
        Args:
            category: Category data from database
            max_products: Maximum number of products to scrape
            asin_dir: Optional directory where ASIN files are located
            
        Returns:
            Processing results
        """
        return self.scrape_products_from_asins(category, max_products=max_products, asin_dir=asin_dir)


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

