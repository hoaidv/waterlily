#!/usr/bin/env python3
"""
Selenium-based Amazon scraper to avoid bot detection
"""

import time
import logging
import random
from typing import Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from .amazon_scraper import AmazonScraper


class SeleniumAmazonScraper(AmazonScraper):
    """
    Amazon scraper using Selenium to simulate real browser traffic
    """
    
    def __init__(self, config: Dict[str, Any], output_dir: str = './output'):
        """Initialize Selenium scraper"""
        super().__init__(config, output_dir)
        
        self.driver = None
        self._setup_driver()
    
    def _setup_driver(self):
        """Setup Selenium Chrome driver with stealth settings"""
        try:
            chrome_options = Options()
            
            # Stealth settings to avoid detection
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User agent
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Window size
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Disable images for faster loading (optional)
            # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
            
            # Headless mode (optional - comment out for debugging)
            chrome_options.add_argument('--headless=new')
            
            # Disable GPU
            chrome_options.add_argument('--disable-gpu')
            
            # No sandbox
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            # Initialize driver
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Set timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(30)
            
            # Hide webdriver property
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
            
            logging.info("✓ Selenium driver initialized")
            
        except Exception as e:
            logging.error(f"Failed to initialize Selenium driver: {e}")
            raise
    
    def _fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch page using Selenium
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None
        """
        try:
            logging.info(f"Fetching: {url}")
            
            # Navigate to page
            self.driver.get(url)
            
            # Random delay to simulate human behavior
            time.sleep(random.uniform(2, 4))
            
            # Wait for page to load (check for common Amazon elements)
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )
            except TimeoutException:
                logging.warning("Page load timeout, continuing anyway...")
            
            # Get page source
            html = self.driver.page_source
            
            # Check for CAPTCHA
            if 'captcha' in html.lower() or 'robot check' in html.lower():
                logging.warning("CAPTCHA detected!")
                return None
            
            return html
            
        except WebDriverException as e:
            logging.error(f"Selenium error fetching {url}: {e}")
            return None
        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
            return None
    
    def search_products_by_category(self, category: Dict[str, Any]) -> list:
        """
        Override to use Selenium-based search
        
        Returns:
            List of product dicts with 'url' key
        """
        category_name = category['name']
        product_urls = self.search_products(category_name, max_products=10)
        
        # Convert URLs to product info dicts
        products = [{'url': url, 'position': i+1} for i, url in enumerate(product_urls)]
        return products
    
    def search_products(self, category_name: str, max_products: int = 10):
        """
        Override search_products to use Selenium
        """
        from urllib.parse import quote_plus
        from lxml import html as lhtml
        
        products = []
        
        try:
            # Construct search URL
            search_query = quote_plus(category_name)
            search_url = f"{self.base_url}/s?k={search_query}"
            
            logging.info(f"Search URL: {search_url}")
            
            # Fetch search page
            html_content = self._fetch_page(search_url)
            
            if not html_content:
                logging.error("Failed to fetch search page")
                return products
            
            # Parse search results
            tree = lhtml.fromstring(html_content)
            
            # Find product links
            product_selectors = [
                '//div[@data-component-type="s-search-result"]//h2/a/@href',
                '//div[@data-asin]//a[contains(@class, "s-link-style")]/@href',
            ]
            
            all_hrefs = []
            for selector in product_selectors:
                hrefs = tree.xpath(selector)
                all_hrefs.extend(hrefs)
            
            logging.info(f"Found {len(all_hrefs)} products with selector: {product_selectors}")
            
            # Filter and clean URLs
            unique_urls = []
            seen = set()
            
            for href in all_hrefs:
                # Skip invalid URLs
                if not href or href == '#' or href.startswith('javascript:'):
                    continue
                
                # Make absolute URL
                if href.startswith('/'):
                    full_url = f"{self.base_url}{href}"
                else:
                    full_url = href
                
                # Extract real URL from redirects
                real_url = self._extract_real_url(full_url)
                
                # Deduplicate
                if real_url not in seen:
                    seen.add(real_url)
                    unique_urls.append(real_url)
                    products.append(real_url)
                
                if len(products) >= max_products:
                    break
            
            logging.info(f"Found {len(products)} unique products for {category_name}")
            
        except Exception as e:
            logging.error(f"Error searching for {category_name}: {e}")
        
        return products
    
    def scrape_product_details(self, product_url: str, category: Dict[str, Any]) -> Dict[str, Any]:
        """
        Override scrape_product_details to use Selenium
        """
        from lxml import html as lhtml
        
        # Extract real URL from redirects
        real_url = self._extract_real_url(product_url)
        logging.info(f"Scraping product: {real_url}")
        
        product_data = {
            'url': real_url,
            'category': category['name'],
            'category_id': category['id'],
            'title': None,
            'price': None,
            'attributes': {},
            'images': [],
            'description': None
        }
        
        try:
            # Fetch page using Selenium
            html_content = self._fetch_page(real_url)
            
            if not html_content:
                product_data['error'] = "Failed to fetch page"
                return product_data
            
            tree = lhtml.fromstring(html_content)
            
            # Extract basic info
            product_data['title'] = self._extract_title(tree)
            product_data['price'] = self._extract_price(tree)
            product_data['images'] = self._extract_images(tree)
            product_data['description'] = self._extract_description(tree)
            
            # Analyze page for patterns if we don't have rules for this category yet
            category_name = category['name']
            if category_name not in self.extraction_config:
                logging.info(f"Learning patterns for {category_name}")
                analysis = self.pattern_learner.analyze_product_page(html_content, real_url)
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
                logging.warning(f"No attributes extracted for {real_url}")
                product_data['_html_snippet'] = html_content[:5000]  # First 5000 chars
            
            self.stats['products_scraped'] += 1
            if product_data['attributes']:
                self.stats['products_with_attributes'] += 1
        
        except Exception as e:
            logging.error(f"Error scraping product {real_url}: {e}")
            product_data['error'] = str(e)
            self.stats['errors'] += 1
        
        return product_data
    
    def __del__(self):
        """Cleanup: close driver"""
        if self.driver:
            try:
                self.driver.quit()
                logging.info("✓ Selenium driver closed")
            except:
                pass
    
    def close(self):
        """Explicitly close the driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

