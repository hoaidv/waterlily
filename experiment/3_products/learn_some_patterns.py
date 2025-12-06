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


def main():
    """Run quick test with 3-5 common categories"""
    print("="*80)
    print("QUICK TEST: Scraping 3-5 Common Categories")
    print("="*80)
    print()
    
    # Test with common, searchable categories
    test_categories = [
        'Laptop',
        'Smartphone', 
        'Headphones',
        'Smart Watch',
        'Tablet'
    ]
    
    print("📋 Test Categories:")
    for i, cat in enumerate(test_categories, 1):
        print(f"   {i}. {cat}")
    print()
    
    print("⚙️  Configuration:")
    print("   - Products per category: 7")
    print("   - Delay between requests: 2-4 seconds")
    print("   - Learning mode: ON")
    print()
    
    input("Press Enter to start scraping (or Ctrl+C to cancel)...")
    print()
    
    # Create orchestrator with test configuration
    config = {
        'target_categories': test_categories,
        'websites': ['amazon'],
        'products_per_category_per_website': 7,  # Less than 10 for quick test
        'rate_limiting': {
            'delay_range': [2.0, 4.0],
            'max_retries': 3,
            'timeout': 15
        },
        'output': {
            'directory': './output'
        }
    }
    
    orchestrator = ScraperOrchestrator()
    orchestrator.config = config
    orchestrator._initialize_scrapers()
    
    # Run scraper
    try:
        orchestrator.run(category_names=test_categories)
        
        print()
        print("="*80)
        print("✓ QUICK TEST COMPLETED")
        print("="*80)
        print()
        print("📁 Check the following files:")
        print("   - ./output/amazon_products.json (scraped products)")
        print("   - ./output/amazon_*_log.json (category logs)")
        print("   - ./output/orchestrator.log (execution log)")
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


if __name__ == "__main__":
    main()

