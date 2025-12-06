#!/usr/bin/env python3
"""
Test script to verify scraper setup
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    
    try:
        import requests
        print("  ✓ requests")
    except ImportError as e:
        print(f"  ✗ requests: {e}")
        return False
    
    try:
        import lxml
        print("  ✓ lxml")
    except ImportError as e:
        print(f"  ✗ lxml: {e}")
        return False
    
    try:
        import mysql.connector
        print("  ✓ mysql-connector-python")
    except ImportError as e:
        print(f"  ✗ mysql-connector-python: {e}")
        return False
    
    try:
        from utils.db_connector import DatabaseConnection, get_target_categories
        print("  ✓ db_connector")
    except ImportError as e:
        print(f"  ✗ db_connector: {e}")
        return False
    
    try:
        from scrapers.base_scraper import BaseScraper
        print("  ✓ base_scraper")
    except ImportError as e:
        print(f"  ✗ base_scraper: {e}")
        return False
    
    try:
        from scrapers.pattern_learner import PatternLearner
        print("  ✓ pattern_learner")
    except ImportError as e:
        print(f"  ✗ pattern_learner: {e}")
        return False
    
    try:
        from scrapers.amazon_scraper import AmazonScraper
        print("  ✓ amazon_scraper")
    except ImportError as e:
        print(f"  ✗ amazon_scraper: {e}")
        return False
    
    try:
        from scrapers.orchestrator import ScraperOrchestrator
        print("  ✓ orchestrator")
    except ImportError as e:
        print(f"  ✗ orchestrator: {e}")
        return False
    
    return True


def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    
    try:
        from utils.db_connector import DatabaseConnection, load_categories
        
        with DatabaseConnection() as cursor:
            categories = load_categories(cursor)
            print(f"  ✓ Connected to database")
            print(f"  ✓ Found {len(categories)} categories")
            
            # Show sample categories
            sample_cats = list(categories.items())[:5]
            print(f"\n  Sample categories:")
            for cat_id, cat_data in sample_cats:
                print(f"    - {cat_data['name']} (ID: {cat_id})")
            
            return True
    
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        return False


def test_pattern_learner():
    """Test pattern learner with sample HTML"""
    print("\nTesting pattern learner...")
    
    try:
        from scrapers.pattern_learner import PatternLearner
        
        learner = PatternLearner()
        
        # Sample HTML with a product table
        sample_html = """
        <html>
            <body>
                <h1 id="productTitle">Test Product</h1>
                <table id="productDetails_techSpec_section_1">
                    <tr>
                        <th>Brand</th>
                        <td>Test Brand</td>
                    </tr>
                    <tr>
                        <th>Model</th>
                        <td>Test Model</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        
        analysis = learner.analyze_product_page(sample_html, "test_url")
        
        if analysis['success']:
            print(f"  ✓ Pattern analysis successful")
            print(f"  ✓ Found {len(analysis['tables_found'])} tables")
            print(f"  ✓ Generated {len(analysis['extraction_rules'])} rules")
            
            if analysis['tables_found']:
                table = analysis['tables_found'][0]
                print(f"\n  Sample table found:")
                print(f"    XPath: {table['xpath']}")
                print(f"    Key-value pairs: {len(table['key_value_pairs'])}")
            
            return True
        else:
            print(f"  ✗ Pattern analysis failed")
            return False
    
    except Exception as e:
        print(f"  ✗ Pattern learner test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scraper_initialization():
    """Test scraper initialization"""
    print("\nTesting scraper initialization...")
    
    try:
        from scrapers.amazon_scraper import AmazonScraper
        
        config = {
            'rate_limiting': {
                'delay_range': [1, 2],
                'max_retries': 3,
                'timeout': 15
            }
        }
        
        scraper = AmazonScraper(config, output_dir="./output")
        print(f"  ✓ Amazon scraper initialized")
        print(f"  ✓ Website name: {scraper.get_website_name()}")
        print(f"  ✓ Base URL: {scraper.base_url}")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Scraper initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("SCRAPER SETUP TEST")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Database Connection", test_database_connection()))
    results.append(("Pattern Learner", test_pattern_learner()))
    results.append(("Scraper Initialization", test_scraper_initialization()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(passed for _, passed in results)
    
    print("="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED - Ready to scrape!")
    else:
        print("✗ SOME TESTS FAILED - Please fix issues before scraping")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

