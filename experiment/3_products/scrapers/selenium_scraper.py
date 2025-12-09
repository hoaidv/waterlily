#!/usr/bin/env python3
"""
Selenium-based Amazon scraper to avoid bot detection
"""

import time
import logging
import random
import json
import os
from typing import Dict, Any, Optional, List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

from .amazon_scraper import AmazonScraper


class SeleniumAmazonScraper(AmazonScraper):
    """
    Amazon scraper using Selenium to simulate real browser traffic
    """
    
    def __init__(self, config: Dict[str, Any], output_dir: str = './output'):
        """Initialize Selenium scraper"""
        super().__init__(config, output_dir)
        
        self.driver = None
        self.current_search_url = None  # Track current search page
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
            
            # Enable all media and scripts for realistic browsing
            prefs = {
                'profile.managed_default_content_settings.images': 2,  # Disable images (2 = block, 1 = allow)
                'profile.managed_default_content_settings.javascript': 1,  # Enable JavaScript
                # 'profile.managed_default_content_settings.plugins': 1,  # Enable plugins
                # 'profile.managed_default_content_settings.media_stream': 1,  # Enable media
                'disk-cache-size': 8192
            }
            chrome_options.add_experimental_option('prefs', prefs)
            
            # Headless mode disabled - show browser for manual CAPTCHA solving
            # chrome_options.add_argument('--headless=new')
            
            # Enable GPU for better rendering
            # chrome_options.add_argument('--disable-gpu')
            
            # No sandbox
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            # Initialize driver
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Set timeouts (shorter for faster scraping)
            self.driver.implicitly_wait(5)
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
            
            # Use configured delay from rate_limiting settings (already applied in navigation)
            
            # Wait for page to load (shorter timeout for speed)
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )
            except TimeoutException:
                logging.debug("Page load timeout, continuing anyway...")
            
            # Simulate human behavior: incremental scrolling over ~5 seconds
            try:
                # Scroll down a bit (random amount)
                scroll_amount = random.randint(300, 800)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(2.0, 3.0))
            except Exception as e:
                logging.debug(f"Scroll simulation failed: {e}")
            
            # Get page source
            html = self.driver.page_source
            
            # Check for "Dogs of Amazon" page - Navigate home to avoid
            if 'dogs of amazon' in html.lower():
                logging.warning("🐕 'Dogs of Amazon' page detected!")
                logging.info("🔗 Navigating home after 🐕")
                
                try:
                    # Navigate to the continue shopping page
                    self.driver.get("https://www.amazon.com/ref=cs_503_link")
                    time.sleep(random.uniform(0, 2))
                    logging.info("✅ Navigated home after 🐕")
                    
                    # Wait a bit more before retry
                    time.sleep(random.uniform(0, 2))
                    
                    # Retry the original URL
                    logging.info("⏳ Retrying original request...")
                    self.driver.get(url)
                    time.sleep(random.uniform(*self.delay_range))
                    
                    # Re-scroll
                    try:
                        self._human_like_scroll()
                    except:
                        pass
                    
                    html = self.driver.page_source
                    logging.info("✅ Successfully recovered from Dogs of Amazon")
                    
                except Exception as e:
                    logging.error(f"Error recovering from Dogs of Amazon: {e}")
                    return None
            
            # Check for "Continue Shopping" button or CAPTCHA
            if 'continue shopping' in html.lower():
                logging.info("🔘 'Continue Shopping' button detected - clicking it...")
                try:
                    time.sleep(1)  # Wait for page to load

                    button_clicked = False
                    try:
                        button = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Continue shopping')]")
                        button.click()
                        logging.info("✅ Clicked 'Continue Shopping' button")
                        html = self.driver.page_source
                        button_clicked = True
                    except:
                        logging.warning("⚠️  Could not click 'Continue Shopping' button, continuing anyway...")
                    
                    if not button_clicked:
                        logging.warning("⚠️  Could not find 'Continue Shopping' button, continuing anyway...")
                except Exception as e:
                    logging.warning(f"Error clicking button: {e}")
            
            # Check for CAPTCHA
            if 'captcha' in html.lower() or 'robot check' in html.lower():
                logging.warning("⚠️  CAPTCHA DETECTED! Please solve it manually in the browser window...")
                logging.warning("⏳ Waiting for you to solve CAPTCHA... (checking every 5 seconds)")
                
                # Wait for user to solve CAPTCHA
                captcha_solved = False
                wait_time = 0
                max_wait = 300  # Wait up to 5 minutes
                
                while not captcha_solved and wait_time < max_wait:
                    time.sleep(5)
                    wait_time += 5
                    
                    # Check if CAPTCHA is still there
                    try:
                        current_html = self.driver.page_source
                        if 'captcha' not in current_html.lower() and 'robot check' not in current_html.lower():
                            captcha_solved = True
                            logging.info("✅ CAPTCHA solved! Continuing...")
                            html = current_html  # Update HTML with the solved page
                        else:
                            logging.debug(f"Still waiting... ({wait_time}s elapsed)")
                    except Exception as e:
                        logging.error(f"Error checking CAPTCHA status: {e}")
                        break
                
                if not captcha_solved:
                    logging.error("❌ CAPTCHA not solved within 5 minutes. Skipping this page.")
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
        Override search_products to use Selenium with realistic search bar interaction
        """
        from urllib.parse import quote_plus
        from lxml import html as lhtml
        
        products = []
        
        try:
            # Navigate to Amazon homepage if not already there
            logging.info("🏠 Navigating to Amazon homepage...")
            self.driver.get(self.base_url)
            time.sleep(random.uniform(2, 3))
            
            # Find and interact with search bar
            logging.info(f"🔍 Searching for: {category_name}")
            
            try:
                # Find search input
                search_input = self.driver.find_element(By.CSS_SELECTOR, "input#twotabsearchtextbox")
                
                # Clear any existing text
                search_input.clear()
                time.sleep(random.uniform(0.3, 0.6))
                
                # Type search term character by character (human-like)
                for char in category_name:
                    search_input.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))  # Small delay between keystrokes
                
                logging.info("⌨️  Typed search term")
                time.sleep(random.uniform(0.5, 1.0))
                
                # Submit search (press Enter)
                search_input.send_keys(Keys.RETURN)
                logging.info("✅ Submitted search")
                
                # Wait for search results to load
                time.sleep(random.uniform(2, 4))
                
                # Get page source
                html_content = self.driver.page_source
                
                # Store the current URL as search URL
                search_url = self.driver.current_url
                
            except NoSuchElementException:
                logging.warning("⚠️  Search bar not found, falling back to direct URL navigation")
                # Fallback: use direct URL
                search_query = quote_plus(category_name)
                search_url = f"{self.base_url}/s?k={search_query}"
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
                
                # Skip author pages (URLs like /e/B0G3WYM4ZQ or /author/...)
                if '/e/' in href or '/author/' in href or '/-/e/' in href:
                    continue
                
                # Make absolute URL
                if href.startswith('/'):
                    full_url = f"{self.base_url}{href}"
                else:
                    full_url = href
                
                # Extract real URL from redirects
                real_url = self._extract_real_url(full_url)
                
                # Double-check after extraction (in case redirect resolved to author page)
                if '/e/' in real_url or '/author/' in real_url or '/-/e/' in real_url:
                    continue
                
                # Deduplicate
                if real_url not in seen:
                    seen.add(real_url)
                    unique_urls.append(real_url)
                    products.append(real_url)
                
                if len(products) >= max_products:
                    break
            
            logging.info(f"Found {len(products)} unique products for {category_name}")
            
            # Store the search URL for later navigation
            self.current_search_url = search_url
            
        except Exception as e:
            logging.error(f"Error searching for {category_name}: {e}")
        
        return products
    
    def scrape_product_details(self, product_url: str, category: Dict[str, Any]) -> Dict[str, Any]:
        """
        Override scrape_product_details to simulate clicking links from search page
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
            # Simplified strategy: Direct navigation with human-like delays
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
    
    def scan_asins(self, category: Dict[str, Any], max_pages: int = 20) -> List[str]:
        """
        Scan for ASINs from Amazon product listing pages
        
        Args:
            category: Category data from database
            max_pages: Maximum number of pages to scan (default: 20)
            
        Returns:
            List of ASIN strings
        """
        category_name = category['name']
        logging.info(f"Scanning ASINs for category: {category_name}")
        
        all_asins = []
        
        try:
            # Navigate to search page
            logging.info(f"🔍 Searching for: {category_name}")
            self.driver.get(self.base_url)
            time.sleep(random.uniform(1, 2))
            
            # Find and interact with search bar
            try:
                search_input = self.driver.find_element(By.CSS_SELECTOR, "input#twotabsearchtextbox")
                search_input.clear()
                time.sleep(random.uniform(0.1, 0.2))
                
                # Type search term character by character
                for char in category_name:
                    search_input.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                
                time.sleep(random.uniform(0.5, 1.0))
                search_input.send_keys(Keys.RETURN)
                logging.info("✅ Submitted search")
                
                # Wait for search results to load
                time.sleep(random.uniform(2, 4))
                
            except NoSuchElementException:
                logging.warning("⚠️  Search bar not found, using direct URL")
                from urllib.parse import quote_plus
                search_query = quote_plus(category_name)
                search_url = f"{self.base_url}/s?k={search_query}"
                self.driver.get(search_url)
                time.sleep(random.uniform(2, 4))
            
            # Scan pages
            for page_num in range(1, max_pages + 1):
                logging.info(f"📄 Scanning page {page_num}...")
                
                # Step 1: Scroll to bottom to fully load all products
                logging.debug("  Scrolling to bottom to load all products...")
                self._scroll_to_bottom()
                
                # Step 2: Extract ASINs from current page
                page_asins = self._extract_asins_from_page()
                
                if page_asins:
                    all_asins.extend(page_asins)
                    logging.info(f"  Found {len(page_asins)} ASINs on page {page_num} (total: {len(all_asins)})")
                else:
                    logging.warning(f"  No ASINs found on page {page_num}")
                
                # Step 3: Try to go to next page (if not on last page)
                if page_num < max_pages:
                    if not self._go_to_next_page():
                        logging.info(f"  No more pages available. Stopping at page {page_num}")
                        break
                    
                    # Wait for next page to load
                    time.sleep(random.uniform(2, 4))
            
            logging.info(f"✓ Completed scanning. Total ASINs found: {len(all_asins)}")
            
        except Exception as e:
            logging.error(f"Error scanning ASINs for {category_name}: {e}")
            self.stats['errors'] += 1
        
        return all_asins
    
    def _scroll_to_bottom(self):
        """
        Scroll to the bottom of the page to ensure all products are loaded
        Waits for pagination elements to be visible before scrolling
        """
        try:
            time.sleep(random.uniform(1, 2))  # Wait for any final lazy-loaded content
            
            # Trigger the load of pagination buttons
            self.driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });")
            
            # Wait for pagination buttons to be present (indicates page is fully loaded)
            logging.debug("  Waiting for pagination buttons...")
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.s-pagination-item"))
                )
                logging.debug("  ✓ Pagination buttons found")
            except TimeoutException:
                logging.warning("  ⚠️  Pagination buttons not found within 30s timeout, continuing anyway...")
            
            # Scroll to absolute bottom
            self.driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });")
            
        except Exception as e:
            logging.debug(f"Error scrolling to bottom: {e}")
            pass
    
    def _extract_asins_from_page(self) -> List[str]:
        """
        Extract ASINs from the current page using data-asin attribute
        Note: Should be called after scrolling to bottom to ensure all products are loaded
        
        Returns:
            List of ASIN strings
        """
        asins = []
        
        try:
            # Find all elements with data-asin attribute
            # Pattern: <div role="listitem" data-asin="B0FGY2WQ9Z" data-component-type="s-search-result">
            elements = self.driver.find_elements(
                By.XPATH,
                '//div[@data-component-type="s-search-result"][@data-asin]'
            )
            
            for element in elements:
                asin = element.get_attribute('data-asin')
                if asin and asin not in asins:
                    asins.append(asin)
            
            # Alternative: try finding within the search results container
            if not asins:
                container = self.driver.find_elements(
                    By.XPATH,
                    '//span[@data-component-type="s-search-results"]//div[@data-asin]'
                )
                for element in container:
                    asin = element.get_attribute('data-asin')
                    if asin and asin not in asins:
                        asins.append(asin)
            
        except Exception as e:
            logging.debug(f"Error extracting ASINs: {e}")
        
        return asins
    
    def _go_to_next_page(self) -> bool:
        """
        Navigate to the next page by clicking pagination button
        Note: Should be called after scanning ASINs (pagination should already be visible)
        
        Returns:
            True if successfully navigated to next page, False otherwise
        """
        try:
            # Find the next page button
            # Pattern: <a href="..." role="button" tabindex="0" aria-label="Go to page 2" class="s-pagination-item s-pagination-button s-pagination-button-accessibility">2</a>
            
            # Find the button that represents the next page number
            current_page = self._get_current_page_number()
            
            if current_page:
                next_page_num = current_page + 1
                # Look for button with text matching next page number
                next_button = self.driver.find_elements(
                    By.XPATH,
                    f'//a[@role="button"][contains(@class, "s-pagination-button")][contains(@aria-label, "Go to page {next_page_num}")]'
                )
                
                if not next_button:
                    # Try alternative: find button with text matching page number
                    next_button = self.driver.find_elements(
                        By.XPATH,
                        f'//a[@role="button"][contains(@class, "s-pagination-button")][text()="{next_page_num}"]'
                    )
                
                if next_button:
                    # Scroll to button to ensure it's visible
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button[0])
                    time.sleep(random.uniform(0.5, 1.0))
                    
                    # Click the button
                    next_button[0].click()
                    logging.info(f"  → Clicked pagination button for page {next_page_num}")
                    return True
            
            # Fallback: try to find "Next" button
            next_buttons = self.driver.find_elements(
                By.XPATH,
                '//a[@aria-label="Go to next page"]'
            )
            
            if next_buttons:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_buttons[0])
                time.sleep(random.uniform(0.5, 1.0))
                next_buttons[0].click()
                logging.info("  → Clicked 'Next' pagination button")
                return True
            
            return False
            
        except Exception as e:
            logging.debug(f"Error navigating to next page: {e}")
            return False
    
    def _get_current_page_number(self) -> Optional[int]:
        """Get the current page number from URL or pagination"""
        try:
            # Try to get from URL
            current_url = self.driver.current_url
            if 'page=' in current_url:
                from urllib.parse import urlparse, parse_qs
                parsed = urlparse(current_url)
                query_params = parse_qs(parsed.query)
                if 'page' in query_params:
                    return int(query_params['page'][0])
            
            # Try to get from pagination (find selected/current page)
            current_page_elem = self.driver.find_elements(
                By.XPATH,
                '//span[@aria-current="page"][contains(@class, "s-pagination-item")]'
            )
            if current_page_elem:
                page_text = current_page_elem[0].text.strip()
                if page_text.isdigit():
                    return int(page_text)
            
            # Default to page 1 if not found
            return 1
            
        except Exception as e:
            logging.debug(f"Error getting current page number: {e}")
            return 1
    
    def save_asins(self, category: Dict[str, Any], asins: List[str]):
        """
        Save ASINs to category-specific file: amazon_asin_<category_name>.json (thread-safe)
        File contains just the list of ASINs
        
        Args:
            category: Category data
            asins: List of ASIN strings
        """
        category_name = category['name']
        safe_name = self._sanitize_filename(category_name)
        output_file = os.path.join(self.output_dir, f"amazon_asin_{safe_name}.json")
        
        # Thread-safe file write using retry mechanism
        max_retries = 5
        retry_delay = 0.1
        
        for attempt in range(max_retries):
            try:
                # Save ASINs as a simple list (atomic write using temp file)
                temp_file = output_file + '.tmp'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(asins, f, indent=2, ensure_ascii=False)
                    f.flush()
                    os.fsync(f.fileno())  # Ensure data is written to disk
                
                # Atomic rename
                os.replace(temp_file, output_file)
                
                logging.info(f"✓ Saved {len(asins)} ASINs for {category_name} to {output_file}")
                return
                
            except (IOError, OSError) as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                logging.error(f"Error saving ASINs for {category_name} (attempt {attempt + 1}/{max_retries}): {e}")
        
        # If all retries failed, log error
        logging.error(f"Failed to save ASINs for {category_name} after {max_retries} attempts")

