#!/usr/bin/env python3
"""
Monitor pattern learning progress
"""

import json
import os
from datetime import datetime

def check_progress():
    """Check and display progress"""
    
    print("="*80)
    print("PATTERN LEARNING PROGRESS")
    print("="*80)
    print()
    
    # Check checkpoint
    checkpoint_file = './output/pattern_learning_checkpoint.json'
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        
        processed = checkpoint.get('processed_categories', [])
        print(f"✓ Categories processed: {len(processed)}")
        
        if processed:
            last = processed[-1]
            print(f"  Last processed: {last['name']} at {last['timestamp']}")
        print()
    else:
        print("No checkpoint file found yet...")
        print()
    
    # Check config
    config_file = './config/amazon_config.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"✓ Learned patterns for {len(config)} categories")
        
        # Count success rate
        with_patterns = sum(1 for cat_data in config.values() if cat_data.get('patterns_found'))
        print(f"  Categories with patterns: {with_patterns}/{len(config)}")
        print(f"  Success rate: {with_patterns/len(config)*100:.1f}%")
        print()
        
        # Show recent categories
        print("Recent categories:")
        for cat_name in list(config.keys())[-5:]:
            cat_data = config[cat_name]
            status = "✓" if cat_data.get('patterns_found') else "✗"
            rules_count = len(cat_data.get('rules', []))
            print(f"  {status} {cat_name}: {rules_count} patterns")
        print()
    
    # Check products
    products_file = './output/amazon_products.json'
    if os.path.exists(products_file):
        with open(products_file, 'r') as f:
            products = json.load(f)
        
        print(f"✓ Total products scraped: {len(products)}")
        
        # Count by category
        from collections import Counter
        category_counts = Counter(p['category'] for p in products)
        print(f"  Unique categories: {len(category_counts)}")
        print()
    
    # Estimate completion
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        
        processed = checkpoint.get('processed_categories', [])
        if len(processed) >= 2:
            # Calculate average time
            first_time = datetime.fromisoformat(processed[0]['timestamp'])
            last_time = datetime.fromisoformat(processed[-1]['timestamp'])
            elapsed = (last_time - first_time).total_seconds()
            avg_per_category = elapsed / len(processed)
            
            remaining = 1004 - len(processed)
            estimated_seconds = remaining * avg_per_category
            estimated_hours = estimated_seconds / 3600
            
            print(f"📊 Estimates:")
            print(f"  Average time per category: {avg_per_category:.1f} seconds")
            print(f"  Remaining categories: {remaining}")
            print(f"  Estimated time remaining: {estimated_hours:.1f} hours")
            print()
    
    print("="*80)
    print(f"Checked at: {datetime.now()}")
    print("="*80)


if __name__ == "__main__":
    check_progress()

