#!/usr/bin/env python3
"""
Verify that product_defs, product_def_attributes, and category mappings were inserted correctly.
"""

import json
import mysql.connector
import os

# Load MySQL config
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, '..', 'mysql-config.json')
with open(config_path, 'r') as f:
    mysql_config = json.load(f)

def connect_to_mysql():
    """Connect to MySQL database"""
    return mysql.connector.connect(
        host=mysql_config['host'],
        port=mysql_config['port'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database'],
        charset=mysql_config['charset']
    )

def verify():
    """Verify the inserted data"""
    conn = connect_to_mysql()
    cursor = conn.cursor(dictionary=True)
    
    print("=== Verification Results ===\n")
    
    # 1. Count product_defs
    cursor.execute("SELECT COUNT(*) as count FROM product_defs")
    result = cursor.fetchone()
    print(f"1. Product Defs: {result['count']}")
    
    # 2. Count product_def_attributes
    cursor.execute("SELECT COUNT(*) as count FROM product_def_attributes")
    result = cursor.fetchone()
    print(f"2. Product Def Attributes: {result['count']}")
    
    # 3. Count categories with product_def_id
    cursor.execute("SELECT COUNT(*) as count FROM categories WHERE product_def_id IS NOT NULL")
    result = cursor.fetchone()
    print(f"3. Categories with product_def_id: {result['count']}")
    
    # 4. Count categories without product_def_id
    cursor.execute("SELECT COUNT(*) as count FROM categories WHERE product_def_id IS NULL")
    result = cursor.fetchone()
    print(f"4. Categories without product_def_id: {result['count']}")
    
    # 5. Sample product_def with attributes
    print("\n5. Sample Product Def (Computers and Laptops):")
    cursor.execute("""
        SELECT pd.id, pd.name, COUNT(pda.id) as attr_count
        FROM product_defs pd
        LEFT JOIN product_def_attributes pda ON pd.id = pda.product_def_id
        WHERE pd.name = 'Computers and Laptops'
        GROUP BY pd.id, pd.name
    """)
    result = cursor.fetchone()
    if result:
        print(f"   ID: {result['id']}, Name: {result['name']}, Attributes: {result['attr_count']}")
        
        # Show attributes
        cursor.execute("""
            SELECT name, datatype, display_name
            FROM product_def_attributes
            WHERE product_def_id = %s
            ORDER BY name
        """, (result['id'],))
        attrs = cursor.fetchall()
        print(f"   Attributes ({len(attrs)}):")
        for attr in attrs[:5]:  # Show first 5
            print(f"     - {attr['name']} ({attr['datatype']}): {attr['display_name']}")
        if len(attrs) > 5:
            print(f"     ... and {len(attrs) - 5} more")
    
    # 6. Sample category mapping
    print("\n6. Sample Category Mappings:")
    cursor.execute("""
        SELECT c.id, c.name, pd.id as product_def_id, pd.name as product_def_name
        FROM categories c
        JOIN product_defs pd ON c.product_def_id = pd.id
        LIMIT 5
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"   Category '{row['name']}' (ID: {row['id']}) -> Product Def '{row['product_def_name']}' (ID: {row['product_def_id']})")
    
    # 7. Product def distribution
    print("\n7. Top 10 Product Defs by Category Count:")
    cursor.execute("""
        SELECT pd.name, COUNT(c.id) as category_count
        FROM product_defs pd
        LEFT JOIN categories c ON pd.id = c.product_def_id
        GROUP BY pd.id, pd.name
        ORDER BY category_count DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"   {row['name']}: {row['category_count']} categories")
    
    cursor.close()
    conn.close()
    
    print("\n✓ Verification complete!")

if __name__ == '__main__':
    verify()

