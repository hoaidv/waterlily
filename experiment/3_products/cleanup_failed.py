#!/usr/bin/env python3
"""
Cleanup failed scraping attempts
- Remove log files with no products, no patterns, or all products with no attributes
- Remove those categories from checkpoint to allow re-scraping
"""

import os
import json
import glob
from typing import List, Dict, Any


def should_remove_log(log_data: Dict[str, Any]) -> bool:
    """
    Check if a log file should be removed
    
    Returns True if:
    - No products found
    - No patterns learned
    - All products have no attributes
    """
    # Check 1: No products found
    products_found = log_data.get('products_found', 0)
    if products_found == 0:
        return True
    
    # Check 2: No patterns learned
    patterns_learned = log_data.get('patterns_learned', False)
    if not patterns_learned:
        return True
    
    # Check 3: All products have no attributes
    products = log_data.get('products', [])
    if products:
        products_with_attrs = sum(1 for p in products if p.get('attributes'))
        if products_with_attrs == 0:
            return True
    
    return False


def cleanup_failed_logs(output_dir: str = './output', checkpoint_file: str = './output/pattern_learning_checkpoint.json', dry_run: bool = False, auto_confirm: bool = False):
    """
    Clean up failed log files and update checkpoint
    """
    print("="*80)
    print("CLEANUP FAILED SCRAPING ATTEMPTS")
    print("="*80)
    print()
    
    # Find all Amazon log files
    log_files = glob.glob(os.path.join(output_dir, 'amazon_*_log.json'))
    print(f"Found {len(log_files)} log files")
    print()
    
    # Analyze logs
    to_remove = []
    stats = {
        'no_products': 0,
        'no_patterns': 0,
        'no_attributes': 0,
        'kept': 0
    }
    
    for log_file in log_files:
        try:
            with open(log_file, 'r') as f:
                data = json.load(f)
            
            category_name = data.get('category', 'Unknown')
            category_id = data.get('category_id')
            
            if should_remove_log(data):
                # Determine reason
                if data.get('products_found', 0) == 0:
                    reason = 'no_products'
                    stats['no_products'] += 1
                elif not data.get('patterns_learned', False):
                    reason = 'no_patterns'
                    stats['no_patterns'] += 1
                else:
                    reason = 'no_attributes'
                    stats['no_attributes'] += 1
                
                to_remove.append({
                    'file': log_file,
                    'category': category_name,
                    'category_id': category_id,
                    'reason': reason
                })
            else:
                stats['kept'] += 1
        
        except Exception as e:
            print(f"⚠️  Error reading {log_file}: {e}")
            continue
    
    print(f"Analysis:")
    print(f"  - No products found: {stats['no_products']}")
    print(f"  - No patterns learned: {stats['no_patterns']}")
    print(f"  - No attributes: {stats['no_attributes']}")
    print(f"  - Total to remove: {len(to_remove)}")
    print(f"  - Will keep: {stats['kept']}")
    print()
    
    if not to_remove:
        print("✓ No files to remove")
        return
    
    # Show sample
    print("Sample categories to remove (first 20):")
    for item in to_remove[:20]:
        print(f"  - {item['category']:30s} | Reason: {item['reason']}")
    if len(to_remove) > 20:
        print(f"  ... and {len(to_remove) - 20} more")
    print()
    
    # Check if dry run
    if dry_run:
        print("DRY RUN - No files will be removed")
        return
    
    # Confirm
    if not auto_confirm:
        response = input(f"Remove {len(to_remove)} log files and update checkpoint? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled")
            return
    else:
        print(f"Auto-confirming removal of {len(to_remove)} log files...")
    
    # Remove log files
    removed_count = 0
    removed_ids = set()
    
    for item in to_remove:
        try:
            os.remove(item['file'])
            removed_count += 1
            removed_ids.add(item['category_id'])
            print(f"✓ Removed: {item['category']}")
        except Exception as e:
            print(f"✗ Failed to remove {item['category']}: {e}")
    
    print()
    print(f"Removed {removed_count} log files")
    print()
    
    # Update checkpoint
    if os.path.exists(checkpoint_file):
        print("Updating checkpoint file...")
        
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        
        original_count = len(checkpoint.get('processed_categories', []))
        
        # Remove categories that were cleaned up
        checkpoint['processed_categories'] = [
            cat for cat in checkpoint.get('processed_categories', [])
            if cat['id'] not in removed_ids
        ]
        
        # Update last_category_id if needed
        if checkpoint['processed_categories']:
            checkpoint['last_category_id'] = checkpoint['processed_categories'][-1]['id']
        else:
            checkpoint['last_category_id'] = None
        
        # Save updated checkpoint
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        new_count = len(checkpoint['processed_categories'])
        print(f"✓ Updated checkpoint: {original_count} → {new_count} categories")
        print(f"  Removed {original_count - new_count} categories from checkpoint")
    else:
        print("⚠️  Checkpoint file not found")
    
    print()
    print("="*80)
    print("CLEANUP COMPLETE")
    print("="*80)
    print()
    print(f"Summary:")
    print(f"  - Log files removed: {removed_count}")
    print(f"  - Checkpoint updated: {original_count - new_count} categories removed")
    print(f"  - These categories can now be re-scraped")
    print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cleanup failed scraping attempts')
    parser.add_argument(
        '--output-dir',
        default='./output',
        help='Output directory containing log files'
    )
    parser.add_argument(
        '--checkpoint',
        default='./output/pattern_learning_checkpoint.json',
        help='Path to checkpoint file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be removed without actually removing'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='Auto-confirm removal without prompting'
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN MODE - No files will be removed")
        print()
    
    cleanup_failed_logs(args.output_dir, args.checkpoint, dry_run=args.dry_run, auto_confirm=args.yes)


if __name__ == "__main__":
    main()

