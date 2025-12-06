#!/usr/bin/env python3
"""
Quick test script to scrape a few products from 3-5 categories
This is a fast test to verify the scraper works end-to-end
"""

import sys
import os
import logging

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scrapers.orchestrator import ScraperOrchestrator
from scrapers.selenium_scraper import SeleniumAmazonScraper
from utils.db_connector import DatabaseConnection, load_categories


def main():
    """Run quick test with specific clothing categories"""
    print("="*80)
    print("QUICK TEST: Clothing Categories")
    print("="*80)
    print()
    
    # Test with clothing categories
    test_categories = [
        "Women's Sneakers",
        "Men's Khakis",
        "iPhones",
        "Digital Cameras"
    ]
    
    print("📋 Test Categories:")
    for i, cat in enumerate(test_categories, 1):
        print(f"   {i}. {cat}")
    print()
    
    print("⚙️  Configuration:")
    print("   - Products per category: 3-5")
    print("   - Delay between requests: 8-15 seconds (slow to avoid rate limiting)")
    print("   - Learning mode: ON")
    print("   - Testing: div.product-facts-detail pattern detection")
    print()
    
    print("Expected attributes (clothing):")
    print("   - Fabric type / Material composition")
    print("   - Origin / Country of Origin")
    print("   - Sole material (footwear)")
    print("   - Outer material (footwear)")
    print("   - Care instructions")
    print()
    
    input("Press Enter to start scraping (or Ctrl+C to cancel)...")
    print()
    
    # Create Selenium scraper configuration
    config = {
        'rate_limiting': {
            'delay_range': [8.0, 15.0],  # Slow to avoid rate limiting
            'max_retries': 3,
            'timeout': 15
        }
    }
    
    # Load categories from database
    print("Loading categories from database...")
    with DatabaseConnection() as cursor:
        categories_dict = load_categories(cursor)
    
    # Find test categories
    categories = []
    for cat_name in test_categories:
        found = False
        for cat_id, cat_data in categories_dict.items():
            if cat_data['name'] == cat_name:
                categories.append(cat_data)
                found = True
                print(f"✓ Found: {cat_name} (ID: {cat_data['id']})")
                break
        if not found:
            print(f"✗ Not found: {cat_name}")
    
    if not categories:
        print("\n✗ No categories found in database")
        sys.exit(1)
    
    print()
    
    # Initialize Selenium scraper
    print("Initializing Selenium scraper...")
    scraper = SeleniumAmazonScraper(config, output_dir='./output')
    print("✓ Selenium driver ready")
    print()
    
    # Run scraper for each category
    all_results = []
    try:
        for idx, category in enumerate(categories, 1):
            print("\n" + "="*80)
            print(f"CATEGORY {idx}/{len(categories)}: {category['name']}")
            print("="*80)
            
            result = scraper.process_category(category, max_products=5)
            all_results.append(result)
            
            # Brief status
            print(f"\n✓ Category completed:")
            print(f"  Products found: {result.get('products_found', 0)}")
            print(f"  Products scraped: {result.get('products_scraped', 0)}")
            print(f"  With attributes: {result.get('products_with_attributes', 0)}")
            print(f"  Patterns learned: {result.get('patterns_learned', False)}")
        
        print()
        print("="*80)
        print("✓ ALL CATEGORIES COMPLETED")
        print("="*80)
        print()
        
        # Summary
        total_found = sum(r.get('products_found', 0) for r in all_results)
        total_scraped = sum(r.get('products_scraped', 0) for r in all_results)
        total_with_attrs = sum(r.get('products_with_attributes', 0) for r in all_results)
        patterns_learned = sum(1 for r in all_results if r.get('patterns_learned', False))
        
        print("Summary:")
        print(f"  Categories processed: {len(all_results)}")
        print(f"  Total products found: {total_found}")
        print(f"  Total products scraped: {total_scraped}")
        print(f"  Products with attributes: {total_with_attrs}")
        print(f"  Categories with patterns: {patterns_learned}/{len(all_results)}")
        print()
        
        # Check for expected attributes in all products
        if total_with_attrs > 0:
            print("Checking extracted attributes...")
            import json
            with open('./output/amazon_products.json', 'r') as f:
                products = json.load(f)
            
            # Check products for each category
            for cat_name in test_categories:
                category_products = [p for p in products if p.get('category') == cat_name]
                
                if category_products:
                    print(f"\n{cat_name} ({len(category_products)} products):")
                    
                    # Show sample attributes from first 2 products
                    for p in category_products[:2]:
                        attrs = p.get('attributes', {})
                        if attrs:
                            title = (p.get('title') or 'N/A')[:50]
                            print(f"  ✓ {title}...")
                            for k, v in list(attrs.items())[:8]:
                                v_str = str(v)[:60]
                                print(f"    - {k}: {v_str}")
                        else:
                            print(f"  ✗ No attributes: {p.get('title', 'N/A')[:50]}...")
        
        print()
        print("📁 Check the following files:")
        print("   - ./output/amazon_products.json (scraped products)")
        print("   - ./output/amazon_womens_sneakers_log.json (category log)")
        print("   - ./config/amazon_config.json (learned patterns)")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup Selenium driver
        if 'scraper' in locals():
            scraper.close()
            print("✓ Selenium driver closed")


if __name__ == "__main__":
    main()

