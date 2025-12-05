#!/usr/bin/env python3
"""
Clear old and insert new product_defs based on category_attributes.py mapping.
1 category = 1 product_def
"""

import json
import mysql.connector
from mysql.connector import Error
import sys
import os
import importlib.util

# Import category_attributes module
script_dir = os.path.dirname(os.path.abspath(__file__))
category_attributes_path = os.path.join(script_dir, "category_attributes.py")
spec = importlib.util.spec_from_file_location("category_attributes", category_attributes_path)
category_attributes_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(category_attributes_module)
CATEGORY_ATTRIBUTES = category_attributes_module.CATEGORY_ATTRIBUTES


def load_mysql_config():
    """Load MySQL configuration from mysql-config.json"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mysql-config.json")
    with open(config_path, 'r') as f:
        return json.load(f)


def clear_old_data(cursor):
    """Clear old product_defs, product_def_attributes, and category links"""
    print("Clearing old data...")
    
    # Clear category links first (to avoid foreign key issues)
    cursor.execute("UPDATE categories SET product_def_id = NULL")
    print(f"  - Cleared {cursor.rowcount} category product_def_id links")
    
    # Clear product_def_attributes (will cascade delete if foreign key is set up)
    cursor.execute("DELETE FROM product_def_attributes")
    print(f"  - Deleted {cursor.rowcount} product_def_attributes")
    
    # Clear product_defs
    cursor.execute("DELETE FROM product_defs")
    print(f"  - Deleted {cursor.rowcount} product_defs")
    
    print("Old data cleared successfully.\n")


def insert_product_defs(cursor, connection):
    """Insert product_defs and product_def_attributes based on category mapping"""
    print("Inserting new product_defs...")
    
    # Map category_id -> product_def_id
    category_to_product_def = {}
    
    # Insert product_defs (one per category)
    insert_product_def_query = """
        INSERT INTO product_defs (name, created_at, updated_at)
        VALUES (%s, NOW(), NOW())
    """
    
    insert_product_def_attr_query = """
        INSERT INTO product_def_attributes 
        (product_def_id, name, datatype, display_name, default_value, validation_rules, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, JSON_OBJECT(), NOW(), NOW())
    """
    
    # Get category names from categories table
    cursor.execute("SELECT id, name FROM categories")
    category_map = {row[0]: row[1] for row in cursor.fetchall()}
    
    product_defs_inserted = 0
    attributes_inserted = 0
    
    for category_entry in CATEGORY_ATTRIBUTES:
        category_id = category_entry['id']
        attributes = category_entry['attributes']
        
        # Get category name
        category_name = category_map.get(category_id, f"Category {category_id}")
        
        # Insert product_def
        cursor.execute(insert_product_def_query, (category_name,))
        product_def_id = cursor.lastrowid
        category_to_product_def[category_id] = product_def_id
        product_defs_inserted += 1
        
        # Insert product_def_attributes
        for attr_name, attr_datatype, attr_display_name in attributes:
            # Use datatype as-is (it's stored as VARCHAR in the database)
            # validation_rules is set to JSON_OBJECT() in the SQL query
            
            cursor.execute(
                insert_product_def_attr_query,
                (product_def_id, attr_name, attr_datatype, attr_display_name, None)
            )
            attributes_inserted += 1
    
    connection.commit()
    print(f"  - Inserted {product_defs_inserted} product_defs")
    print(f"  - Inserted {attributes_inserted} product_def_attributes")
    print("Product_defs inserted successfully.\n")
    
    return category_to_product_def


def link_categories(cursor, connection, category_to_product_def):
    """Link categories.product_def_id with product_defs"""
    print("Linking categories to product_defs...")
    
    update_query = "UPDATE categories SET product_def_id = %s WHERE id = %s"
    
    linked_count = 0
    for category_id, product_def_id in category_to_product_def.items():
        cursor.execute(update_query, (product_def_id, category_id))
        linked_count += 1
    
    connection.commit()
    print(f"  - Linked {linked_count} categories to product_defs")
    print("Categories linked successfully.\n")


def main():
    """Main function"""
    try:
        # Load MySQL config
        config = load_mysql_config()
        
        # Connect to MySQL
        print("Connecting to MySQL...")
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config.get('charset', 'utf8mb4')
        )
        
        if connection.is_connected():
            print("Connected to MySQL successfully.\n")
            cursor = connection.cursor()
            
            try:
                # Clear old data
                clear_old_data(cursor)
                
                # Insert new product_defs
                category_to_product_def = insert_product_defs(cursor, connection)
                
                # Link categories
                link_categories(cursor, connection, category_to_product_def)
                
                print("=" * 50)
                print("SUCCESS: All operations completed successfully!")
                print("=" * 50)
                
            except Error as e:
                print(f"Error during operations: {e}")
                connection.rollback()
                raise
            finally:
                cursor.close()
                connection.close()
                print("\nMySQL connection closed.")
        
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

