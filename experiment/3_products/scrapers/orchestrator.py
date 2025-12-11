#!/usr/bin/env python3
"""
Orchestrator for running scrapers across multiple categories
"""

import json
import logging
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from utils.db_connector import DatabaseConnection, get_target_categories, load_categories
from scrapers.amazon_scraper import AmazonScraper
from scrapers.selenium_scraper import SeleniumAmazonScraper


class ScraperOrchestrator:
    """Orchestrates scraping across multiple categories and websites"""
    
    def __init__(self, config_file: str = "../config/scraping_config.json", asin_dir: Optional[str] = None):
        """
        Initialize orchestrator
        
        Args:
            config_file: Path to configuration file
            use_selenium: Whether to use Selenium scraper (for ASIN scanning)
            asin_dir: Optional directory where ASIN files are located
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.asin_dir = asin_dir
        
        # Setup logging
        self._setup_logging()
        
        # Initialize scrapers
        self.scrapers = {}
        self._initialize_scrapers()
        
        # Statistics
        self.stats = {
            'start_time': None,
            'end_time': None,
            'categories_processed': 0,
            'total_products_scraped': 0,
            'total_products_with_attributes': 0,
            'errors': 0
        }
        
        # Thread lock for thread-safe operations
        self.progress_lock = threading.Lock()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        config_path = os.path.join(os.path.dirname(__file__), self.config_file)
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            logging.warning(f"Config file not found: {config_path}")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'target_categories': [],
            'websites': ['amazon'],
            'products_per_category_per_website': 5,
            'rate_limiting': {
                'delay_range': [2.0, 4.0],
                'max_retries': 3,
                'timeout': 15
            },
            'output': {
                'directory': '../output'
            }
        }
    
    def _setup_logging(self):
        """Setup logging configuration"""
        output_dir = os.path.join(
            os.path.dirname(__file__),
            self.config.get('output', {}).get('directory', '../output')
        )
        os.makedirs(output_dir, exist_ok=True)
        
        log_file = os.path.join(output_dir, 'orchestrator.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("=" * 80)
        self.logger.info("AMAZON SCRAPER ORCHESTRATOR")
        self.logger.info("=" * 80)
    
    def _initialize_scrapers(self):
        """Initialize website scrapers"""
        output_dir = os.path.join(
            os.path.dirname(__file__),
            self.config.get('output', {}).get('directory', '../output')
        )
        
        websites = self.config.get('websites', ['amazon'])
        
        for website in websites:
            if website.lower() == 'amazon':
                self.scrapers['amazon'] = SeleniumAmazonScraper(
                    self.config,
                    output_dir=output_dir,
                    browser='Local',
                    headless=True
                )
                self.logger.info(f"✓ Initialized Selenium Amazon scraper")
            # Add more scrapers here as needed
    
    def load_categories_from_db(self, category_names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Load categories from database
        
        Args:
            category_names: Optional list of specific category names to load
            
        Returns:
            List of category dictionaries
        """
        self.logger.info("Loading categories from database...")
        
        try:
            with DatabaseConnection() as cursor:
                if category_names:
                    categories = get_target_categories(cursor, category_names)
                    self.logger.info(f"Loaded {len(categories)} target categories")
                else:
                    categories_dict = load_categories(cursor)
                    categories = list(categories_dict.values())
                    self.logger.info(f"Loaded {len(categories)} total categories")
                
                return categories
        
        except Exception as e:
            self.logger.error(f"Failed to load categories from database: {e}")
            return []
    
    def _is_category_scraped(self, category_name: str, asin_count: int, output_dir: str) -> bool:
        """
        Check if a category's products are already scraped
        
        A category is considered scraped when:
        - The products file exists
        - The products file contains a list with count == asin_count
        
        Args:
            category_name: Name of the category
            asin_count: Number of ASINs for this category
            output_dir: Output directory where products file should be
            
        Returns:
            True if category is already scraped, False otherwise
        """
        safe_name = self._sanitize_filename(category_name)
        products_file = os.path.join(output_dir, f"amazon_products_{safe_name}.json")
        
        if not os.path.exists(products_file):
            return False
        
        try:
            with open(products_file, 'r', encoding='utf-8') as f:
                products = json.load(f)
            
            # Check if file contains a list with matching count
            if isinstance(products, list) and len(products) == asin_count:
                return True
            
            return False
            
        except (json.JSONDecodeError, IOError, TypeError) as e:
            # If file is corrupted or can't be read, assume not scraped
            self.logger.debug(f"Error checking products file for {category_name}: {e}")
            return False
    
    def _scrape_single_asin(self, asin: str, category: Dict[str, Any], scraper: SeleniumAmazonScraper, 
                            asin_index: int, total_asins: int) -> Dict[str, Any]:
        """
        Worker function to scrape a single ASIN
        
        Args:
            asin: ASIN to scrape
            category: Category data
            scraper: Scraper instance to use
            asin_index: Index of this ASIN (for logging)
            total_asins: Total number of ASINs (for logging)
            
        Returns:
            Product data dictionary or None if failed
        """
        if not asin or not isinstance(asin, str):
            return None
        
        try:
            # Construct product URL
            product_url = f"{scraper.base_url}/dp/{asin}"
            
            # Scrape product details
            product_data = scraper.scrape_product_details(product_url, category)
            product_data['asin'] = asin
            product_data['position'] = asin_index
            
            return product_data
            
        except Exception as e:
            self.logger.error(f"Error scraping ASIN {asin} (position {asin_index}): {e}")
            with self.progress_lock:
                self.stats['errors'] += 1
            return None
    
    def scrape_products(self, category_names: Optional[List[str]] = None, num_workers: int = 1, force: bool = False):
        """
        Run scraping orchestrator
        
        Args:
            category_names: Optional list of category names to scrape
                           If None or empty, loads ALL categories from database
                           Otherwise, uses target_categories from config if available
            num_workers: Number of parallel browser instances (default: 1, sequential)
            force: If True, force scraping even if category is already scraped (overwrites old results)
        """
        self.stats['start_time'] = datetime.now()
        self.logger.info(f"Starting scraping run at {self.stats['start_time']}")
        
        # Determine which categories to load
        # If category_names is None or empty, load ALL categories from database
        # Otherwise, use the provided category names or from config
        if category_names is None or len(category_names) == 0:
            # Try config first, but if empty, load all
            category_names = self.config.get('target_categories', [])
            if not category_names:
                self.logger.info("No specific categories provided - will scrape ALL categories from database")
                categories = self.load_categories_from_db(None)  # Load all categories
            else:
                self.logger.info(f"Target categories from config: {', '.join(category_names)}")
                categories = self.load_categories_from_db(category_names)
        else:
            self.logger.info(f"Target categories: {', '.join(category_names)}")
            categories = self.load_categories_from_db(category_names)
        
        if not categories:
            self.logger.error("No categories loaded from database")
            return
        
        # Log ASIN directory if specified
        if self.asin_dir:
            self.logger.info(f"ASIN directory: {self.asin_dir}")
        else:
            output_dir = os.path.join(
                os.path.dirname(__file__),
                self.config.get('output', {}).get('directory', '../output')
            )
            self.logger.info(f"ASIN directory: {output_dir} (default)")
        
        # Verify that we have matching categories (only if specific categories were requested)
        if category_names and len(category_names) > 0:
            loaded_names = {cat['name'] for cat in categories}
            requested_names = set(category_names)
            missing = requested_names - loaded_names
            if missing:
                self.logger.warning(f"Categories not found in database: {', '.join(missing)}")
        
        # Get output directory
        output_dir = os.path.join(
            os.path.dirname(__file__),
            self.config.get('output', {}).get('directory', '../output')
        )
        os.makedirs(output_dir, exist_ok=True)
        
        max_products = self.config.get('products_per_category_per_website', None)  # None = all products
        
        self.logger.info(f"\n📋 Total categories: {len(categories)}")
        self.logger.info(f"🔧 Parallel workers per category: {num_workers}")
        if max_products:
            self.logger.info(f"📦 Max products per category: {max_products}")
        
        # Process categories sequentially (one by one)
        for cat_idx, category in enumerate(categories, 1):
            category_name = category['name']
            safe_name = self._sanitize_filename(category_name)
            
            self.logger.info(f"\n{'='*80}")
            self.logger.info(f"[{cat_idx}/{len(categories)}] PROCESSING CATEGORY: {category_name}")
            self.logger.info(f"{'='*80}")
            
            # Step 1: Load ASINs from file
            asin_directory = self.asin_dir if self.asin_dir else output_dir
            asin_file = os.path.join(asin_directory, f"amazon_asin_{safe_name}.json")
            
            if not os.path.exists(asin_file):
                self.logger.warning(f"ASIN file not found: {asin_file} - skipping category")
                continue
            
            try:
                with open(asin_file, 'r', encoding='utf-8') as f:
                    asins = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.logger.error(f"Error loading ASIN file {asin_file}: {e} - skipping category")
                continue
            
            if not isinstance(asins, list):
                self.logger.error(f"Invalid ASIN file format: expected list, got {type(asins)} - skipping category")
                continue
            
            if not asins:
                self.logger.warning(f"No ASINs found in {asin_file} - skipping category")
                continue
            
            # Limit ASINs if specified
            original_count = len(asins)
            if max_products and max_products > 0:
                asins = asins[:max_products]
                if len(asins) < original_count:
                    self.logger.info(f"Limited ASINs: {original_count} -> {len(asins)}")
            
            # Check if category is already scraped (unless force=True)
            if not force:
                if self._is_category_scraped(category_name, len(asins), output_dir):
                    self.logger.info(f"⏭️  Category {category_name} already scraped ({len(asins)} products) - skipping")
                    self.logger.info(f"   (Use --categories to force re-scraping)")
                    continue
                else:
                    self.logger.info(f"Category {category_name} not yet scraped or incomplete - proceeding")
            else:
                self.logger.info(f"🔄 Force mode: Re-scraping category {category_name} (will overwrite existing results)")
            
            self.logger.info(f"Loaded {len(asins)} ASINs for {category_name}")
            
            # Step 2: Process ASINs in parallel using worker pool
            scraped_products = []
            completed_count = 0
            
            if num_workers > 1:
                # Parallel processing with multiple scrapers
                self.logger.info(f"🚀 Processing {len(asins)} ASINs with {num_workers} parallel workers...")
                
                # Create one scraper per worker (reused for all ASINs in this category)
                # Use a list for easier indexing
                scrapers = []
                for worker_id in range(num_workers):
                    scrapers.append(SeleniumAmazonScraper(
                        self.config, 
                        output_dir=output_dir, 
                        browser='Local', 
                        headless=True
                    ))
                
                try:
                    with ThreadPoolExecutor(max_workers=num_workers) as executor:
                        # Submit all ASIN scraping tasks
                        # Each task will use a scraper based on its index (round-robin assignment)
                        future_to_asin = {}
                        for asin_idx, asin in enumerate(asins, 1):
                            # Assign scraper based on ASIN index (round-robin)
                            scraper = scrapers[(asin_idx - 1) % num_workers]
                            future = executor.submit(
                                self._scrape_single_asin,
                                asin, category, scraper, asin_idx, len(asins)
                            )
                            future_to_asin[future] = (asin, asin_idx)
                        
                        # Collect results as they complete
                        for future in as_completed(future_to_asin):
                            asin, asin_idx = future_to_asin[future]
                            try:
                                product_data = future.result()
                                if product_data:
                                    scraped_products.append(product_data)
                                    completed_count += 1
                                    if completed_count % 10 == 0 or completed_count == len(asins):
                                        self.logger.info(f"  Progress: {completed_count}/{len(asins)} ASINs completed")
                            except Exception as e:
                                self.logger.error(f"Exception processing ASIN {asin} (position {asin_idx}): {e}")
                finally:
                    # Close all scrapers for this category
                    for worker_id, scraper in enumerate(scrapers, 1):
                        if hasattr(scraper, 'close'):
                            try:
                                scraper.close()
                            except Exception as e:
                                self.logger.warning(f"Error closing scraper {worker_id}: {e}")
            else:
                # Sequential processing (single scraper)
                self.logger.info(f"🔄 Processing {len(asins)} ASINs sequentially...")
                scraper = SeleniumAmazonScraper(
                    self.config, 
                    output_dir=output_dir, 
                    browser='Local', 
                    headless=True
                )
                try:
                    for asin_idx, asin in enumerate(asins, 1):
                        product_data = self._scrape_single_asin(asin, category, scraper, asin_idx, len(asins))
                        if product_data:
                            scraped_products.append(product_data)
                            completed_count += 1
                            if completed_count % 10 == 0 or completed_count == len(asins):
                                self.logger.info(f"  Progress: {completed_count}/{len(asins)} ASINs completed")
                finally:
                    if hasattr(scraper, 'close'):
                        try:
                            scraper.close()
                        except:
                            pass
            
            # Step 3: Save all products for this category to category-specific file
            products_file = os.path.join(output_dir, f"amazon_products_{safe_name}.json")
            
            # Remove temporary analysis data before saving
            for product in scraped_products:
                product.pop('_analysis', None)
                product.pop('_html_snippet', None)
            
            with open(products_file, 'w', encoding='utf-8') as f:
                json.dump(scraped_products, f, indent=2, ensure_ascii=False)
            
            products_with_attributes = sum(1 for p in scraped_products if p.get('attributes'))
            
            # Update statistics
            self.stats['categories_processed'] += 1
            self.stats['total_products_scraped'] += len(scraped_products)
            self.stats['total_products_with_attributes'] += products_with_attributes
            
            self.logger.info(f"✓ Completed category: {category_name}")
            self.logger.info(f"  ASINs processed: {len(asins)}")
            self.logger.info(f"  Products scraped: {len(scraped_products)}")
            self.logger.info(f"  Products with attributes: {products_with_attributes}")
            self.logger.info(f"  Saved to: {products_file}")
        
        # Finalize
        self.stats['end_time'] = datetime.now()
        duration = self.stats['end_time'] - self.stats['start_time']
        
        self.logger.info(f"\n{'='*80}")
        self.logger.info("SCRAPING RUN COMPLETED")
        self.logger.info(f"{'='*80}")
        self.logger.info(f"Duration: {duration}")
        self.logger.info(f"Categories processed: {self.stats['categories_processed']}")
        self.logger.info(f"Total products scraped: {self.stats['total_products_scraped']}")
        self.logger.info(f"Products with attributes: {self.stats['total_products_with_attributes']}")
        self.logger.info(f"Errors: {self.stats['errors']}")
        
        # Save statistics
        self._save_statistics()
    
    def _load_asin_progress(self) -> Dict[str, Any]:
        """Load ASIN scanning progress from file"""
        output_dir = os.path.join(
            os.path.dirname(__file__),
            self.config.get('output', {}).get('directory', '../output')
        )
        progress_file = os.path.join(output_dir, 'amazon_asin_progress.json')
        
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.logger.warning(f"Error loading progress file: {e}")
                return {}
        
        return {}
    
    def _save_asin_progress(self, progress: Dict[str, Any]):
        """Save ASIN scanning progress to file (thread-safe)"""
        output_dir = os.path.join(
            os.path.dirname(__file__),
            self.config.get('output', {}).get('directory', '../output')
        )
        os.makedirs(output_dir, exist_ok=True)
        progress_file = os.path.join(output_dir, 'amazon_asin_progress.json')
        
        with self.progress_lock:
            try:
                with open(progress_file, 'w', encoding='utf-8') as f:
                    json.dump(progress, f, indent=2, ensure_ascii=False)
            except IOError as e:
                self.logger.error(f"Error saving progress file: {e}")
    
    def _is_category_completed(self, category: Dict[str, Any]) -> bool:
        """
        Check if a category has already been processed by checking category-specific file
        A category is considered completed if its file exists with at least 1 ASIN
        
        Args:
            category: Category data (needs 'name' field)
            
        Returns:
            True if category is already completed, False otherwise
        """
        category_name = category['name']
        safe_name = self._sanitize_filename(category_name)
        
        output_dir = os.path.join(
            os.path.dirname(__file__),
            self.config.get('output', {}).get('directory', '../output')
        )
        asin_file = os.path.join(output_dir, f'amazon_asin_{safe_name}.json')
        
        if not os.path.exists(asin_file):
            return False
        
        try:
            with self.progress_lock:  # Thread-safe file read
                with open(asin_file, 'r', encoding='utf-8') as f:
                    asins = json.load(f)
            
            # Check if file contains a list with at least 1 ASIN
            if isinstance(asins, list) and len(asins) > 0:
                return True
            
            return False
            
        except (json.JSONDecodeError, IOError, TypeError) as e:
            # If file is corrupted or can't be read, assume not completed
            self.logger.debug(f"Error checking category {category_name} in ASIN file: {e}")
            return False
    
    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a string to be used as a filename
        
        Args:
            name: String to sanitize
            
        Returns:
            Sanitized string
        """
        # Replace spaces and special characters
        safe = name.replace(' ', '_').replace("'", '').replace('"', '')
        safe = ''.join(c for c in safe if c.isalnum() or c in ('_', '-'))
        return safe.lower()
    
    def _update_progress(self, category_id: int, category_name: str, asin_count: int, progress: Dict[str, Any]):
        """Update progress tracking (thread-safe)"""
        with self.progress_lock:
            if 'completed_category_ids' not in progress:
                progress['completed_category_ids'] = []
            if 'category_details' not in progress:
                progress['category_details'] = {}
            
            progress['completed_category_ids'].append(category_id)
            progress['category_details'][str(category_id)] = {
                'category_name': category_name,
                'asin_count': asin_count,
                'completed_at': datetime.now().isoformat()
            }
            
            # Remove duplicates
            progress['completed_category_ids'] = list(set(progress['completed_category_ids']))
    
    def _process_category_worker(self, category: Dict[str, Any], max_pages: int, progress: Dict[str, Any], 
                                  worker_id: int, total_categories: int, category_index: int, scraper: SeleniumAmazonScraper):
        """
        Worker function to process a single category (for parallel processing)
        
        Args:
            category: Category data to process
            max_pages: Maximum pages to scan
            progress: Shared progress dictionary
            worker_id: ID of the worker thread
            total_categories: Total number of categories
            category_index: Index of this category in the list
            scraper: Reusable scraper instance for this worker (reuses browser)
        """
        category_id = category['id']
        category_name = category['name']
        
        try:
            self.logger.info(f"{'='*80}")
            self.logger.info(f"[Worker {worker_id}] [{category_index}/{total_categories}] SCANNING ASINs FOR: {category_name}")
            self.logger.info(f"{'='*80}")
            
            # Scan ASINs (reuse the same browser)
            asins = scraper.scan_asins(category, max_pages=max_pages)
            
            # Save ASINs (thread-safe via lock in save_asins)
            scraper.save_asins(category, asins)
            
            # Update progress (thread-safe)
            self._update_progress(category_id, category_name, len(asins), progress)
            self._save_asin_progress(progress)
            
            # Update statistics (thread-safe)
            with self.progress_lock:
                self.stats['categories_processed'] += 1
            
            self.logger.info(f"[Worker {worker_id}] ✓ Completed ASIN scan for {category_name}")
            self.logger.info(f"[Worker {worker_id}]   Total ASINs found: {len(asins)}")
            
            # Show progress summary (count from category-specific ASIN files)
            with self.progress_lock:
                output_dir = os.path.join(
                    os.path.dirname(__file__),
                    self.config.get('output', {}).get('directory', '../output')
                )
                completed_now = 0
                if os.path.exists(output_dir):
                    for filename in os.listdir(output_dir):
                        if filename.startswith('amazon_asin_') and filename.endswith('.json'):
                            try:
                                filepath = os.path.join(output_dir, filename)
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    asins = json.load(f)
                                if isinstance(asins, list) and len(asins) > 0:
                                    completed_now += 1
                            except (json.JSONDecodeError, IOError):
                                pass
                remaining = total_categories - completed_now
                self.logger.info(f"[Worker {worker_id}] 📊 Progress: {completed_now}/{total_categories} completed ({remaining} remaining)")
            
            return {'success': True, 'category_id': category_id, 'asin_count': len(asins)}
            
        except Exception as e:
            self.logger.error(f"[Worker {worker_id}] Error scanning ASINs for {category_name}: {e}")
            with self.progress_lock:
                self.stats['errors'] += 1
            return {'success': False, 'category_id': category_id, 'error': str(e)}
    
    def run_asin_scan(self, category_names: Optional[List[str]] = None, max_pages: int = 20, 
                      resume: bool = True, num_workers: int = 1):
        """
        Run ASIN scanning mode
        
        Args:
            category_names: Optional list of category names to scan
            max_pages: Maximum number of pages to scan per category
            resume: If True, skip categories that have already been processed
            num_workers: Number of parallel browser instances (default: 1, sequential)
        """
        self.stats['start_time'] = datetime.now()
        self.logger.info(f"Starting ASIN scanning at {self.stats['start_time']}")
        
        # Load progress (for statistics only, completion check uses category-specific files)
        progress = self._load_asin_progress() if resume else {}
        
        if resume:
            # Count completed categories from category-specific files
            output_dir = os.path.join(
                os.path.dirname(__file__),
                self.config.get('output', {}).get('directory', '../output')
            )
            completed_count = 0
            if os.path.exists(output_dir):
                for filename in os.listdir(output_dir):
                    if filename.startswith('amazon_asin_') and filename.endswith('.json'):
                        try:
                            filepath = os.path.join(output_dir, filename)
                            with open(filepath, 'r', encoding='utf-8') as f:
                                asins = json.load(f)
                            if isinstance(asins, list) and len(asins) > 0:
                                completed_count += 1
                        except (json.JSONDecodeError, IOError):
                            pass
            
            if completed_count > 0:
                self.logger.info(f"📊 Found {completed_count} previously completed categories (with ASIN files)")
                self.logger.info("  (Use --no-resume to reprocess all categories)")
        
        # Determine which categories to load
        # If category_names is None or empty, load ALL categories from database
        # Otherwise, use the provided category names
        if category_names:
            self.logger.info(f"Target categories: {', '.join(category_names)}")
        else:
            self.logger.info("No specific categories provided - will scan ALL categories from database")
        
        self.logger.info(f"Max pages per category: {max_pages}")
        
        # Load categories from database
        # Pass None to load all categories if no specific categories provided
        categories = self.load_categories_from_db(category_names if category_names else None)
        
        if not categories:
            self.logger.error("No categories loaded from database")
            return
        
        # Filter out already completed categories
        categories_to_process = []
        skipped_count = 0
        for idx, category in enumerate(categories, 1):
            category_id = category['id']
            category_name = category['name']
            
            # Check if already completed (check amazon_asin.json directly)
            if resume and self._is_category_completed(category):
                skipped_count += 1
                if skipped_count <= 5 or idx % 50 == 0:  # Log first 5 and every 50th
                    self.logger.info(f"⏭️  [{idx}/{len(categories)}] Skipping {category_name} (already has ASINs)")
                continue
            
            categories_to_process.append((idx, category))
        
        if skipped_count > 0:
            self.logger.info(f"⏭️  Skipped {skipped_count} already completed categories")
        
        total_categories = len(categories)
        categories_to_process_count = len(categories_to_process)
        self.logger.info(f"\n📋 Total categories: {total_categories}")
        self.logger.info(f"📋 Categories to process: {categories_to_process_count}")
        self.logger.info(f"🔧 Parallel workers: {num_workers}")
        
        if not categories_to_process:
            self.logger.info("✅ All categories already completed!")
            return
        
        # Process categories
        if num_workers > 1:
            # Parallel processing with multiple browsers
            self.logger.info(f"\n🚀 Starting parallel processing with {num_workers} workers...")
            
            # Create one scraper per worker (reused for all categories in that worker)
            output_dir = os.path.join(
                os.path.dirname(__file__),
                self.config.get('output', {}).get('directory', '../output')
            )
            scrapers = {}
            for worker_id in range(1, num_workers + 1):
                scrapers[worker_id] = SeleniumAmazonScraper(self.config, output_dir=output_dir, browser='Local', headless=True)
                self.logger.info(f"  Created browser for worker {worker_id}")
            
            try:
                with ThreadPoolExecutor(max_workers=num_workers) as executor:
                    # Submit all tasks
                    future_to_category = {}
                    for idx, category in categories_to_process:
                        worker_id = (idx % num_workers) + 1
                        scraper = scrapers[worker_id]
                        future = executor.submit(
                            self._process_category_worker,
                            category, max_pages, progress, 
                            worker_id, total_categories, idx, scraper
                        )
                        future_to_category[future] = (idx, category)
                    
                    # Process completed tasks
                    for future in as_completed(future_to_category):
                        idx, category = future_to_category[future]
                        try:
                            result = future.result()
                            if result['success']:
                                self.logger.debug(f"Category {category['name']} completed successfully")
                            else:
                                self.logger.error(f"Category {category['name']} failed: {result.get('error', 'Unknown error')}")
                        except Exception as e:
                            self.logger.error(f"Exception processing category {category['name']}: {e}")
            finally:
                # Close all scrapers after all work is done
                self.logger.info(f"\n🔒 Closing all browser instances...")
                for worker_id, scraper in scrapers.items():
                    if hasattr(scraper, 'close'):
                        try:
                            scraper.close()
                            self.logger.info(f"  ✓ Closed browser for worker {worker_id}")
                        except Exception as e:
                            self.logger.warning(f"  ⚠️  Error closing browser for worker {worker_id}: {e}")
        else:
            # Sequential processing (original behavior - create scraper once)
            self.logger.info(f"\n🔄 Starting sequential processing...")
            output_dir = os.path.join(
                os.path.dirname(__file__),
                self.config.get('output', {}).get('directory', '../output')
            )
            scraper = SeleniumAmazonScraper(self.config, output_dir=output_dir, browser='Local', headless=True)
            try:
                for idx, category in categories_to_process:
                    self._process_category_worker(
                        category, max_pages, progress,
                        1, total_categories, idx, scraper
                    )
            finally:
                # Close scraper after all work is done
                if hasattr(scraper, 'close'):
                    try:
                        scraper.close()
                        self.logger.info("✓ Closed browser")
                    except:
                        pass
        
        # Finalize
        self.stats['end_time'] = datetime.now()
        duration = self.stats['end_time'] - self.stats['start_time']
        
        # Final progress summary (from category-specific ASIN files)
        output_dir = os.path.join(
            os.path.dirname(__file__),
            self.config.get('output', {}).get('directory', '../output')
        )
        final_completed = 0
        total_asins = 0
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                if filename.startswith('amazon_asin_') and filename.endswith('.json'):
                    try:
                        filepath = os.path.join(output_dir, filename)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            asins = json.load(f)
                        if isinstance(asins, list):
                            if len(asins) > 0:
                                final_completed += 1
                            total_asins += len(asins)
                    except (json.JSONDecodeError, IOError):
                        pass
        
        self.logger.info(f"\n{'='*80}")
        self.logger.info("ASIN SCANNING COMPLETED")
        self.logger.info(f"{'='*80}")
        self.logger.info(f"Duration: {duration}")
        self.logger.info(f"Categories processed: {self.stats['categories_processed']}")
        self.logger.info(f"Total categories completed: {final_completed}/{total_categories}")
        self.logger.info(f"Total ASINs collected: {total_asins}")
        self.logger.info(f"Errors: {self.stats['errors']}")
        
        # Cleanup Selenium drivers if present (for sequential mode)
        # Note: In parallel mode, each worker closes its own driver
        for scraper in self.scrapers.values():
            if hasattr(scraper, 'close'):
                try:
                    scraper.close()
                except:
                    pass
    
    def _save_statistics(self):
        """Save run statistics"""
        output_dir = os.path.join(
            os.path.dirname(__file__),
            self.config.get('output', {}).get('directory', '../output')
        )
        
        stats_file = os.path.join(output_dir, 'scraping_statistics.json')
        
        # Convert datetime to string
        stats_to_save = self.stats.copy()
        stats_to_save['start_time'] = str(stats_to_save['start_time'])
        stats_to_save['end_time'] = str(stats_to_save['end_time'])
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_to_save, f, indent=2)
        
        self.logger.info(f"✓ Saved statistics to {stats_file}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Amazon Product Scraper with Pattern Learning')
    parser.add_argument(
        '--categories',
        nargs='+',
        help='Category names to scrape (e.g., "Laptop" "Smartphone")'
    )
    parser.add_argument(
        '--config',
        default='../config/scraping_config.json',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Run in sample mode with predefined categories'
    )
    parser.add_argument(
        '--scan-asin',
        action='store_true',
        help='Scan for ASINs only (uses Selenium scraper)'
    )
    parser.add_argument(
        '--scrape-products',
        action='store_true',
        help='Scrape product details from ASINs (uses Selenium scraper, requires ASIN files)'
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        default=20,
        help='Maximum number of pages to scan per category (default: 20, only used with --scan-asin)'
    )
    parser.add_argument(
        '--no-resume',
        action='store_true',
        help='Do not resume from previous progress (reprocess all categories, only used with --scan-asin)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='Number of parallel browser instances (default: 1, sequential). Used with --scan-asin or --scrape-products'
    )
    parser.add_argument(
        '--asin-dir',
        type=str,
        default=None,
        help='Directory where ASIN files (amazon_asin_<category_name>.json) are located'
    )
    
    args = parser.parse_args()
    
    # Validate mutually exclusive modes
    if args.scan_asin and args.scrape_products:
        parser.error("--scan-asin and --scrape-products cannot be used together. Choose one mode.")
    
    # Initialize orchestrator
    # Use Selenium for both ASIN scanning and product scraping (since AmazonScraper doesn't work)
    orchestrator = ScraperOrchestrator(config_file=args.config, asin_dir=args.asin_dir)
    
    # Determine categories
    if args.scan_asin:
        # ASIN scanning mode
        resume = not args.no_resume
        num_workers = max(1, args.workers)  # Ensure at least 1 worker
        
        if args.categories:
            orchestrator.run_asin_scan(
                category_names=args.categories, 
                max_pages=args.max_pages, 
                resume=resume,
                num_workers=num_workers
            )
        else:
            # No categories provided - scan ALL categories from database
            orchestrator.run_asin_scan(
                max_pages=args.max_pages, 
                resume=resume,
                num_workers=num_workers
            )
    elif args.scrape_products:
        num_workers = max(1, args.workers)  # Ensure at least 1 worker
        
        if args.categories:
            # Categories explicitly provided - force scraping (overwrite old results)
            print(f"\n🛒 Running PRODUCT SCRAPING MODE with categories: {', '.join(args.categories)}")
            print(f"   (Force mode: will overwrite existing results)")
            orchestrator.scrape_products(category_names=args.categories, num_workers=num_workers, force=True)
        else:
            # No categories provided - scrape ALL categories from database (skip already scraped)
            print(f"\n🛒 Running PRODUCT SCRAPING MODE - will scrape ALL categories from database")
            print(f"   (Will skip categories that are already scraped)")
            orchestrator.scrape_products(category_names=None, num_workers=num_workers, force=False)
    else:
        raise NotImplementedError('Please specify a mode to run')


if __name__ == "__main__":
    main()

