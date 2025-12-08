#!/usr/bin/env python3
"""
Cleanup script to remove failed categories from pattern learning results.

This script identifies and removes categories that failed to scrape successfully:
- Categories with no products found
- Categories where all products have empty attributes

It will:
1. Analyze all log files in ./output/
2. Identify failed categories
3. Remove them from the checkpoint file
4. Delete their log files
"""

import json
import os
import glob
import argparse
from typing import List, Dict, Set


def analyze_log_files(output_dir: str = './output') -> List[Dict[str, str]]:
    """
    Analyze all category log files and identify failed ones.
    
    Args:
        output_dir: Directory containing log files
        
    Returns:
        List of failed category dicts with 'name' and 'log_file' keys
    """
    failed_categories = []
    log_files = glob.glob(os.path.join(output_dir, 'amazon_*_log.json'))
    
    print(f'\n{"="*80}')
    print(f'ANALYZING {len(log_files)} CATEGORY LOG FILES')
    print(f'{"="*80}\n')
    
    for log_file in log_files:
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
            
            category_name = log_data.get('category', 'Unknown')
            products = log_data.get('products', [])
            
            # Check if failed: no products
            if len(products) == 0:
                print(f'❌ {category_name}: No products found')
                failed_categories.append({
                    'name': category_name,
                    'log_file': log_file,
                    'reason': 'no_products'
                })
            else:
                # Check if failed: all products have empty attributes
                products_with_attrs = [p for p in products if p.get('attributes')]
                
                if len(products_with_attrs) == 0:
                    print(f'❌ {category_name}: {len(products)} products, 0 with attributes')
                    failed_categories.append({
                        'name': category_name,
                        'log_file': log_file,
                        'reason': 'no_attributes'
                    })
        
        except json.JSONDecodeError:
            print(f'⚠️  {log_file}: Invalid JSON format')
        except Exception as e:
            print(f'⚠️  {log_file}: Error reading file - {e}')
    
    return failed_categories


def clean_checkpoint(failed_names: Set[str], checkpoint_file: str = './output/pattern_learning_checkpoint.json') -> Dict[str, int]:
    """
    Remove failed categories from the checkpoint file.
    
    Args:
        failed_names: Set of category names to remove
        checkpoint_file: Path to checkpoint file
        
    Returns:
        Dict with stats: original_count, removed_count, final_count
    """
    if not os.path.exists(checkpoint_file):
        print(f'\n⚠️  Checkpoint file not found: {checkpoint_file}')
        return {'original_count': 0, 'removed_count': 0, 'final_count': 0}
    
    with open(checkpoint_file, 'r') as f:
        checkpoint = json.load(f)
    
    processed = checkpoint.get('processed_categories', [])
    original_count = len(processed)
    
    # Remove failed categories
    cleaned = [cat for cat in processed if cat['name'] not in failed_names]
    
    # Remove duplicates (by ID)
    seen_ids = set()
    unique_cleaned = []
    for cat in cleaned:
        if cat['id'] not in seen_ids:
            seen_ids.add(cat['id'])
            unique_cleaned.append(cat)
    
    # Update checkpoint
    checkpoint['processed_categories'] = unique_cleaned
    if unique_cleaned:
        checkpoint['last_category_id'] = unique_cleaned[-1]['id']
    else:
        checkpoint['last_category_id'] = None
    
    # Save updated checkpoint
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint, f, indent=2)
    
    return {
        'original_count': original_count,
        'removed_count': original_count - len(unique_cleaned),
        'final_count': len(unique_cleaned)
    }


def delete_log_files(failed_categories: List[Dict[str, str]]) -> int:
    """
    Delete log files for failed categories.
    
    Args:
        failed_categories: List of failed category dicts
        
    Returns:
        Number of files deleted
    """
    deleted = 0
    for cat in failed_categories:
        try:
            os.remove(cat['log_file'])
            deleted += 1
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"⚠️  Could not delete {cat['log_file']}: {e}")
    
    return deleted


def main():
    """Main cleanup function"""
    parser = argparse.ArgumentParser(
        description='Clean up failed categories from pattern learning results'
    )
    parser.add_argument(
        '--output-dir',
        default='./output',
        help='Directory containing log files (default: ./output)'
    )
    parser.add_argument(
        '--checkpoint',
        default='./output/pattern_learning_checkpoint.json',
        help='Path to checkpoint file (default: ./output/pattern_learning_checkpoint.json)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be deleted without actually deleting'
    )
    parser.add_argument(
        '--auto-confirm',
        action='store_true',
        help='Skip confirmation prompt'
    )
    
    args = parser.parse_args()
    
    # Analyze log files
    failed_categories = analyze_log_files(args.output_dir)
    
    if not failed_categories:
        print(f'\n✅ No failed categories found. All categories have products with attributes!')
        return
    
    # Summary
    print(f'\n{"="*80}')
    print(f'SUMMARY')
    print(f'{"="*80}')
    print(f'Total failed categories: {len(failed_categories)}')
    
    # Breakdown by reason
    no_products = sum(1 for cat in failed_categories if cat['reason'] == 'no_products')
    no_attrs = sum(1 for cat in failed_categories if cat['reason'] == 'no_attributes')
    print(f'  - No products found: {no_products}')
    print(f'  - All products without attributes: {no_attrs}')
    
    # Show categories to be removed
    print(f'\nCategories to be removed:')
    for i, cat in enumerate(failed_categories[:10], 1):
        print(f'  {i}. {cat["name"]} ({cat["reason"]})')
    if len(failed_categories) > 10:
        print(f'  ... and {len(failed_categories) - 10} more')
    
    # Confirmation
    if args.dry_run:
        print(f'\n🔍 DRY RUN MODE - No changes will be made')
        return
    
    if not args.auto_confirm:
        print()
        response = input('Proceed with cleanup? (yes/no): ')
        if response.lower() not in ['yes', 'y']:
            print('Cleanup cancelled.')
            return
    
    # Clean checkpoint
    print(f'\n{"="*80}')
    print(f'CLEANING CHECKPOINT')
    print(f'{"="*80}')
    
    failed_names = {cat['name'] for cat in failed_categories}
    stats = clean_checkpoint(failed_names, args.checkpoint)
    
    print(f'✅ Checkpoint updated:')
    print(f'   Original: {stats["original_count"]} categories')
    print(f'   Removed: {stats["removed_count"]} categories')
    print(f'   Final: {stats["final_count"]} unique categories')
    
    # Delete log files
    print(f'\n{"="*80}')
    print(f'DELETING LOG FILES')
    print(f'{"="*80}')
    
    deleted = delete_log_files(failed_categories)
    print(f'🗑️  Deleted {deleted}/{len(failed_categories)} log files')
    
    print(f'\n{"="*80}')
    print(f'✅ CLEANUP COMPLETE!')
    print(f'{"="*80}\n')


if __name__ == "__main__":
    main()

