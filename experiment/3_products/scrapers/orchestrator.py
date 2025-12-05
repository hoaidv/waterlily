#!/usr/bin/env python3
"""
Main scraping orchestrator that coordinates category scraping across all websites
"""

import json
import os
import sys
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

# Import utilities
try:
    from utils.db_connector import DatabaseConnection, get_target_categories
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
    from db_connector import DatabaseConnection, get_target_categories

# Import scrapers
from amazon_scraper import AmazonScraper
from flipkart_scraper import FlipkartScraper
from newegg_scraper import NeweggScraper
from craigslist_scraper import CraigslistScraper
from attribute_extractor import AttributeExtractor


class ScrapingOrchestrator:
    """Orchestrates scraping across multiple websites and categories"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize orchestrator with configuration"""
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'scraping_config.json')
        
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Initialize scrapers
        delay_range = tuple(self.config['rate_limiting']['delay_range'])
        max_retries = self.config['rate_limiting']['max_retries']
        
        self.scrapers = {
            'amazon': AmazonScraper(delay_range, max_retries),
            'flipkart': FlipkartScraper(delay_range, max_retries),
            'newegg': NeweggScraper(delay_range, max_retries),
            'craigslist': CraigslistScraper(delay_range, max_retries, 
                                           self.config['craigslist']['location'])
        }
        
        # Initialize attribute extractor
        config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
        self.attribute_extractor = AttributeExtractor(config_dir)
        
        # Results storage
        self.scraped_products = []
        self.stats = {
            'categories_processed': 0,
            'products_scraped': 0,
            'products_with_attributes': 0,
            'websites_scraped': {},
            'errors': []
        }
        
        # Checkpoint
        self.checkpoint_file = os.path.join(os.path.dirname(__file__), 
                                           self.config['checkpoint']['file'])
        self.checkpoint_interval = self.config['checkpoint']['interval']
    
    def load_categories_from_db(self) -> List[Dict[str, Any]]:
        """Load target categories and their attributes from database"""
        with DatabaseConnection() as cursor:
            target_names = self.config['target_categories']
            categories = get_target_categories(cursor, target_names)
            return categories
    
    def scrape_product_with_attributes(self, scraper, product_url: str, 
                                      category: Dict[str, Any],
                                      website: str) -> Optional[Dict[str, Any]]:
        """Scrape product and extract attributes"""
        print(f"\n      🔍 Scraping product from {website}...")
        
        # Get product basic info
        product = scraper.scrape_product_page(product_url)
        
        if not product:
            print(f"      ✗ Failed to extract basic product info")
            return None
        
        print(f"      ✓ Basic info extracted: {product.get('name', 'N/A')[:60]}")
        
        # Parse HTML for attribute extraction
        print(f"      🔄 Re-fetching page for attribute extraction...")
        response = scraper._fetch_with_retry(product_url)
        if not response:
            print(f"      ⚠ Could not re-fetch page, returning basic info only")
            return product  # Return basic info even if we can't extract attributes
        
        soup = scraper._parse_html(response.content)
        
        # Extract attributes using configuration
        extracted_attributes = self.attribute_extractor.extract_attributes(
            soup, 
            product, 
            category['name'],
            website,
            category.get('attributes', [])
        )
        
        product['attributes'] = extracted_attributes
        product['category_id'] = category['id']
        product['category_name'] = category['name']
        product['product_def_id'] = category.get('product_def_id')
        
        # Calculate attribute coverage
        required_attrs = len(category.get('attributes', []))
        extracted_attrs = len(extracted_attributes)
        product['attribute_coverage'] = extracted_attrs / required_attrs if required_attrs > 0 else 0
        
        print(f"      📊 Attribute coverage: {extracted_attrs}/{required_attrs} ({product['attribute_coverage']:.1%})")
        
        return product
    
    def scrape_category(self, category: Dict[str, Any], websites: List[str], 
                       sample_mode: bool = False) -> List[Dict[str, Any]]:
        """Scrape a category from multiple websites"""
        category_name = category['name']
        category_id = category['id']
        attributes = category.get('attributes', [])
        
        print(f"\n{'=' * 60}")
        print(f"Scraping category: {category_name} (ID: {category_id})")
        print(f"Required attributes: {len(attributes)}")
        print(f"{'=' * 60}")
        
        category_products = []
        
        # Determine products per website
        if sample_mode:
            products_per_website = self.config['sample_mode']['products_per_website']
        else:
            products_per_website = self.config['products_per_category_per_website']
        
        for website in websites:
            if website not in self.scrapers:
                print(f"  ✗ Unknown website: {website}")
                continue
            
            scraper = self.scrapers[website]
            print(f"\n  Website: {website}")
            
            try:
                # Get product URLs from listing page
                product_urls = scraper.scrape_listing_page(category_name, products_per_website)
                
                if not product_urls:
                    print(f"    ✗ No products found")
                    self.stats['websites_scraped'][website] = self.stats['websites_scraped'].get(website, 0)
                    continue
                
                print(f"    Found {len(product_urls)} product URLs")
                
                # Scrape each product with attributes
                for i, product_url in enumerate(product_urls, 1):
                    print(f"\n    {'='*70}")
                    print(f"    [{i}/{len(product_urls)}] Product URL: {product_url[:100]}")
                    print(f"    {'='*70}")
                    
                    product_info = self.scrape_product_with_attributes(
                        scraper, product_url, category, website
                    )
                    
                    if product_info:
                        category_products.append(product_info)
                        
                        coverage = product_info.get('attribute_coverage', 0)
                        attr_count = len(product_info.get('attributes', {}))
                        
                        # Show extracted attributes
                        print(f"\n      📋 Extracted Attributes:")
                        for attr_name, attr_value in product_info.get('attributes', {}).items():
                            value_str = str(attr_value)[:50]
                            print(f"         • {attr_name}: {value_str}")
                        
                        print(f"\n      ✅ SUCCESS: {attr_count}/{len(attributes)} attributes ({coverage:.1%})")
                        
                        # Track stats
                        if product_info.get('attributes'):
                            self.stats['products_with_attributes'] += 1
                    else:
                        print(f"\n      ❌ FAILED: Could not scrape product")
                
                # Track website stats
                self.stats['websites_scraped'][website] = self.stats['websites_scraped'].get(website, 0) + len(category_products)
            
            except Exception as e:
                error_msg = f"Error scraping {website} for category {category_name}: {e}"
                print(f"    ✗ {error_msg}")
                self.stats['errors'].append(error_msg)
                import traceback
                traceback.print_exc()
                continue
        
        return category_products
    
    def save_checkpoint(self):
        """Save checkpoint to file"""
        checkpoint_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'stats': self.stats.copy(),
            'products': self.scraped_products,
            'config': self.config
        }
        
        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Checkpoint saved: {len(self.scraped_products)} products")
    
    def load_checkpoint(self) -> bool:
        """Load checkpoint from file"""
        if not os.path.exists(self.checkpoint_file):
            return False
        
        try:
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint_data = json.load(f)
            
            self.scraped_products = checkpoint_data.get('products', [])
            self.stats = checkpoint_data.get('stats', self.stats)
            
            print(f"✓ Loaded checkpoint: {len(self.scraped_products)} products")
            return True
        except Exception as e:
            print(f"✗ Error loading checkpoint: {e}")
            return False
    
    def save_results(self):
        """Save scraped products to output file"""
        output_config = self.config['output']
        output_dir = os.path.join(os.path.dirname(__file__), '..', output_config['directory'])
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, output_config['file'])
        
        results = {
            'metadata': {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_products': len(self.scraped_products),
                'categories': self.config['target_categories'],
                'websites': self.config['websites']
            },
            'stats': self.stats,
            'products': self.scraped_products
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved {len(self.scraped_products)} products to {output_file}")
    
    def run(self, sample_mode: bool = False, resume_from_checkpoint: bool = False):
        """Run the scraping orchestrator"""
        print("=" * 60)
        print("Product Scraping Orchestrator")
        print("=" * 60)
        
        # Load checkpoint if resuming
        if resume_from_checkpoint:
            self.load_checkpoint()
        
        # Load categories from database
        print("\nLoading categories from database...")
        categories = self.load_categories_from_db()
        print(f"✓ Loaded {len(categories)} categories")
        
        for category in categories:
            print(f"  - {category['name']}: {len(category.get('attributes', []))} attributes")
        
        # Get websites to scrape
        websites = self.config['websites']
        print(f"\nWebsites: {', '.join(websites)}")
        
        if sample_mode:
            print(f"\n⚠️  SAMPLE MODE: Scraping {self.config['sample_mode']['products_per_website']} products per website")
        
        # Scrape each category
        for category in categories:
            category_products = self.scrape_category(category, websites, sample_mode)
            self.scraped_products.extend(category_products)
            self.stats['categories_processed'] += 1
            self.stats['products_scraped'] += len(category_products)
            
            # Save checkpoint periodically
            if self.config['checkpoint']['enabled']:
                if len(self.scraped_products) >= self.checkpoint_interval:
                    self.save_checkpoint()
        
        # Final checkpoint
        if self.config['checkpoint']['enabled']:
            self.save_checkpoint()
        
        # Save results
        self.save_results()
        
        # Print final stats
        print("\n" + "=" * 60)
        print("Scraping Complete!")
        print("=" * 60)
        print(f"Categories processed: {self.stats['categories_processed']}")
        print(f"Products scraped: {self.stats['products_scraped']}")
        print(f"Products with attributes: {self.stats['products_with_attributes']}")
        
        print("\nProducts per website:")
        for website, count in self.stats['websites_scraped'].items():
            print(f"  {website}: {count}")
        
        print(f"\nErrors: {len(self.stats['errors'])}")
        if self.stats['errors']:
            print("\nFirst 5 errors:")
            for error in self.stats['errors'][:5]:
                print(f"  - {error}")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape products from multiple websites')
    parser.add_argument('--sample', action='store_true', help='Run in sample mode (fewer products)')
    parser.add_argument('--resume', action='store_true', help='Resume from checkpoint')
    parser.add_argument('--config', type=str, help='Path to config file')
    
    args = parser.parse_args()
    
    orchestrator = ScrapingOrchestrator(args.config)
    orchestrator.run(sample_mode=args.sample, resume_from_checkpoint=args.resume)


if __name__ == "__main__":
    main()

