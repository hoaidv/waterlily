#!/usr/bin/env python3
"""
Script to scan products from JSON files and insert them into MySQL database.

Usage:
    python import_products.py <path> <regex_pattern>

Example:
    python import_products.py do_not_remove_01 "amazon.*\.json"
"""

import json
import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from decimal import Decimal, InvalidOperation
import secrets

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.db_connector import get_db_connection, load_mysql_config, load_categories


def generate_random_bigint() -> int:
    """Generate a random BIGINT (64-bit integer)"""
    # Generate random 64-bit integer
    return secrets.randbits(63)  # Use 63 bits to ensure positive value


def parse_price(price_str: str) -> Tuple[Optional[Decimal], Optional[str]]:
    """
    Parse price string into decimal and currency.
    
    Examples:
        "VND310,784" -> (310784.00, "VND")
        "VND 168,440" -> (168440.00, "VND")
        "USD 19.99" -> (19.99, "USD")
        "$19.99" -> (19.99, "USD")
    
    Returns:
        Tuple of (decimal_price, currency_code) or (None, None) if parsing fails
    """
    if not price_str or not isinstance(price_str, str):
        return None, None
    
    price_str = price_str.strip()
    
    # Common currency codes (3-letter ISO codes)
    currency_pattern = r'([A-Z]{3})'
    
    # Try to extract currency code
    currency_match = re.search(currency_pattern, price_str)
    currency = None
    
    if currency_match:
        currency = currency_match.group(1)
        # Remove currency code from string
        price_str = re.sub(currency_pattern, '', price_str, count=1).strip()
    
    # Handle $ symbol
    if price_str.startswith('$'):
        currency = currency or 'USD'
        price_str = price_str[1:].strip()
    
    # Remove commas and other non-numeric characters except decimal point
    # Keep only digits and decimal point
    numeric_str = re.sub(r'[^\d.]', '', price_str)
    
    if not numeric_str:
        return None, None
    
    try:
        # Convert to Decimal
        decimal_price = Decimal(numeric_str)
        currency = currency or 'USD'  # Default to USD if no currency found
        return decimal_price, currency
    except (InvalidOperation, ValueError):
        return None, None


def validate_product(product: Dict[str, Any], valid_category_ids: Optional[set] = None) -> Tuple[bool, str]:
    """
    Validate that a product has all required fields.
    
    Args:
        product: Product dictionary to validate
        valid_category_ids: Optional set of valid category IDs for validation
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if not product.get('title'):
        return False, "Missing title"
    
    if not product.get('price'):
        return False, "Missing price"
    
    if not product.get('url'):
        return False, "Missing url"
    
    # Check attributes
    attributes = product.get('attributes', {})
    if not isinstance(attributes, dict):
        return False, "Attributes must be a dictionary"
    
    # Count non-empty attributes (excluding price which is stored separately)
    attribute_count = sum(1 for k, v in attributes.items() 
                         if k != 'price' and v and str(v).strip())
    
    if attribute_count < 2:
        return False, f"Need at least 2 attributes, found {attribute_count}"
    
    # Validate price can be parsed
    price_decimal, currency = parse_price(product['price'])
    if price_decimal is None:
        return False, f"Could not parse price: {product['price']}"
    
    # Validate category_id if provided
    if valid_category_ids is not None:
        category_id = product.get('category_id')
        if category_id is not None and category_id not in valid_category_ids:
            return False, f"Invalid category_id: {category_id}"
    
    return True, ""


def generate_random_string(length: int = 10) -> str:
    """Generate a random string of A-Z0-9 characters"""
    import string
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_base_sku(prefix: str) -> str:
    """Generate a base SKU for the product using prefix and random string"""
    random_part = generate_random_string(10)
    return f"{prefix}-{random_part}"


def generate_variant_sku(base_sku: str) -> str:
    """Generate a variant SKU (default variant)"""
    return f"{base_sku}-DEFAULT"


def scan_json_files(path: str, regex_pattern: str) -> List[Path]:
    """
    Scan for JSON files matching the regex pattern in the given path.
    
    Args:
        path: Directory path to scan
        regex_pattern: Regex pattern to match filenames (pure form, no escaping needed)
    
    Returns:
        List of matching file paths
    """
    path_obj = Path(path)
    
    if not path_obj.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    if not path_obj.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    
    # Compile regex pattern
    try:
        pattern = re.compile(regex_pattern)
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {e}")
    
    matching_files = []
    
    # Scan files in directory (non-recursive)
    for file_path in path_obj.iterdir():
        if file_path.is_file() and file_path.suffix == '.json':
            if pattern.search(file_path.name):
                matching_files.append(file_path)
    
    return sorted(matching_files)


def load_products_from_file(file_path: Path) -> List[Dict[str, Any]]:
    """Load products from a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products = data.get('products', [])
        if not isinstance(products, list):
            return []
        
        return products
    except json.JSONDecodeError as e:
        print(f"  Warning: Failed to parse JSON in {file_path.name}: {e}")
        return []
    except Exception as e:
        print(f"  Warning: Error reading {file_path.name}: {e}")
        return []


def insert_product(cursor, product: Dict[str, Any], source: str = "amazon", 
                   base_sku_prefix: str = "AMZ") -> Optional[int]:
    """
    Insert a product into the database.
    
    Args:
        cursor: Database cursor
        product: Product dictionary
        source: Source name
        base_sku_prefix: Prefix for base SKU generation
    
    Returns:
        Product ID if successful, None otherwise
    """
    # Generate product ID
    product_id = generate_random_bigint()
    
    # Generate base SKU with prefix and random string
    base_sku = generate_base_sku(base_sku_prefix)
    
    # Ensure base_sku is unique (retry if collision)
    max_retries = 10
    for _ in range(max_retries):
        cursor.execute("SELECT id FROM products WHERE base_sku = %s", (base_sku,))
        if cursor.fetchone() is None:
            break
        base_sku = generate_base_sku(base_sku_prefix)
    else:
        print(f"  Warning: Could not generate unique base_sku after {max_retries} attempts")
        return None
    
    # Prepare attributes JSON (exclude price as it's stored separately)
    attributes = {k: v for k, v in product.get('attributes', {}).items() if k != 'price'}
    
    # Insert product
    insert_query = """
        INSERT INTO products (
            id, base_sku, name, description, status, source, source_url,
            category_id, product_def_id, attributes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """
    
    try:
        cursor.execute(insert_query, (
            product_id,
            base_sku,
            product['title'],
            product.get('description'),
            'ACTIVE',
            source,
            product['url'],
            product.get('category_id'),
            None,  # product_def_id - can be set later
            json.dumps(attributes) if attributes else None
        ))
        
        return product_id
    except Exception as e:
        print(f"  Error inserting product: {e}")
        return None


def insert_product_variant(cursor, product_id: int, base_sku: str, 
                           price_decimal: Decimal, currency: str) -> Optional[int]:
    """
    Insert a default product variant.
    
    Returns:
        Variant ID if successful, None otherwise
    """
    # Generate variant ID
    variant_id = generate_random_bigint()
    
    # Generate variant SKU
    variant_sku = generate_variant_sku(base_sku)
    
    # Check if variant_sku already exists (shouldn't happen for default variant)
    cursor.execute("SELECT id FROM product_variants WHERE variant_sku = %s", (variant_sku,))
    if cursor.fetchone() is not None:
        print(f"  Warning: Variant with SKU {variant_sku} already exists, skipping")
        return None
    
    # Insert variant
    insert_query = """
        INSERT INTO product_variants (
            id, product_id, variant_sku, quantity, price, currency, attributes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s
        )
    """
    
    try:
        cursor.execute(insert_query, (
            variant_id,
            product_id,
            variant_sku,
            0,  # Default quantity
            price_decimal,
            currency,
            json.dumps({})  # Empty attributes for default variant
        ))
        
        return variant_id
    except Exception as e:
        print(f"  Error inserting variant: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Scan products from JSON files and insert into MySQL database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python import_products.py do_not_remove_01 "amazon.*\\.json" --base-sku-prefix AMZ --dry-run
  python import_products.py do_not_remove_01 "amazon.*\\.json" --base-sku-prefix AMZ --import
  python import_products.py do_not_remove_01 ".*\\.json" --base-sku-prefix AMZ --import
  
Note: Regex pattern is passed as-is. Use standard regex syntax.
      To match a literal dot, use \\. (may need shell escaping: "\\\\.json" or '\.json')
      --base-sku-prefix is required and will be used to generate base SKUs like: <prefix>-<10 random chars>
        """
    )
    
    parser.add_argument('path', help='Directory path to scan (e.g., do_not_remove_01)')
    parser.add_argument('regex', help='Regex pattern to match files (e.g., amazon.*.json)')
    
    # Mode selection (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--dry-run', action='store_true',
                           help='Count products without importing (default: False)')
    mode_group.add_argument('--import', dest='do_import', action='store_true',
                           help='Import products into database (default: True)')
    
    parser.add_argument('--config', help='Path to MySQL config file (default: ../mysql-config.json)',
                       default=None)
    parser.add_argument('--source', help='Source name for products (default: amazon)',
                       default='amazon')
    parser.add_argument('--base-sku-prefix', required=True,
                       help='Prefix for base SKU generation (e.g., AMZ)')
    
    args = parser.parse_args()
    
    # Default to import mode if neither is specified
    is_dry_run = args.dry_run
    if not args.dry_run and not args.do_import:
        is_dry_run = False  # Default to import mode
    
    # Resolve path relative to script directory
    script_dir = Path(__file__).parent
    scan_path = script_dir / args.path
    
    print("=" * 60)
    print("Product Import Script")
    print("=" * 60)
    print(f"Mode: {'DRY-RUN' if is_dry_run else 'IMPORT'}")
    print(f"Scan path: {scan_path}")
    print(f"Regex pattern: {args.regex}")
    print(f"Source: {args.source}")
    print(f"Base SKU prefix: {args.base_sku_prefix}")
    print()
    
    # Scan for matching files
    try:
        matching_files = scan_json_files(str(scan_path), args.regex)
        print(f"Found {len(matching_files)} matching file(s)")
        
        if not matching_files:
            print("No files found matching the pattern. Exiting.")
            return
        
        for file_path in matching_files:
            print(f"  - {file_path.name}")
        print()
    except Exception as e:
        print(f"Error scanning files: {e}")
        sys.exit(1)
    
    # Connect to database (needed for both dry-run and import)
    try:
        config_path = args.config
        if config_path:
            config_path = os.path.abspath(config_path)
        else:
            # Default to experiment/mysql-config.json
            config_path = script_dir.parent / 'mysql-config.json'
        
        connection = get_db_connection(str(config_path))
        cursor = connection.cursor()
        
        print(f"Connected to database: {load_mysql_config(str(config_path))['database']}")
        print()
        
        # Load valid category IDs for validation
        valid_categories = load_categories(cursor)
        valid_category_ids = set(valid_categories.keys())
        print(f"Loaded {len(valid_category_ids)} valid categories from database")
        print()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
    
    # Process files
    total_products_loaded = 0
    total_products_valid = 0
    total_products_inserted = 0
    total_variants_inserted = 0
    
    # Statistics for dry-run mode
    invalid_reasons = {}
    invalid_categories = {}
    
    try:
        for file_path in matching_files:
            print(f"Processing: {file_path.name}")
            
            products = load_products_from_file(file_path)
            total_products_loaded += len(products)
            
            print(f"  Loaded {len(products)} product(s)")
            
            valid_products = []
            for product in products:
                is_valid, error_msg = validate_product(product, valid_category_ids)
                if is_valid:
                    valid_products.append(product)
                else:
                    # Track invalid reasons
                    if is_dry_run:
                        reason = error_msg
                        invalid_reasons[reason] = invalid_reasons.get(reason, 0) + 1
                        
                        # Track invalid categories separately
                        if reason.startswith("Invalid category_id"):
                            category_id = product.get('category_id')
                            if category_id:
                                invalid_categories[category_id] = invalid_categories.get(category_id, 0) + 1
                    else:
                        print(f"  Skipping product (validation failed: {error_msg})")
            
            total_products_valid += len(valid_products)
            print(f"  Valid products: {len(valid_products)}")
            
            if is_dry_run:
                print(f"  Invalid products: {len(products) - len(valid_products)}")
            else:
                # Insert valid products
                for product in valid_products:
                    # Parse price
                    price_decimal, currency = parse_price(product['price'])
                    
                    # Insert product
                    product_id = insert_product(cursor, product, args.source, args.base_sku_prefix)
                    
                    if product_id:
                        # Get base_sku for variant
                        cursor.execute("SELECT base_sku FROM products WHERE id = %s", (product_id,))
                        row = cursor.fetchone()
                        if row:
                            base_sku = row[0]
                            
                            # Insert variant
                            variant_id = insert_product_variant(
                                cursor, product_id, base_sku, price_decimal, currency
                            )
                            
                            if variant_id:
                                total_products_inserted += 1
                                total_variants_inserted += 1
                            else:
                                # Rollback product if variant insertion fails
                                cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
                        else:
                            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
                
                # Commit after each file
                connection.commit()
                print(f"  Inserted {len(valid_products)} product(s) and variant(s)")
            print()
        
        # Print summary
        print("=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"Files processed: {len(matching_files)}")
        print(f"Total products loaded: {total_products_loaded}")
        print(f"Total products valid: {total_products_valid}")
        print(f"Total products invalid: {total_products_loaded - total_products_valid}")
        
        if is_dry_run:
            # Detailed statistics for dry-run
            print()
            print("Invalid Products by Reason:")
            for reason, count in sorted(invalid_reasons.items(), key=lambda x: x[1], reverse=True):
                print(f"  {reason}: {count}")
            
            if invalid_categories:
                print()
                print("Invalid Categories:")
                for category_id, count in sorted(invalid_categories.items(), key=lambda x: x[1], reverse=True):
                    print(f"  category_id {category_id}: {count} product(s)")
        else:
            print(f"Total products inserted: {total_products_inserted}")
            print(f"Total variants inserted: {total_variants_inserted}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during processing: {e}")
        import traceback
        traceback.print_exc()
        if not is_dry_run:
            connection.rollback()
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()

