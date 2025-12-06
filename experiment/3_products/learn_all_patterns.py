#!/usr/bin/env python3
"""
Learn extraction patterns for ALL categories in the database
This script will:
- Load all 1000+ categories from MySQL
- Learn patterns by scraping sample products (5-7 per category)
- Save patterns to config for future use
- Support checkpointing and resuming
"""

import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.db_connector import DatabaseConnection, load_categories
from scrapers.selenium_scraper import SeleniumAmazonScraper


class PatternLearner:
    """Learn patterns for all categories"""
    
    def __init__(self, output_dir='./output', checkpoint_file='./output/pattern_learning_checkpoint.json'):
        self.output_dir = output_dir
        self.checkpoint_file = checkpoint_file
        self.checkpoint = self._load_checkpoint()
        
        # Setup logging
        self._setup_logging()
        
        # Initialize Selenium scraper with no delays for real-time viewing
        config = {
            'rate_limiting': {
                'delay_range': [1.0, 2.0],  # Minimal delays for real-time scraping
                'max_retries': 3,
                'timeout': 15
            }
        }
        self.scraper = SeleniumAmazonScraper(config, output_dir=output_dir)
        self.logger.info("✓ Selenium scraper initialized (browser visible - real-time scraping)")
        
        # Statistics
        self.stats = {
            'start_time': None,
            'end_time': None,
            'total_categories': 0,
            'categories_processed': 0,
            'categories_with_patterns': 0,
            'categories_failed': 0,
            'total_products_scraped': 0,
            'failed_categories': []
        }
    
    def _setup_logging(self):
        """Setup logging"""
        os.makedirs(self.output_dir, exist_ok=True)
        log_file = os.path.join(self.output_dir, 'pattern_learning.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _load_checkpoint(self) -> Dict[str, Any]:
        """Load checkpoint if exists"""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {'processed_categories': [], 'last_category_id': None}
    
    def _save_checkpoint(self, category_id: int, category_name: str):
        """Save checkpoint"""
        self.checkpoint['processed_categories'].append({
            'id': category_id,
            'name': category_name,
            'timestamp': datetime.now().isoformat()
        })
        self.checkpoint['last_category_id'] = category_id
        
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.checkpoint, f, indent=2)
    
    def _is_processed(self, category_id: int) -> bool:
        """Check if category already processed"""
        processed_ids = [c['id'] for c in self.checkpoint.get('processed_categories', [])]
        return category_id in processed_ids
    
    def load_all_categories(self) -> List[Dict[str, Any]]:
        """Load all categories from database"""
        self.logger.info("Loading all categories from database...")
        
        with DatabaseConnection() as cursor:
            categories_dict = load_categories(cursor)
            categories = list(categories_dict.values())
        
        self.logger.info(f"Loaded {len(categories)} categories")
        return categories
    
    def learn_patterns_for_category(self, category: Dict[str, Any], max_products: int = 5) -> bool:
        """
        Learn patterns for a single category
        
        Args:
            category: Category data
            max_products: Number of products to sample (fewer = faster)
            
        Returns:
            True if patterns learned successfully
        """
        category_name = category['name']
        category_id = category['id']
        
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"Learning patterns for: {category_name} (ID: {category_id})")
        self.logger.info(f"{'='*80}")
        
        try:
            # Process category (will learn patterns automatically)
            result = self.scraper.process_category(category, max_products=max_products)
            
            # Check if patterns were learned
            patterns_learned = result.get('patterns_learned', False)
            products_scraped = result.get('products_scraped', 0)
            
            if patterns_learned:
                self.stats['categories_with_patterns'] += 1
                self.logger.info(f"✓ Patterns learned for {category_name}")
            else:
                self.logger.warning(f"⚠ No patterns learned for {category_name}")
            
            self.stats['total_products_scraped'] += products_scraped
            self.stats['categories_processed'] += 1
            
            return patterns_learned
            
        except Exception as e:
            self.logger.error(f"✗ Error processing {category_name}: {e}")
            self.stats['categories_failed'] += 1
            self.stats['failed_categories'].append({
                'name': category_name,
                'id': category_id,
                'error': str(e)
            })
            return False
    
    def run(self, start_from: int = 0, max_categories: int = None, products_per_category: int = 5, category_names: list = None):
        """
        Run pattern learning for all categories or specific categories
        
        Args:
            start_from: Start from this category index (for resuming)
            max_categories: Maximum number of categories to process (None = all)
            products_per_category: Number of products to sample per category
            category_names: List of specific category names to process (None = all)
        """
        self.stats['start_time'] = datetime.now()
        
        self.logger.info("="*80)
        if category_names:
            self.logger.info(f"PATTERN LEARNING FOR SPECIFIC CATEGORIES ({len(category_names)})")
        else:
            self.logger.info("PATTERN LEARNING FOR ALL CATEGORIES")
        self.logger.info("="*80)
        self.logger.info(f"Start time: {self.stats['start_time']}")
        self.logger.info(f"Products per category: {products_per_category}")
        if category_names:
            self.logger.info(f"Target categories: {', '.join(category_names)}")
        else:
            self.logger.info(f"Start from index: {start_from}")
            self.logger.info(f"Max categories: {max_categories or 'ALL'}")
        self.logger.info("")
        
        # Load categories
        all_categories = self.load_all_categories()
        self.stats['total_categories'] = len(all_categories)
        
        # Filter by specific category names if provided
        if category_names:
            categories_to_process = [
                cat for cat in all_categories
                if cat['name'] in category_names
            ]
            
            # Check which categories were not found
            found_names = {cat['name'] for cat in categories_to_process}
            not_found = set(category_names) - found_names
            if not_found:
                self.logger.warning(f"Categories not found in database: {', '.join(not_found)}")
            
            self.logger.info(f"Found {len(categories_to_process)}/{len(category_names)} requested categories")
        else:
            # Filter already processed (for 'all' mode)
            categories_to_process = [
                cat for cat in all_categories 
                if not self._is_processed(cat['id'])
            ]
        
        if not category_names:
            self.logger.info(f"Already processed: {len(all_categories) - len(categories_to_process)}")
            self.logger.info(f"Remaining: {len(categories_to_process)}")
            self.logger.info("")
            
            # Apply start_from and max_categories (only for 'all' mode)
            if start_from > 0:
                categories_to_process = categories_to_process[start_from:]
            
            if max_categories:
                categories_to_process = categories_to_process[:max_categories]
        
        self.logger.info(f"Will process: {len(categories_to_process)} categories")
        self.logger.info("")
        
        # Check if there are categories to process
        if not categories_to_process:
            self.logger.warning("No categories to process!")
            return
        
        # Process each category
        for idx, category in enumerate(categories_to_process, 1):
            self.logger.info(f"\n[{idx}/{len(categories_to_process)}] Processing: {category['name']}")
            
            success = self.learn_patterns_for_category(category, max_products=products_per_category)
            
            # Save checkpoint
            self._save_checkpoint(category['id'], category['name'])
            
            # Progress report every 10 categories
            if idx % 10 == 0:
                self._print_progress_report()
        
        # Final statistics
        self.stats['end_time'] = datetime.now()
        self._save_final_report()
        self._print_final_report()
    
    def _print_progress_report(self):
        """Print progress report"""
        elapsed = datetime.now() - self.stats['start_time']
        
        self.logger.info("")
        self.logger.info("="*80)
        self.logger.info("PROGRESS REPORT")
        self.logger.info("="*80)
        self.logger.info(f"Elapsed time: {elapsed}")
        self.logger.info(f"Categories processed: {self.stats['categories_processed']}")
        self.logger.info(f"Categories with patterns: {self.stats['categories_with_patterns']}")
        self.logger.info(f"Categories failed: {self.stats['categories_failed']}")
        self.logger.info(f"Total products scraped: {self.stats['total_products_scraped']}")
        
        if self.stats['categories_processed'] > 0:
            success_rate = (self.stats['categories_with_patterns'] / self.stats['categories_processed']) * 100
            self.logger.info(f"Success rate: {success_rate:.1f}%")
        
        self.logger.info("="*80)
        self.logger.info("")
    
    def _save_final_report(self):
        """Save final report to file"""
        report_file = os.path.join(self.output_dir, 'pattern_learning_report.json')
        
        with open(report_file, 'w') as f:
            json.dump({
                'start_time': str(self.stats['start_time']),
                'end_time': str(self.stats['end_time']),
                'duration': str(self.stats['end_time'] - self.stats['start_time']),
                'total_categories': self.stats['total_categories'],
                'categories_processed': self.stats['categories_processed'],
                'categories_with_patterns': self.stats['categories_with_patterns'],
                'categories_failed': self.stats['categories_failed'],
                'total_products_scraped': self.stats['total_products_scraped'],
                'success_rate': (self.stats['categories_with_patterns'] / self.stats['categories_processed'] * 100) if self.stats['categories_processed'] > 0 else 0,
                'failed_categories': self.stats['failed_categories']
            }, f, indent=2)
        
        self.logger.info(f"✓ Saved final report to {report_file}")
    
    def _print_final_report(self):
        """Print final report"""
        duration = self.stats['end_time'] - self.stats['start_time']
        
        self.logger.info("")
        self.logger.info("="*80)
        self.logger.info("PATTERN LEARNING COMPLETED")
        self.logger.info("="*80)
        self.logger.info(f"Start time: {self.stats['start_time']}")
        self.logger.info(f"End time: {self.stats['end_time']}")
        self.logger.info(f"Total duration: {duration}")
        self.logger.info(f"")
        self.logger.info(f"Total categories in DB: {self.stats['total_categories']}")
        self.logger.info(f"Categories processed: {self.stats['categories_processed']}")
        self.logger.info(f"Categories with patterns: {self.stats['categories_with_patterns']}")
        self.logger.info(f"Categories failed: {self.stats['categories_failed']}")
        self.logger.info(f"Total products scraped: {self.stats['total_products_scraped']}")
        
        if self.stats['categories_processed'] > 0:
            success_rate = (self.stats['categories_with_patterns'] / self.stats['categories_processed']) * 100
            self.logger.info(f"Success rate: {success_rate:.1f}%")
            
            avg_time = duration / self.stats['categories_processed']
            self.logger.info(f"Average time per category: {avg_time}")
        
        if self.stats['failed_categories']:
            self.logger.info(f"\nFailed categories ({len(self.stats['failed_categories'])}):")
            for failed in self.stats['failed_categories'][:10]:
                self.logger.info(f"  - {failed['name']}: {failed['error']}")
            if len(self.stats['failed_categories']) > 10:
                self.logger.info(f"  ... and {len(self.stats['failed_categories']) - 10} more")
        
        self.logger.info("="*80)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Learn patterns for all categories')
    parser.add_argument(
        '--start-from',
        type=int,
        default=0,
        help='Start from this category index (for resuming)'
    )
    parser.add_argument(
        '--max-categories',
        type=int,
        default=None,
        help='Maximum number of categories to process'
    )
    parser.add_argument(
        '--products-per-category',
        type=int,
        default=5,
        help='Number of products to sample per category (default: 5)'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Run a small batch for testing (first 20 categories)'
    )
    parser.add_argument(
        '--categories',
        nargs='+',
        help='Specific category names to process (e.g., "Women\'s Sneakers" "Men\'s Khakis")'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Process all categories (default behavior if no categories specified)'
    )
    
    args = parser.parse_args()
    
    # Batch mode for testing
    if args.batch:
        args.max_categories = 20
        print("\n🧪 BATCH MODE: Processing first 20 categories")
    
    print("="*80)
    if args.categories:
        print(f"PATTERN LEARNING FOR SPECIFIC CATEGORIES ({len(args.categories)})")
    else:
        print("PATTERN LEARNING FOR ALL CATEGORIES")
    print("="*80)
    print()
    print(f"Configuration:")
    print(f"  - Products per category: {args.products_per_category}")
    if args.categories:
        print(f"  - Target categories: {', '.join(args.categories)}")
    else:
        print(f"  - Start from: {args.start_from}")
        print(f"  - Max categories: {args.max_categories or 'ALL (1000+)'}")
        print(f"  - Batch mode: {args.batch}")
    print()
    
    if not args.batch and not args.categories:
        print("⚠️  WARNING: This will take several hours to complete!")
        print("   Estimated time: 3-6 hours for all 1000+ categories")
        print()
        response = input("Continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            sys.exit(0)
    
    print()
    
    # Run pattern learning
    learner = PatternLearner()
    
    try:
        learner.run(
            start_from=args.start_from,
            max_categories=args.max_categories,
            products_per_category=args.products_per_category,
            category_names=args.categories
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup Selenium driver
        if hasattr(learner, 'scraper') and learner.scraper:
            learner.scraper.close()
            print("\n✓ Selenium driver closed")


if __name__ == "__main__":
    main()

