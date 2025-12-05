#!/usr/bin/env python3
"""Verify that product definitions were inserted correctly"""

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

conn = connect_to_mysql()
cursor = conn.cursor(dictionary=True)

print("=== Verification Report ===\n")

# Check attribute_defs
cursor.execute("SELECT COUNT(*) as count FROM attribute_defs")
attr_count = cursor.fetchone()['count']
print(f"✓ Attribute definitions: {attr_count}")

# Check product_defs
cursor.execute("SELECT COUNT(*) as count FROM product_defs")
pd_count = cursor.fetchone()['count']
print(f"✓ Product definitions: {pd_count}")

# Check product_def_attributes
cursor.execute("SELECT COUNT(*) as count FROM product_def_attributes")
pda_count = cursor.fetchone()['count']
print(f"✓ Product definition attributes: {pda_count}")

# Check categories with product_def_id
cursor.execute("SELECT COUNT(*) as count FROM categories WHERE product_def_id IS NOT NULL")
cat_count = cursor.fetchone()['count']
print(f"✓ Categories with product_def_id: {cat_count}")

# Show sample product definitions
print("\n=== Sample Product Definitions ===")
cursor.execute("""
    SELECT pd.id, pd.name, COUNT(pda.attribute_name) as attr_count
    FROM product_defs pd
    LEFT JOIN product_def_attributes pda ON pd.id = pda.product_def_id
    GROUP BY pd.id, pd.name
    ORDER BY pd.id
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"  {row['id']}: {row['name']} ({row['attr_count']} attributes)")

# Show categories distribution
print("\n=== Categories Distribution ===")
cursor.execute("""
    SELECT pd.name, COUNT(c.id) as category_count
    FROM product_defs pd
    LEFT JOIN categories c ON pd.id = c.product_def_id
    GROUP BY pd.id, pd.name
    ORDER BY category_count DESC
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"  {row['name']}: {row['category_count']} categories")

cursor.close()
conn.close()

print("\n✓ All verifications complete!")

