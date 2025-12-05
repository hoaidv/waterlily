#!/usr/bin/env python3
"""
Database connector utility for loading categories and attributes from MySQL
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
import mysql.connector
from mysql.connector import Error


def load_mysql_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """Load MySQL configuration from JSON file"""
    if config_file is None:
        # Default to experiment/mysql-config.json
        config_file = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            '..',
            'mysql-config.json'
        )
    
    with open(config_file, 'r') as f:
        return json.load(f)


def get_db_connection(config_file: Optional[str] = None):
    """Create and return a MySQL database connection"""
    config = load_mysql_config(config_file)
    
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config.get('charset', 'utf8mb4'),
            connection_timeout=config.get('connection_timeout', 30)
        )
        
        if connection.is_connected():
            return connection
        else:
            raise Error("Failed to connect to database")
    
    except Error as e:
        raise Exception(f"Error connecting to MySQL: {e}")


def load_categories(cursor) -> Dict[int, Dict[str, Any]]:
    """
    Load all categories from the database
    Returns: Dict mapping category_id -> category data
    """
    query = """
        SELECT 
            c.id,
            c.name,
            c.description,
            c.product_def_id,
            pd.name as product_def_name
        FROM categories c
        LEFT JOIN product_defs pd ON c.product_def_id = pd.id
        ORDER BY c.id
    """
    
    cursor.execute(query)
    categories = {}
    
    for row in cursor.fetchall():
        category_id = row[0]
        categories[category_id] = {
            'id': category_id,
            'name': row[1],
            'description': row[2],
            'product_def_id': row[3],
            'product_def_name': row[4]
        }
    
    return categories


def load_category_by_name(cursor, category_name: str) -> Optional[Dict[str, Any]]:
    """
    Load a specific category by name
    Returns: Category data or None if not found
    """
    query = """
        SELECT 
            c.id,
            c.name,
            c.description,
            c.product_def_id,
            pd.name as product_def_name
        FROM categories c
        LEFT JOIN product_defs pd ON c.product_def_id = pd.id
        WHERE c.name = %s
    """
    
    cursor.execute(query, (category_name,))
    row = cursor.fetchone()
    
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'product_def_id': row[3],
            'product_def_name': row[4]
        }
    
    return None


def load_product_def_attributes(cursor, product_def_id: int) -> List[Dict[str, Any]]:
    """
    Load all attributes for a given product definition
    Returns: List of attribute definitions
    """
    query = """
        SELECT 
            id,
            product_def_id,
            name,
            datatype,
            display_name,
            default_value,
            validation_rules
        FROM product_def_attributes
        WHERE product_def_id = %s
        ORDER BY name
    """
    
    cursor.execute(query, (product_def_id,))
    attributes = []
    
    for row in cursor.fetchall():
        attributes.append({
            'id': row[0],
            'product_def_id': row[1],
            'name': row[2],
            'datatype': row[3],
            'display_name': row[4],
            'default_value': row[5],
            'validation_rules': json.loads(row[6]) if row[6] else {}
        })
    
    return attributes


def load_category_to_attributes(cursor) -> Dict[int, List[Dict[str, Any]]]:
    """
    Load mapping of category_id to required attributes
    Returns: Dict mapping category_id -> list of attribute definitions
    """
    # First get all categories
    categories = load_categories(cursor)
    
    # Then get attributes for each category's product_def
    category_attributes = {}
    
    for category_id, category_data in categories.items():
        product_def_id = category_data.get('product_def_id')
        if product_def_id:
            attributes = load_product_def_attributes(cursor, product_def_id)
            category_attributes[category_id] = attributes
        else:
            category_attributes[category_id] = []
    
    return category_attributes


def get_target_categories(cursor, category_names: List[str]) -> List[Dict[str, Any]]:
    """
    Load specific categories by name with their attributes
    Args:
        cursor: Database cursor
        category_names: List of category names to load
    Returns: List of category data with attributes
    """
    target_categories = []
    
    for category_name in category_names:
        category = load_category_by_name(cursor, category_name)
        
        if category:
            # Load attributes for this category
            product_def_id = category.get('product_def_id')
            if product_def_id:
                attributes = load_product_def_attributes(cursor, product_def_id)
                category['attributes'] = attributes
            else:
                category['attributes'] = []
            
            target_categories.append(category)
        else:
            print(f"Warning: Category '{category_name}' not found in database")
    
    return target_categories


def get_all_distinct_attributes(cursor) -> List[str]:
    """
    Get all distinct attribute names from product_def_attributes
    Returns: List of unique attribute names
    """
    query = """
        SELECT DISTINCT name
        FROM product_def_attributes
        ORDER BY name
    """
    
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


# Context manager for database operations
class DatabaseConnection:
    """Context manager for database connections"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = get_db_connection(self.config_file)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()


def main():
    """Test the database connector"""
    print("Testing Database Connector")
    print("=" * 60)
    
    try:
        with DatabaseConnection() as cursor:
            # Test loading categories
            print("\n1. Loading all categories...")
            categories = load_categories(cursor)
            print(f"   Found {len(categories)} categories")
            
            # Show first 5 categories
            for i, (cat_id, cat_data) in enumerate(list(categories.items())[:5], 1):
                print(f"   {i}. {cat_data['name']} (ID: {cat_id}, Def: {cat_data['product_def_id']})")
            
            # Test loading specific categories
            print("\n2. Loading target categories...")
            target_names = ['iPhones', 'Men\'s Clothing', 'Mirrorless Cameras']
            target_categories = get_target_categories(cursor, target_names)
            
            for category in target_categories:
                print(f"\n   Category: {category['name']}")
                print(f"   Product Def ID: {category['product_def_id']}")
                print(f"   Attributes: {len(category['attributes'])}")
                
                # Show first 5 attributes
                for i, attr in enumerate(category['attributes'][:5], 1):
                    print(f"      {i}. {attr['name']} ({attr['datatype']})")
            
            # Test getting all distinct attributes
            print("\n3. Getting all distinct attributes...")
            all_attributes = get_all_distinct_attributes(cursor)
            print(f"   Found {len(all_attributes)} distinct attributes")
            print(f"   First 10: {', '.join(all_attributes[:10])}")
        
        print("\n" + "=" * 60)
        print("✓ Database connector test completed successfully")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

