#!/usr/bin/env python3
"""
Scan ASIN progress from output folder
Shows statistics about categories with ASINs crawled
"""

import json
import os
import sys
from typing import Dict, List, Tuple
from collections import defaultdict

def scan_asin_progress(output_dir: str = "./output") -> Dict[str, any]:
    """
    Scan output directory for ASIN files and generate progress statistics
    
    Args:
        output_dir: Directory containing ASIN files
        
    Returns:
        Dictionary with progress statistics
    """
    stats = {
        'total_categories': 0,
        'categories_with_asins': 0,
        'categories_empty': 0,
        'categories_missing': 0,
        'total_asins': 0,
        'categories': [],
        'empty_files': [],
        'top_categories': []
    }
    
    if not os.path.exists(output_dir):
        print(f"❌ Output directory not found: {output_dir}")
        return stats
    
    # Find all amazon_asin_*.json files
    asin_files = []
    for filename in os.listdir(output_dir):
        if filename.startswith('amazon_asin_') and filename.endswith('.json'):
            asin_files.append(filename)
    
    stats['total_categories'] = len(asin_files)
    
    # Process each file
    category_stats = []
    for filename in sorted(asin_files):
        filepath = os.path.join(output_dir, filename)
        
        # Extract category name from filename
        # Format: amazon_asin_<category_name>.json
        category_name = filename.replace('amazon_asin_', '').replace('.json', '')
        category_name = category_name.replace('_', ' ').title()  # Make it readable
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                asins = json.load(f)
            
            if not isinstance(asins, list):
                # Handle old format (dict with 'asin' key)
                if isinstance(asins, dict) and 'asin' in asins:
                    asins = asins['asin']
                else:
                    asins = []
            
            asin_count = len(asins)
            
            category_info = {
                'filename': filename,
                'category_name': category_name,
                'asin_count': asin_count,
                'has_asins': asin_count > 0
            }
            category_stats.append(category_info)
            
            if asin_count > 0:
                stats['categories_with_asins'] += 1
                stats['total_asins'] += asin_count
            else:
                stats['categories_empty'] += 1
                stats['empty_files'].append(category_name)
        
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Error reading {filename}: {e}")
            stats['categories_empty'] += 1
            stats['empty_files'].append(category_name)
    
    stats['categories'] = category_stats
    
    # Sort by ASIN count (descending) for top categories
    stats['top_categories'] = sorted(
        [c for c in category_stats if c['has_asins']],
        key=lambda x: x['asin_count'],
        reverse=True
    )[:20]  # Top 20
    
    return stats


def print_progress_report(stats: Dict[str, any], show_details: bool = False):
    """
    Print a formatted progress report
    
    Args:
        stats: Statistics dictionary from scan_asin_progress
        show_details: If True, show detailed category list
    """
    print("=" * 80)
    print("ASIN CRAWLING PROGRESS REPORT")
    print("=" * 80)
    print()
    
    # Summary statistics
    print("📊 SUMMARY")
    print("-" * 80)
    print(f"Total categories found:     {stats['total_categories']}")
    print(f"Categories with ASINs:      {stats['categories_with_asins']} ({stats['categories_with_asins']/max(stats['total_categories'], 1)*100:.1f}%)")
    print(f"Categories empty/missing:   {stats['categories_empty']} ({stats['categories_empty']/max(stats['total_categories'], 1)*100:.1f}%)")
    print(f"Total ASINs collected:     {stats['total_asins']:,}")
    
    if stats['categories_with_asins'] > 0:
        avg_asins = stats['total_asins'] / stats['categories_with_asins']
        print(f"Average ASINs per category: {avg_asins:.1f}")
    
    print()
    
    # Top categories
    if stats['top_categories']:
        print("🏆 TOP 20 CATEGORIES BY ASIN COUNT")
        print("-" * 80)
        for idx, cat in enumerate(stats['top_categories'], 1):
            print(f"{idx:2d}. {cat['category_name']:40s} {cat['asin_count']:6,} ASINs")
        print()
    
    # Empty categories
    if stats['empty_files']:
        print(f"⚠️  EMPTY CATEGORIES ({len(stats['empty_files'])})")
        print("-" * 80)
        if len(stats['empty_files']) <= 20:
            for cat_name in stats['empty_files']:
                print(f"  - {cat_name}")
        else:
            for cat_name in stats['empty_files'][:20]:
                print(f"  - {cat_name}")
            print(f"  ... and {len(stats['empty_files']) - 20} more")
        print()
    
    # Detailed breakdown
    if show_details:
        print("📋 DETAILED BREAKDOWN")
        print("-" * 80)
        for cat in stats['categories']:
            status = "✓" if cat['has_asins'] else "✗"
            print(f"{status} {cat['category_name']:40s} {cat['asin_count']:6,} ASINs")
        print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Scan ASIN crawling progress from output folder'
    )
    parser.add_argument(
        '--output-dir',
        default='./output',
        help='Directory containing ASIN files (default: ./output)'
    )
    parser.add_argument(
        '--details',
        action='store_true',
        help='Show detailed breakdown of all categories'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    # Resolve path relative to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, args.output_dir)
    
    # Scan progress
    stats = scan_asin_progress(output_dir)
    
    # Output results
    if args.json:
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    else:
        print_progress_report(stats, show_details=args.details)


if __name__ == "__main__":
    main()

