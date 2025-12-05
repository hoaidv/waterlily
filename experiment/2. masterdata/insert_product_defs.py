#!/usr/bin/env python3
"""
Insert product_defs, product_def_attributes, and update categories with product_def_id.
Steps:
3. Insert product_defs to MySQL
4. Insert product_def_attributes to MySQL
5. Match categories with product_defs, update product_def_id in MySQL
"""

import csv
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

def step3_insert_product_defs(conn):
    """Step 3: Insert product_defs to MySQL"""
    print("\n=== Step 3: Inserting product_defs ===")
    
    cursor = conn.cursor()
    
    # Read product_defs.csv
    product_defs_file = os.path.join(script_dir, 'product_defs.csv')
    id_mapping = {}  # Maps CSV id -> MySQL id
    
    with open(product_defs_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            csv_id = int(row['id'])
            name = row['name']
            
            # Insert product_def (let MySQL auto-increment)
            insert_sql = "INSERT INTO product_defs (name) VALUES (%s)"
            cursor.execute(insert_sql, (name,))
            mysql_id = cursor.lastrowid
            
            id_mapping[csv_id] = mysql_id
            print(f"  Inserted: {name} (CSV ID: {csv_id} -> MySQL ID: {mysql_id})")
    
    conn.commit()
    cursor.close()
    
    print(f"✓ Inserted {len(id_mapping)} product_defs")
    return id_mapping

def step4_insert_product_def_attributes(conn, id_mapping):
    """Step 4: Insert product_def_attributes to MySQL"""
    print("\n=== Step 4: Inserting product_def_attributes ===")
    
    cursor = conn.cursor()
    
    # Read product_def_attributes.csv
    attributes_file = os.path.join(script_dir, 'product_def_attributes.csv')
    inserted_count = 0
    skipped_count = 0
    
    with open(attributes_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            csv_product_def_id = int(row['product_def_id'])
            mysql_product_def_id = id_mapping[csv_product_def_id]
            name = row['name']
            datatype = row['datatype']
            display_name = row['display_name']
            default_value = row['default_value'] if row['default_value'] else None
            validation_rules = row['validation_rules'] if row['validation_rules'] else '{}'
            
            # Insert with ON DUPLICATE KEY UPDATE (in case of duplicates)
            insert_sql = """
                INSERT INTO product_def_attributes 
                (product_def_id, name, datatype, display_name, default_value, validation_rules)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    datatype = VALUES(datatype),
                    display_name = VALUES(display_name),
                    default_value = VALUES(default_value),
                    validation_rules = VALUES(validation_rules)
            """
            
            try:
                cursor.execute(insert_sql, (
                    mysql_product_def_id,
                    name,
                    datatype,
                    display_name,
                    default_value,
                    validation_rules
                ))
                inserted_count += 1
            except mysql.connector.Error as e:
                print(f"  Warning: Error inserting {name} for product_def_id {mysql_product_def_id}: {e}")
                skipped_count += 1
    
    conn.commit()
    cursor.close()
    
    print(f"✓ Inserted {inserted_count} product_def_attributes")
    if skipped_count > 0:
        print(f"  (Skipped {skipped_count} due to errors)")

def step5_update_categories(conn, id_mapping):
    """Step 5: Update categories with product_def_id"""
    print("\n=== Step 5: Updating categories with product_def_id ===")
    
    cursor = conn.cursor()
    
    # Read category_product_def_mapping.csv
    mapping_file = os.path.join(script_dir, 'category_product_def_mapping.csv')
    updated_count = 0
    not_found_count = 0
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            category_id = int(row['category_id'])
            csv_product_def_id = int(row['product_def_id'])
            mysql_product_def_id = id_mapping[csv_product_def_id]
            
            # Update category
            update_sql = "UPDATE categories SET product_def_id = %s WHERE id = %s"
            cursor.execute(update_sql, (mysql_product_def_id, category_id))
            
            if cursor.rowcount > 0:
                updated_count += 1
            else:
                not_found_count += 1
                print(f"  Warning: Category ID {category_id} not found in database")
    
    conn.commit()
    cursor.close()
    
    print(f"✓ Updated {updated_count} categories")
    if not_found_count > 0:
        print(f"  (Could not find {not_found_count} categories in database)")

def main():
    """Main execution function"""
    print("Starting product_defs insertion process...")
    
    try:
        conn = connect_to_mysql()
        print("✓ Connected to MySQL database")
        
        # Step 3: Insert product_defs
        id_mapping = step3_insert_product_defs(conn)
        
        # Step 4: Insert product_def_attributes
        step4_insert_product_def_attributes(conn, id_mapping)
        
        # Step 5: Update categories
        step5_update_categories(conn, id_mapping)
        
        conn.close()
        print("\n✓ All steps completed successfully!")
        
    except mysql.connector.Error as e:
        print(f"\n✗ MySQL Error: {e}")
        return 1
    except FileNotFoundError as e:
        print(f"\n✗ File not found: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())

