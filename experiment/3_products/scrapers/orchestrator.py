#!/usr/bin/env python3
"""
Orchestrator for running scrapers across multiple categories
"""

import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from utils.db_connector import DatabaseConnection, get_target_categories, load_categories
from scrapers.amazon_scraper import AmazonScraper


class ScraperOrchestrator:
    """Orchestrates scraping across multiple categories and websites"""
    
    def __init__(self, config_file: str = "../config/scraping_config.json"):
        """
        Initialize orchestrator
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
        
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
            'products_per_category_per_website': 10,
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
                self.scrapers['amazon'] = AmazonScraper(
                    self.config,
                    output_dir=output_dir
                )
                self.logger.info(f"✓ Initialized Amazon scraper")
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
    
    def run(self, category_names: Optional[List[str]] = None):
        """
        Run scraping orchestrator
        
        Args:
            category_names: Optional list of category names to scrape
                           If None, uses target_categories from config
        """
        self.stats['start_time'] = datetime.now()
        self.logger.info(f"Starting scraping run at {self.stats['start_time']}")
        
        # Get categories
        if category_names is None:
            category_names = self.config.get('target_categories', [])
        
        if not category_names:
            self.logger.error("No target categories specified")
            return
        
        self.logger.info(f"Target categories: {', '.join(category_names)}")
        
        # Load categories from database
        categories = self.load_categories_from_db(category_names)
        
        if not categories:
            self.logger.error("No categories loaded from database")
            return
        
        # Process each category with each scraper
        max_products = self.config.get('products_per_category_per_website', 10)
        
        for category in categories:
            category_name = category['name']
            self.logger.info(f"\n{'='*80}")
            self.logger.info(f"CATEGORY: {category_name}")
            self.logger.info(f"{'='*80}")
            
            for website, scraper in self.scrapers.items():
                self.logger.info(f"\nProcessing with {website} scraper...")
                
                try:
                    result = scraper.process_category(category, max_products=max_products)
                    
                    # Update statistics
                    self.stats['categories_processed'] += 1
                    self.stats['total_products_scraped'] += result.get('products_scraped', 0)
                    self.stats['total_products_with_attributes'] += result.get('products_with_attributes', 0)
                    
                    self.logger.info(f"✓ Completed {category_name} on {website}")
                    self.logger.info(f"  Products scraped: {result.get('products_scraped', 0)}")
                    self.logger.info(f"  Products with attributes: {result.get('products_with_attributes', 0)}")
                
                except Exception as e:
                    self.logger.error(f"Error processing {category_name} on {website}: {e}")
                    self.stats['errors'] += 1
        
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
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = ScraperOrchestrator(config_file=args.config)
    
    # Determine categories
    if args.sample:
        # Use sample categories for testing
        sample_categories = ['Laptop', 'Smartphone', 'Headphones', 'Smart Watch', 'Tablet']
        print(f"\n🔬 Running in SAMPLE MODE with categories: {', '.join(sample_categories)}")
        orchestrator.run(category_names=sample_categories)
    elif args.categories:
        orchestrator.run(category_names=args.categories)
    else:
        # Use categories from config
        orchestrator.run()


if __name__ == "__main__":
    main()

