#!/usr/bin/env python3
"""
Script to merge duplicated patterns in amazon_config.json (ignoring sample_keys)
and output unique patterns to amazon_shared.json
"""

import json
from collections import defaultdict
from typing import Dict, List, Any


def create_pattern_key(pattern: Dict[str, Any]) -> tuple:
    """
    Create a unique key for a pattern based on all fields except sample_keys.
    This key will be used to identify duplicate patterns.
    """
    return (
        pattern.get("type"),
        pattern.get("priority"),
        pattern.get("xpath"),
        pattern.get("extraction_method")
    )


def merge_patterns(pattern1: Dict[str, Any], pattern2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two patterns by combining their frequencies, averaging confidences,
    and merging sample_keys.
    """
    merged = pattern1.copy()
    
    # Combine frequencies
    merged["frequency"] = pattern1.get("frequency", 0) + pattern2.get("frequency", 0)
    
    # Average confidences (weighted by frequency)
    freq1 = pattern1.get("frequency", 0)
    freq2 = pattern2.get("frequency", 0)
    conf1 = pattern1.get("confidence", 0.0)
    conf2 = pattern2.get("confidence", 0.0)
    
    if freq1 + freq2 > 0:
        merged["confidence"] = (conf1 * freq1 + conf2 * freq2) / (freq1 + freq2)
    else:
        merged["confidence"] = (conf1 + conf2) / 2 if (conf1 + conf2) > 0 else 0.0
    
    # Merge sample_keys (combine unique values)
    sample_keys1 = set(pattern1.get("sample_keys", []))
    sample_keys2 = set(pattern2.get("sample_keys", []))
    merged["sample_keys"] = sorted(list(sample_keys1 | sample_keys2))
    
    return merged


def process_amazon_config(input_file: str, output_file: str):
    """
    Load amazon_config.json, merge duplicate patterns, and save unique patterns.
    """
    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Dictionary to store unique patterns
    unique_patterns: Dict[tuple, Dict[str, Any]] = {}
    
    # Track total products analyzed across all categories
    total_products = 0
    categories_with_patterns = 0
    
    # Process each category
    for category_name, category_data in config.items():
        if not isinstance(category_data, dict):
            continue
            
        total_products += category_data.get("total_products_analyzed", 0)
        if category_data.get("patterns_found", False):
            categories_with_patterns += 1
        
        rules = category_data.get("rules", [])
        for pattern in rules:
            pattern_key = create_pattern_key(pattern)
            
            if pattern_key in unique_patterns:
                # Merge with existing pattern
                unique_patterns[pattern_key] = merge_patterns(
                    unique_patterns[pattern_key],
                    pattern
                )
            else:
                # Add new pattern (make a copy to avoid modifying original)
                unique_patterns[pattern_key] = pattern.copy()
    
    # Convert to list and sort by frequency (descending) and confidence (descending)
    unique_patterns_list = list(unique_patterns.values())
    unique_patterns_list.sort(
        key=lambda p: (p.get("frequency", 0), p.get("confidence", 0.0)),
        reverse=True
    )
    
    # Create output structure
    output = {
        "total_categories_processed": len(config),
        "categories_with_patterns": categories_with_patterns,
        "total_products_analyzed": total_products,
        "unique_patterns_count": len(unique_patterns_list),
        "patterns": unique_patterns_list
    }
    
    # Save to output file
    print(f"Saving {len(unique_patterns_list)} unique patterns to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Done! Merged patterns from {len(config)} categories into {len(unique_patterns_list)} unique patterns.")
    print(f"Total products analyzed: {total_products}")
    print(f"Categories with patterns: {categories_with_patterns}")


if __name__ == "__main__":
    input_file = "config/amazon_config.json"
    output_file = "config/amazon_shared.json"
    
    process_amazon_config(input_file, output_file)

