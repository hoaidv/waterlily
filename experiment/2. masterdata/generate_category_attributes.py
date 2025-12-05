#!/usr/bin/env python3
"""
Generate category attributes for all categories in categories.csv
This script analyzes each category individually to generate specific, relevant attributes.
"""

import csv
import re

def generate_attributes_for_category(category_id, name, description):
    """
    Generate relevant attributes for a category by analyzing its specific name and description.
    This function thinks about what attributes products in THIS specific category would need.
    """
    name_lower = name.lower().strip()
    desc_lower = (description.lower().strip() if description else "")
    combined = f"{name_lower} {desc_lower}".strip()
    
    attributes = []
    
    # Build a comprehensive category-specific attribute mapping
    # Each category gets attributes that make sense for THAT specific category
    
    # === BATTERIES ===
    if 'aa battery' in combined or name_lower == 'aa batteries':
        attributes = [
            ('voltage', 'STRING', 'Voltage per cell (typically 1.5V)'),
            ('chemistry', 'STRING', 'Battery chemistry (Alkaline, Lithium, etc.)'),
            ('quantity', 'NUMBER', 'Number of batteries in pack'),
            ('rechargeable', 'BOOLEAN', 'Rechargeable'),
            ('brand', 'STRING', 'Brand name'),
            ('expiration_date', 'STRING', 'Expiration date'),
        ]
    elif 'aaa battery' in combined or name_lower == 'aaa batteries':
        attributes = [
            ('voltage', 'STRING', 'Voltage per cell (typically 1.5V)'),
            ('chemistry', 'STRING', 'Battery chemistry (Alkaline, Lithium, etc.)'),
            ('quantity', 'NUMBER', 'Number of batteries in pack'),
            ('rechargeable', 'BOOLEAN', 'Rechargeable'),
            ('brand', 'STRING', 'Brand name'),
            ('expiration_date', 'STRING', 'Expiration date'),
        ]
    elif 'battery' in combined and 'charger' not in combined:
        attributes = [
            ('voltage', 'STRING', 'Voltage rating'),
            ('capacity', 'STRING', 'Battery capacity (mAh)'),
            ('chemistry', 'STRING', 'Battery chemistry type'),
            ('size', 'STRING', 'Battery size'),
            ('quantity', 'NUMBER', 'Number of batteries in pack'),
            ('rechargeable', 'BOOLEAN', 'Rechargeable'),
            ('brand', 'STRING', 'Brand name'),
        ]
    
    # === BOOKS ===
    elif name_lower == 'books' or name_lower == 'fiction books':
        attributes = [
            ('title', 'STRING', 'Book title'),
            ('author', 'STRING', 'Author name'),
            ('publisher', 'STRING', 'Publisher'),
            ('isbn', 'STRING', 'ISBN-13 or ISBN-10'),
            ('publication_date', 'STRING', 'Publication date'),
            ('language', 'STRING', 'Language'),
            ('format', 'STRING', 'Format (Hardcover, Paperback, eBook, Audiobook)'),
            ('pages', 'NUMBER', 'Number of pages'),
            ('genre', 'STRING', 'Genre'),
            ('edition', 'STRING', 'Edition number'),
        ]
    elif 'mystery' in combined or 'thriller' in combined:
        attributes = [
            ('title', 'STRING', 'Book title'),
            ('author', 'STRING', 'Author name'),
            ('publisher', 'STRING', 'Publisher'),
            ('isbn', 'STRING', 'ISBN'),
            ('publication_date', 'STRING', 'Publication date'),
            ('language', 'STRING', 'Language'),
            ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
            ('pages', 'NUMBER', 'Number of pages'),
            ('series', 'STRING', 'Series name (if part of a series)'),
        ]
    elif 'textbook' in combined:
        attributes = [
            ('title', 'STRING', 'Textbook title'),
            ('author', 'STRING', 'Author name'),
            ('publisher', 'STRING', 'Publisher'),
            ('isbn', 'STRING', 'ISBN'),
            ('edition', 'STRING', 'Edition'),
            ('publication_date', 'STRING', 'Publication date'),
            ('subject', 'STRING', 'Subject area'),
            ('grade_level', 'STRING', 'Grade level'),
            ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
            ('pages', 'NUMBER', 'Number of pages'),
        ]
    elif 'book' in combined:
        attributes = [
            ('title', 'STRING', 'Book title'),
            ('author', 'STRING', 'Author name'),
            ('publisher', 'STRING', 'Publisher'),
            ('isbn', 'STRING', 'ISBN'),
            ('publication_date', 'STRING', 'Publication date'),
            ('language', 'STRING', 'Language'),
            ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
            ('pages', 'NUMBER', 'Number of pages'),
            ('genre', 'STRING', 'Genre'),
        ]
    
    # === ELECTRONICS - PHONES ===
    elif 'iphone' in combined or name_lower == 'iphones':
        attributes = [
            ('model', 'STRING', 'iPhone model (e.g., iPhone 15 Pro)'),
            ('storage', 'STRING', 'Storage capacity (128GB, 256GB, 512GB, 1TB)'),
            ('color', 'STRING', 'Color'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('year', 'NUMBER', 'Release year'),
            ('network', 'STRING', 'Network compatibility (5G, 4G LTE)'),
            ('condition', 'STRING', 'Condition (New, Refurbished, Used)'),
        ]
    elif 'android phone' in combined or ('smartphone' in combined and 'iphone' not in combined):
        attributes = [
            ('brand', 'STRING', 'Brand (Samsung, Google, OnePlus, etc.)'),
            ('model', 'STRING', 'Model name'),
            ('storage', 'STRING', 'Storage capacity'),
            ('ram', 'STRING', 'RAM size'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('resolution', 'STRING', 'Display resolution'),
            ('processor', 'STRING', 'Processor'),
            ('camera_megapixels', 'STRING', 'Camera megapixels'),
            ('battery_capacity', 'STRING', 'Battery capacity (mAh)'),
            ('operating_system', 'STRING', 'Android version'),
            ('color', 'STRING', 'Color'),
            ('year', 'NUMBER', 'Release year'),
        ]
    elif 'phone' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('storage', 'STRING', 'Storage capacity'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('color', 'STRING', 'Color'),
            ('year', 'NUMBER', 'Release year'),
        ]
    
    # === LAPTOPS ===
    elif 'macbook' in combined:
        attributes = [
            ('model', 'STRING', 'MacBook model (Air, Pro)'),
            ('screen_size', 'STRING', 'Screen size (13", 14", 16")'),
            ('processor', 'STRING', 'Processor (M1, M2, M3, Intel)'),
            ('ram', 'STRING', 'RAM size'),
            ('storage', 'STRING', 'Storage capacity (SSD)'),
            ('color', 'STRING', 'Color'),
            ('year', 'NUMBER', 'Release year'),
            ('condition', 'STRING', 'Condition'),
        ]
    elif 'chromebook' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('processor', 'STRING', 'Processor'),
            ('ram', 'STRING', 'RAM size'),
            ('storage', 'STRING', 'Storage capacity'),
            ('color', 'STRING', 'Color'),
            ('year', 'NUMBER', 'Release year'),
        ]
    elif 'gaming laptop' in combined or 'gaming pc' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('processor', 'STRING', 'CPU processor'),
            ('ram', 'STRING', 'RAM size'),
            ('storage', 'STRING', 'Storage capacity'),
            ('storage_type', 'STRING', 'Storage type (SSD, HDD)'),
            ('graphics_card', 'STRING', 'Graphics card (GPU)'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
            ('resolution', 'STRING', 'Display resolution'),
            ('operating_system', 'STRING', 'Operating system'),
            ('color', 'STRING', 'Color'),
            ('year', 'NUMBER', 'Release year'),
        ]
    elif 'laptop' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('processor', 'STRING', 'CPU processor'),
            ('ram', 'STRING', 'RAM size'),
            ('storage', 'STRING', 'Storage capacity'),
            ('storage_type', 'STRING', 'Storage type (SSD/HDD)'),
            ('operating_system', 'STRING', 'Operating system'),
            ('color', 'STRING', 'Color'),
            ('weight', 'STRING', 'Weight'),
            ('year', 'NUMBER', 'Release year'),
        ]
    
    # === CAMERAS ===
    elif 'dslr camera' in combined or 'dslr' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand (Canon, Nikon, Sony, etc.)'),
            ('model', 'STRING', 'Camera model'),
            ('megapixels', 'STRING', 'Megapixels'),
            ('sensor_size', 'STRING', 'Sensor size (Full Frame, APS-C, etc.)'),
            ('lens_mount', 'STRING', 'Lens mount type'),
            ('iso_range', 'STRING', 'ISO range'),
            ('video_resolution', 'STRING', 'Video resolution'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('weight', 'STRING', 'Weight'),
            ('year', 'NUMBER', 'Release year'),
        ]
    elif 'mirrorless camera' in combined or 'mirrorless' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Camera model'),
            ('megapixels', 'STRING', 'Megapixels'),
            ('sensor_size', 'STRING', 'Sensor size'),
            ('lens_mount', 'STRING', 'Lens mount type'),
            ('iso_range', 'STRING', 'ISO range'),
            ('video_resolution', 'STRING', 'Video resolution'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('weight', 'STRING', 'Weight'),
            ('year', 'NUMBER', 'Release year'),
        ]
    elif 'camera' in combined and 'flash' not in combined and 'bag' not in combined and 'lens' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Camera model'),
            ('megapixels', 'STRING', 'Megapixels'),
            ('sensor_size', 'STRING', 'Sensor size'),
            ('zoom', 'STRING', 'Optical zoom'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('weight', 'STRING', 'Weight'),
            ('year', 'NUMBER', 'Release year'),
        ]
    
    # === CLOTHING - WOMEN'S ===
    elif "women's sneaker" in combined or "women's shoe" in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (US)'),
            ('width', 'STRING', 'Width'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material'),
            ('style', 'STRING', 'Style'),
            ('closure', 'STRING', 'Closure type'),
            ('heel_height', 'STRING', 'Heel height'),
        ]
    elif "women's jean" in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('waist_size', 'STRING', 'Waist size'),
            ('inseam', 'STRING', 'Inseam length'),
            ('fit', 'STRING', 'Fit (Skinny, Straight, Bootcut, etc.)'),
            ('rise', 'STRING', 'Rise (Low, Mid, High)'),
            ('color', 'STRING', 'Color/Wash'),
            ('material', 'STRING', 'Material (Denim composition)'),
            ('stretch', 'BOOLEAN', 'Stretch denim'),
        ]
    elif "women's dress" in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material/Fabric'),
            ('length', 'STRING', 'Dress length'),
            ('sleeve_length', 'STRING', 'Sleeve length'),
            ('style', 'STRING', 'Style'),
            ('occasion', 'STRING', 'Occasion'),
            ('care_instructions', 'STRING', 'Care instructions'),
        ]
    elif "women's" in combined and ('top' in combined or 'shirt' in combined or 'blouse' in combined):
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material/Fabric'),
            ('sleeve_length', 'STRING', 'Sleeve length'),
            ('fit', 'STRING', 'Fit type'),
            ('style', 'STRING', 'Style'),
            ('care_instructions', 'STRING', 'Care instructions'),
        ]
    elif "women's" in combined and 'pant' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('waist_size', 'STRING', 'Waist size'),
            ('inseam', 'STRING', 'Inseam length'),
            ('fit', 'STRING', 'Fit type'),
            ('rise', 'STRING', 'Rise'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material/Fabric'),
        ]
    
    # === CLOTHING - MEN'S ===
    elif "men's sneaker" in combined or "men's shoe" in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (US)'),
            ('width', 'STRING', 'Width'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material'),
            ('style', 'STRING', 'Style'),
            ('closure', 'STRING', 'Closure type'),
        ]
    elif "men's jean" in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('waist_size', 'STRING', 'Waist size'),
            ('inseam', 'STRING', 'Inseam length'),
            ('fit', 'STRING', 'Fit (Slim, Straight, Relaxed, etc.)'),
            ('rise', 'STRING', 'Rise'),
            ('color', 'STRING', 'Color/Wash'),
            ('material', 'STRING', 'Material'),
            ('stretch', 'BOOLEAN', 'Stretch denim'),
        ]
    elif "men's" in combined and ('shirt' in combined or 'tee' in combined):
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material/Fabric'),
            ('sleeve_length', 'STRING', 'Sleeve length'),
            ('fit', 'STRING', 'Fit type'),
            ('style', 'STRING', 'Style'),
        ]
    elif "men's" in combined and 'pant' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('waist_size', 'STRING', 'Waist size'),
            ('inseam', 'STRING', 'Inseam length'),
            ('fit', 'STRING', 'Fit type'),
            ('rise', 'STRING', 'Rise'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material/Fabric'),
        ]
    
    # === CLOTHING - KIDS ===
    elif "girls'" in combined or "boys'" in combined or "kids'" in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('age_range', 'STRING', 'Age range'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material/Fabric'),
            ('care_instructions', 'STRING', 'Care instructions'),
        ]
    
    # === BABY PRODUCTS ===
    elif 'baby bottle' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Bottle size (oz)'),
            ('material', 'STRING', 'Material (Glass, Plastic, Silicone)'),
            ('nipple_type', 'STRING', 'Nipple type'),
            ('age_range', 'STRING', 'Age range'),
            ('bpa_free', 'BOOLEAN', 'BPA-free'),
            ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
        ]
    elif 'baby' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('age_range', 'STRING', 'Age range'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material'),
            ('safety_certification', 'STRING', 'Safety certification'),
        ]
    
    # === FURNITURE ===
    elif 'dining table' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material (Wood, Glass, Metal)'),
            ('color', 'STRING', 'Color/Finish'),
            ('seating_capacity', 'NUMBER', 'Seating capacity'),
            ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
            ('shape', 'STRING', 'Shape (Round, Rectangular, Square)'),
            ('assembly_required', 'BOOLEAN', 'Assembly required'),
        ]
    elif 'sofa' in combined or 'couch' in combined or 'loveseat' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material (Fabric, Leather, etc.)'),
            ('color', 'STRING', 'Color'),
            ('seating_capacity', 'NUMBER', 'Seating capacity'),
            ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
            ('assembly_required', 'BOOLEAN', 'Assembly required'),
            ('style', 'STRING', 'Style'),
        ]
    elif 'chair' in combined and 'high' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('dimensions', 'STRING', 'Dimensions'),
            ('weight_capacity', 'STRING', 'Weight capacity'),
            ('assembly_required', 'BOOLEAN', 'Assembly required'),
        ]
    elif 'furniture' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color/Finish'),
            ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
            ('assembly_required', 'BOOLEAN', 'Assembly required'),
            ('style', 'STRING', 'Style'),
        ]
    
    # === KITCHEN ===
    elif 'coffee maker' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model'),
            ('capacity', 'STRING', 'Capacity (cups)'),
            ('type', 'STRING', 'Type (Drip, Espresso, French Press, etc.)'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material'),
            ('programmable', 'BOOLEAN', 'Programmable'),
        ]
    elif 'kettle' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Capacity (liters)'),
            ('material', 'STRING', 'Material (Stainless Steel, Glass, etc.)'),
            ('color', 'STRING', 'Color'),
            ('cordless', 'BOOLEAN', 'Cordless'),
            ('temperature_control', 'BOOLEAN', 'Temperature control'),
        ]
    elif 'pot' in combined or 'pan' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('size', 'STRING', 'Size/Diameter'),
            ('capacity', 'STRING', 'Capacity'),
            ('non_stick', 'BOOLEAN', 'Non-stick coating'),
            ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
            ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
        ]
    
    # === STORAGE ===
    elif 'hard drive' in combined or 'ssd' in combined or 'external' in combined and 'storage' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Storage capacity'),
            ('type', 'STRING', 'Type (HDD, SSD, NVMe)'),
            ('interface', 'STRING', 'Interface (USB 3.0, USB-C, Thunderbolt)'),
            ('form_factor', 'STRING', 'Form factor'),
            ('speed', 'STRING', 'Read/Write speed'),
        ]
    elif 'ram memory' in combined or 'memory' in combined and 'card' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Memory capacity'),
            ('type', 'STRING', 'Type (DDR4, DDR5)'),
            ('speed', 'STRING', 'Speed (MHz)'),
            ('form_factor', 'STRING', 'Form factor'),
        ]
    
    # === TVs & MONITORS ===
    elif 'led tv' in combined or 'oled tv' in combined or '4k tv' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('resolution', 'STRING', 'Resolution (4K, 1080p, 8K)'),
            ('display_type', 'STRING', 'Display type (LED, OLED, QLED)'),
            ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
            ('smart_tv', 'BOOLEAN', 'Smart TV features'),
            ('hdr', 'BOOLEAN', 'HDR support'),
            ('year', 'NUMBER', 'Release year'),
        ]
    elif 'gaming monitor' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('resolution', 'STRING', 'Resolution'),
            ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
            ('response_time', 'STRING', 'Response time (ms)'),
            ('panel_type', 'STRING', 'Panel type (IPS, VA, TN)'),
            ('curved', 'BOOLEAN', 'Curved display'),
        ]
    elif 'monitor' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('resolution', 'STRING', 'Resolution'),
            ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
            ('panel_type', 'STRING', 'Panel type'),
        ]
    
    # === HEADPHONES & AUDIO ===
    elif 'wireless headphone' in combined or 'bluetooth headphone' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Over-ear, On-ear, In-ear)'),
            ('noise_cancellation', 'BOOLEAN', 'Noise cancellation'),
            ('battery_life', 'STRING', 'Battery life (hours)'),
            ('color', 'STRING', 'Color'),
            ('water_resistant', 'BOOLEAN', 'Water resistant'),
        ]
    elif 'headphone' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type'),
            ('wireless', 'BOOLEAN', 'Wireless'),
            ('noise_cancellation', 'BOOLEAN', 'Noise cancellation'),
            ('color', 'STRING', 'Color'),
        ]
    
    # === MUSICAL INSTRUMENTS ===
    elif 'guitar' in combined and 'case' not in combined and 'string' not in combined and 'pick' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Acoustic, Electric, Bass)'),
            ('color', 'STRING', 'Color/Finish'),
            ('number_of_strings', 'NUMBER', 'Number of strings'),
            ('body_material', 'STRING', 'Body material'),
            ('scale_length', 'STRING', 'Scale length'),
        ]
    elif 'piano' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Acoustic, Digital)'),
            ('number_of_keys', 'NUMBER', 'Number of keys'),
            ('color', 'STRING', 'Color/Finish'),
            ('dimensions', 'STRING', 'Dimensions'),
        ]
    elif any(inst in combined for inst in ['saxophone', 'trumpet', 'flute', 'clarinet', 'trombone', 'violin', 'cello', 'viola']):
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type'),
            ('key', 'STRING', 'Key'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color/Finish'),
        ]
    
    # === SPORTS ===
    elif 'soccer' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Ball size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('indoor_outdoor', 'STRING', 'Indoor/Outdoor'),
        ]
    elif 'basketball' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Ball size'),
            ('material', 'STRING', 'Material'),
            ('indoor_outdoor', 'STRING', 'Indoor/Outdoor'),
        ]
    elif 'bike' in combined or 'bicycle' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model'),
            ('type', 'STRING', 'Type (Mountain, Road, Hybrid, etc.)'),
            ('frame_size', 'STRING', 'Frame size'),
            ('wheel_size', 'STRING', 'Wheel size'),
            ('number_of_speeds', 'NUMBER', 'Number of speeds'),
            ('color', 'STRING', 'Color'),
        ]
    
    # === BEAUTY & PERSONAL CARE ===
    elif 'makeup' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('product_type', 'STRING', 'Product type'),
            ('shade', 'STRING', 'Shade/Color'),
            ('size', 'STRING', 'Size'),
            ('cruelty_free', 'BOOLEAN', 'Cruelty-free'),
            ('vegan', 'BOOLEAN', 'Vegan'),
        ]
    elif 'shampoo' in combined or 'conditioner' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (oz)'),
            ('hair_type', 'STRING', 'Hair type'),
            ('ingredients', 'STRING', 'Key ingredients'),
            ('sulfate_free', 'BOOLEAN', 'Sulfate-free'),
        ]
    
    # === PET SUPPLIES ===
    elif 'dog' in combined and ('food' in combined or 'toy' in combined or 'bed' in combined):
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('age_range', 'STRING', 'Age range'),
            ('breed_size', 'STRING', 'Breed size (Small, Medium, Large)'),
        ]
    elif 'cat' in combined and ('food' in combined or 'toy' in combined or 'litter' in combined):
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('age_range', 'STRING', 'Age range'),
            ('type', 'STRING', 'Type'),
        ]
    
    # === FOOD ===
    elif 'coffee' in combined and 'maker' not in combined and 'bean' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('roast_level', 'STRING', 'Roast level (Light, Medium, Dark)'),
            ('origin', 'STRING', 'Origin'),
            ('weight', 'STRING', 'Weight'),
            ('grind', 'STRING', 'Grind (Whole Bean, Ground)'),
            ('flavor_notes', 'STRING', 'Flavor notes'),
        ]
    elif 'candy' in combined or 'chocolate' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('flavor', 'STRING', 'Flavor'),
            ('package_size', 'STRING', 'Package size'),
            ('weight', 'STRING', 'Weight'),
            ('ingredients', 'STRING', 'Ingredients'),
            ('allergens', 'STRING', 'Allergen information'),
        ]
    
    # === MORE SPECIFIC CATEGORIES ===
    elif 'graphics card' in combined or 'gpu' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand (NVIDIA, AMD)'),
            ('model', 'STRING', 'Model name'),
            ('memory', 'STRING', 'VRAM (GB)'),
            ('memory_type', 'STRING', 'Memory type (GDDR6, GDDR6X)'),
            ('clock_speed', 'STRING', 'Clock speed'),
            ('interface', 'STRING', 'Interface (PCIe)'),
            ('power_consumption', 'STRING', 'Power consumption (watts)'),
        ]
    elif 'fitness tracker' in combined or 'activity tracker' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('display_type', 'STRING', 'Display type'),
            ('battery_life', 'STRING', 'Battery life (days)'),
            ('water_resistant', 'BOOLEAN', 'Water resistant'),
            ('heart_rate_monitor', 'BOOLEAN', 'Heart rate monitor'),
            ('gps', 'BOOLEAN', 'GPS'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'smartwatch' in combined or 'smart watch' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('screen_size', 'STRING', 'Screen size'),
            ('operating_system', 'STRING', 'Operating system'),
            ('battery_life', 'STRING', 'Battery life'),
            ('water_resistant', 'BOOLEAN', 'Water resistant'),
            ('cellular', 'BOOLEAN', 'Cellular connectivity'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'tablet' in combined and 'ipad' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('storage', 'STRING', 'Storage capacity'),
            ('ram', 'STRING', 'RAM size'),
            ('operating_system', 'STRING', 'Operating system'),
            ('color', 'STRING', 'Color'),
            ('cellular', 'BOOLEAN', 'Cellular connectivity'),
        ]
    elif 'ipad' in combined:
        attributes = [
            ('model', 'STRING', 'iPad model'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('storage', 'STRING', 'Storage capacity'),
            ('cellular', 'BOOLEAN', 'Cellular connectivity'),
            ('color', 'STRING', 'Color'),
            ('year', 'NUMBER', 'Release year'),
        ]
    elif 'bed sheet' in combined or 'bedding' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (Twin, Full, Queen, King)'),
            ('thread_count', 'STRING', 'Thread count'),
            ('material', 'STRING', 'Material (Cotton, Microfiber, etc.)'),
            ('color', 'STRING', 'Color'),
            ('pattern', 'STRING', 'Pattern'),
            ('care_instructions', 'STRING', 'Care instructions'),
        ]
    elif 'mattress' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (Twin, Full, Queen, King)'),
            ('type', 'STRING', 'Type (Memory Foam, Innerspring, Hybrid)'),
            ('firmness', 'STRING', 'Firmness level'),
            ('thickness', 'STRING', 'Thickness (inches)'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'backpack' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Capacity (liters)'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('number_of_compartments', 'NUMBER', 'Number of compartments'),
            ('laptop_compartment', 'BOOLEAN', 'Laptop compartment'),
            ('water_resistant', 'BOOLEAN', 'Water resistant'),
        ]
    elif 'wallet' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material (Leather, Fabric, etc.)'),
            ('color', 'STRING', 'Color'),
            ('type', 'STRING', 'Type (Bifold, Trifold, Cardholder)'),
            ('rfid_blocking', 'BOOLEAN', 'RFID blocking'),
        ]
    elif 'jewelry' in combined or 'ring' in combined or 'necklace' in combined or 'bracelet' in combined or 'earring' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
            ('stone_type', 'STRING', 'Stone type (if applicable)'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'watch' in combined and 'smart' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Analog, Digital, Hybrid)'),
            ('material', 'STRING', 'Material'),
            ('band_material', 'STRING', 'Band material'),
            ('water_resistant', 'BOOLEAN', 'Water resistant'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'towel' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material (Cotton, Microfiber, etc.)'),
            ('color', 'STRING', 'Color'),
            ('weight', 'STRING', 'Weight (GSM)'),
            ('absorbency', 'STRING', 'Absorbency level'),
        ]
    elif 'candle' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('scent', 'STRING', 'Scent/Fragrance'),
            ('size', 'STRING', 'Size'),
            ('burn_time', 'STRING', 'Burn time (hours)'),
            ('material', 'STRING', 'Material (Soy, Beeswax, Paraffin)'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'vitamin' in combined or 'supplement' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('product_type', 'STRING', 'Product type'),
            ('dosage', 'STRING', 'Dosage per serving'),
            ('quantity', 'NUMBER', 'Quantity (count)'),
            ('expiration_date', 'STRING', 'Expiration date'),
            ('ingredients', 'STRING', 'Key ingredients'),
        ]
    elif 'toy' in combined and 'cat' not in combined and 'dog' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('age_range', 'STRING', 'Age range'),
            ('material', 'STRING', 'Material'),
            ('batteries_required', 'BOOLEAN', 'Batteries required'),
            ('number_of_players', 'STRING', 'Number of players'),
            ('theme', 'STRING', 'Theme'),
        ]
    elif 'game' in combined and 'video' not in combined and 'board' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('age_range', 'STRING', 'Age range'),
            ('number_of_players', 'STRING', 'Number of players'),
            ('play_time', 'STRING', 'Play time (minutes)'),
            ('theme', 'STRING', 'Theme'),
        ]
    elif 'board game' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('age_range', 'STRING', 'Age range'),
            ('number_of_players', 'STRING', 'Number of players'),
            ('play_time', 'STRING', 'Play time (minutes)'),
            ('theme', 'STRING', 'Theme'),
            ('difficulty', 'STRING', 'Difficulty level'),
        ]
    elif 'video game' in combined or 'gaming' in combined and 'console' in combined:
        attributes = [
            ('title', 'STRING', 'Game title'),
            ('platform', 'STRING', 'Platform (PlayStation, Xbox, Nintendo, PC)'),
            ('genre', 'STRING', 'Genre'),
            ('rating', 'STRING', 'ESRB rating'),
            ('release_date', 'STRING', 'Release date'),
            ('edition', 'STRING', 'Edition'),
        ]
    elif 'charger' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (USB, Wireless, Car)'),
            ('output', 'STRING', 'Output power/voltage'),
            ('compatibility', 'STRING', 'Device compatibility'),
            ('cable_length', 'STRING', 'Cable length'),
        ]
    elif 'cable' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
            ('length', 'STRING', 'Length'),
            ('compatibility', 'STRING', 'Compatibility'),
        ]
    elif 'case' in combined and 'phone' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Phone model compatibility'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('protection_level', 'STRING', 'Protection level'),
        ]
    elif 'hanger' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('quantity', 'NUMBER', 'Quantity in pack'),
            ('type', 'STRING', 'Type (Plastic, Wood, Velvet)'),
        ]
    elif 'organizer' in combined or 'storage' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('dimensions', 'STRING', 'Dimensions'),
            ('number_of_compartments', 'NUMBER', 'Number of compartments'),
        ]
    elif 'lamp' in combined or 'light' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Desk, Floor, Table)'),
            ('bulb_type', 'STRING', 'Bulb type'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material'),
            ('dimmable', 'BOOLEAN', 'Dimmable'),
        ]
    elif 'rug' in combined or 'carpet' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('pattern', 'STRING', 'Pattern'),
            ('pile_height', 'STRING', 'Pile height'),
        ]
    elif 'curtain' in combined or 'drape' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('pattern', 'STRING', 'Pattern'),
            ('light_blocking', 'BOOLEAN', 'Light blocking'),
        ]
    elif 'frame' in combined and 'picture' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('orientation', 'STRING', 'Orientation (Portrait, Landscape)'),
        ]
    elif 'printer' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Inkjet, Laser, All-in-One)'),
            ('print_speed', 'STRING', 'Print speed (ppm)'),
            ('connectivity', 'STRING', 'Connectivity (USB, Wi-Fi, Ethernet)'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'scanner' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Flatbed, Sheet-fed)'),
            ('resolution', 'STRING', 'Resolution (DPI)'),
            ('connectivity', 'STRING', 'Connectivity'),
        ]
    elif 'router' in combined or 'modem' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('wifi_standard', 'STRING', 'Wi-Fi standard (Wi-Fi 6, Wi-Fi 5)'),
            ('speed', 'STRING', 'Speed (Mbps)'),
            ('number_of_antennas', 'NUMBER', 'Number of antennas'),
        ]
    elif 'mesh wi-fi' in combined or 'mesh network' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('wifi_standard', 'STRING', 'Wi-Fi standard'),
            ('coverage_area', 'STRING', 'Coverage area (sq ft)'),
            ('number_of_nodes', 'NUMBER', 'Number of nodes'),
            ('speed', 'STRING', 'Speed (Mbps)'),
        ]
    elif 'gps' in combined or 'navigation' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('screen_size', 'STRING', 'Screen size (inches)'),
            ('type', 'STRING', 'Type (Portable, Built-in)'),
            ('maps_included', 'BOOLEAN', 'Maps included'),
            ('lifetime_updates', 'BOOLEAN', 'Lifetime map updates'),
        ]
    elif 'sugar bowl' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material (Ceramic, Glass, Silver)'),
            ('capacity', 'STRING', 'Capacity'),
            ('color', 'STRING', 'Color'),
            ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
            ('quantity', 'NUMBER', 'Quantity in set'),
        ]
    elif 'embroidery kit' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('design', 'STRING', 'Design/Pattern'),
            ('difficulty_level', 'STRING', 'Difficulty level'),
            ('includes', 'STRING', 'What\'s included'),
            ('finished_size', 'STRING', 'Finished size'),
        ]
    elif 'teapot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material (Ceramic, Cast Iron, Glass)'),
            ('capacity', 'STRING', 'Capacity (cups)'),
            ('color', 'STRING', 'Color'),
            ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
        ]
    elif 'glassware' in combined or 'drinking glass' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
            ('microwave_safe', 'BOOLEAN', 'Microwave safe'),
            ('quantity', 'NUMBER', 'Quantity in set'),
        ]
    elif 'champagne flute' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material (Glass, Crystal)'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('height', 'STRING', 'Height'),
            ('quantity', 'NUMBER', 'Quantity in set'),
        ]
    elif 'cocktail glass' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('type', 'STRING', 'Type (Martini, Margarita, etc.)'),
            ('quantity', 'NUMBER', 'Quantity in set'),
        ]
    elif 'wine glass' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material (Glass, Crystal)'),
            ('type', 'STRING', 'Type (Red, White, Champagne)'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('quantity', 'NUMBER', 'Quantity in set'),
        ]
    elif 'beer glass' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('type', 'STRING', 'Type (Pint, Mug, Stein)'),
            ('quantity', 'NUMBER', 'Quantity in set'),
        ]
    elif 'shot glass' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('quantity', 'NUMBER', 'Quantity in set'),
        ]
    elif 'mug' in combined and 'travel' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material (Ceramic, Glass, Stainless Steel)'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
            ('microwave_safe', 'BOOLEAN', 'Microwave safe'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'travel mug' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('insulated', 'BOOLEAN', 'Insulated'),
            ('leak_proof', 'BOOLEAN', 'Leak-proof'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'thermos' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('material', 'STRING', 'Material'),
            ('insulation', 'STRING', 'Insulation type'),
            ('leak_proof', 'BOOLEAN', 'Leak-proof'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'water bottle' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('material', 'STRING', 'Material (Plastic, Stainless Steel, Glass)'),
            ('bpa_free', 'BOOLEAN', 'BPA-free'),
            ('insulated', 'BOOLEAN', 'Insulated'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'bottled water' in combined or name_lower == 'water':
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('type', 'STRING', 'Type (Spring, Purified, Mineral)'),
            ('ph_level', 'STRING', 'pH level'),
            ('minerals', 'STRING', 'Mineral content'),
        ]
    elif 'car seat cover' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('fit', 'STRING', 'Fit type'),
            ('washable', 'BOOLEAN', 'Washable'),
        ]
    elif 'car floor mat' in combined or 'floor mat' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('fit', 'STRING', 'Vehicle fit'),
            ('weather_resistant', 'BOOLEAN', 'Weather resistant'),
        ]
    elif 'car organizer' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('number_of_compartments', 'NUMBER', 'Number of compartments'),
        ]
    elif 'car charger' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('output', 'STRING', 'Output power'),
            ('number_of_ports', 'NUMBER', 'Number of ports'),
            ('fast_charging', 'BOOLEAN', 'Fast charging'),
            ('cable_length', 'STRING', 'Cable length'),
        ]
    elif 'phone charger' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (USB, Wireless)'),
            ('output', 'STRING', 'Output power'),
            ('cable_length', 'STRING', 'Cable length'),
            ('compatibility', 'STRING', 'Device compatibility'),
        ]
    elif 'wireless charger' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('output', 'STRING', 'Output power'),
            ('charging_speed', 'STRING', 'Charging speed'),
            ('compatibility', 'STRING', 'Device compatibility'),
        ]
    elif 'usb cable' in combined or 'usb-c cable' in combined or 'lightning cable' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Cable type'),
            ('length', 'STRING', 'Length'),
            ('data_transfer_speed', 'STRING', 'Data transfer speed'),
            ('charging_speed', 'STRING', 'Charging speed'),
        ]
    elif 'hdmi cable' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('version', 'STRING', 'HDMI version'),
            ('resolution_support', 'STRING', 'Resolution support'),
        ]
    elif 'ethernet cable' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('category', 'STRING', 'Category (Cat5e, Cat6, Cat7)'),
            ('speed', 'STRING', 'Speed (Mbps)'),
        ]
    elif 'displayport cable' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('version', 'STRING', 'DisplayPort version'),
            ('resolution_support', 'STRING', 'Resolution support'),
        ]
    elif 'usb flash drive' in combined or 'thumb drive' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Storage capacity'),
            ('type', 'STRING', 'USB type (USB 2.0, USB 3.0, USB-C)'),
            ('transfer_speed', 'STRING', 'Transfer speed'),
        ]
    elif 'memory card' in combined or 'sd card' in combined or 'microsd' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Storage capacity'),
            ('type', 'STRING', 'Type (SD, SDHC, SDXC, MicroSD)'),
            ('speed_class', 'STRING', 'Speed class'),
            ('read_speed', 'STRING', 'Read speed'),
            ('write_speed', 'STRING', 'Write speed'),
        ]
    elif 'camera flash' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('guide_number', 'STRING', 'Guide number'),
            ('compatibility', 'STRING', 'Camera compatibility'),
            ('ttl', 'BOOLEAN', 'TTL support'),
            ('battery_type', 'STRING', 'Battery type'),
        ]
    elif 'camera lens' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('focal_length', 'STRING', 'Focal length'),
            ('aperture', 'STRING', 'Maximum aperture'),
            ('lens_mount', 'STRING', 'Lens mount'),
            ('image_stabilization', 'BOOLEAN', 'Image stabilization'),
        ]
    elif 'camera bag' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Capacity'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('water_resistant', 'BOOLEAN', 'Water resistant'),
        ]
    elif 'tripod' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('max_height', 'STRING', 'Maximum height'),
            ('min_height', 'STRING', 'Minimum height'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
            ('folded_length', 'STRING', 'Folded length'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'camera filter' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Filter type'),
            ('size', 'STRING', 'Filter size (mm)'),
            ('compatibility', 'STRING', 'Lens compatibility'),
        ]
    elif 'sticky note' in combined or 'post-it' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('quantity', 'NUMBER', 'Quantity per pack'),
            ('pack_count', 'NUMBER', 'Number of packs'),
        ]
    elif 'legal pad' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('ruling', 'STRING', 'Ruling (Wide, College, Narrow)'),
            ('sheets_per_pad', 'NUMBER', 'Sheets per pad'),
            ('pack_count', 'NUMBER', 'Number of pads'),
        ]
    elif 'notebook' in combined and 'computer' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('ruling', 'STRING', 'Ruling (Lined, Blank, Grid)'),
            ('pages', 'NUMBER', 'Number of pages'),
            ('binding', 'STRING', 'Binding type'),
            ('cover', 'STRING', 'Cover type'),
        ]
    elif 'binder' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('ring_size', 'STRING', 'Ring size'),
            ('capacity', 'STRING', 'Sheet capacity'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'folder' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('type', 'STRING', 'Type (Manila, Hanging, Pocket)'),
            ('color', 'STRING', 'Color'),
            ('quantity', 'NUMBER', 'Quantity per pack'),
        ]
    elif 'pen' in combined and 'stylus' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Ballpoint, Gel, Rollerball)'),
            ('ink_color', 'STRING', 'Ink color'),
            ('tip_size', 'STRING', 'Tip size'),
            ('refillable', 'BOOLEAN', 'Refillable'),
            ('pack_count', 'NUMBER', 'Number of pens'),
        ]
    elif 'pencil' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Wood, Mechanical)'),
            ('lead_size', 'STRING', 'Lead size'),
            ('hardness', 'STRING', 'Hardness (HB, 2B, etc.)'),
            ('pack_count', 'NUMBER', 'Number of pencils'),
        ]
    elif 'marker' in combined or 'highlighter' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('ink_color', 'STRING', 'Ink color'),
            ('tip_size', 'STRING', 'Tip size'),
            ('pack_count', 'NUMBER', 'Number of markers'),
        ]
    elif 'scissors' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('type', 'STRING', 'Type (Office, Craft, Kitchen)'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'stapler' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Desktop, Mini)'),
            ('staple_capacity', 'STRING', 'Staple capacity'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'tape' in combined and 'dispenser' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Packing, Masking, Duct)'),
            ('width', 'STRING', 'Width'),
            ('length', 'STRING', 'Length'),
        ]
    elif 'tape dispenser' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'paper clip' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('quantity', 'NUMBER', 'Quantity per box'),
        ]
    elif 'push pin' in combined or 'thumbtack' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('color', 'STRING', 'Color'),
            ('quantity', 'NUMBER', 'Quantity per pack'),
        ]
    elif 'rubber band' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('quantity', 'NUMBER', 'Quantity per pack'),
        ]
    elif 'binder clip' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('quantity', 'NUMBER', 'Quantity per pack'),
        ]
    elif 'calculator' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Basic, Scientific, Graphing)'),
            ('display_type', 'STRING', 'Display type'),
            ('power_source', 'STRING', 'Power source'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'ruler' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('unit', 'STRING', 'Unit (Inches, Centimeters)'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'protractor' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'compass' in combined and 'drawing' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'eraser' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('color', 'STRING', 'Color'),
            ('pack_count', 'NUMBER', 'Number of erasers'),
        ]
    elif 'sharpener' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Manual, Electric)'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'hole punch' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Single, 2-hole, 3-hole)'),
            ('sheet_capacity', 'STRING', 'Sheet capacity'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'label' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('shape', 'STRING', 'Shape'),
            ('color', 'STRING', 'Color'),
            ('quantity', 'NUMBER', 'Quantity per pack'),
        ]
    elif 'envelope' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('type', 'STRING', 'Type'),
            ('color', 'STRING', 'Color'),
            ('quantity', 'NUMBER', 'Quantity per pack'),
        ]
    elif 'printer paper' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (Letter, Legal, A4)'),
            ('weight', 'STRING', 'Weight (lb)'),
            ('brightness', 'STRING', 'Brightness'),
            ('sheets_per_ream', 'NUMBER', 'Sheets per ream'),
            ('reams_per_pack', 'NUMBER', 'Reams per pack'),
        ]
    elif 'copy paper' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('weight', 'STRING', 'Weight (lb)'),
            ('brightness', 'STRING', 'Brightness'),
            ('sheets_per_ream', 'NUMBER', 'Sheets per ream'),
            ('reams_per_pack', 'NUMBER', 'Reams per pack'),
        ]
    elif 'cardstock' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('weight', 'STRING', 'Weight (lb)'),
            ('color', 'STRING', 'Color'),
            ('sheets_per_pack', 'NUMBER', 'Sheets per pack'),
        ]
    elif 'construction paper' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('sheets_per_pack', 'NUMBER', 'Sheets per pack'),
        ]
    elif 'art paper' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('weight', 'STRING', 'Weight'),
            ('texture', 'STRING', 'Texture'),
            ('sheets_per_pack', 'NUMBER', 'Sheets per pack'),
        ]
    elif 'drawing paper' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('weight', 'STRING', 'Weight'),
            ('texture', 'STRING', 'Texture'),
            ('sheets_per_pack', 'NUMBER', 'Sheets per pack'),
        ]
    elif 'watercolor paper' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('weight', 'STRING', 'Weight (lb)'),
            ('texture', 'STRING', 'Texture'),
            ('sheets_per_pack', 'NUMBER', 'Sheets per pack'),
        ]
    elif 'canvas' in combined and 'art' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('type', 'STRING', 'Type (Stretched, Roll)'),
            ('thickness', 'STRING', 'Thickness'),
        ]
    elif 'paint' in combined and 'supply' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Acrylic, Oil, Watercolor)'),
            ('color', 'STRING', 'Color'),
            ('size', 'STRING', 'Size'),
            ('finish', 'STRING', 'Finish (Matte, Gloss)'),
        ]
    elif 'paint brush' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Brush type'),
            ('size', 'STRING', 'Size'),
            ('bristle_material', 'STRING', 'Bristle material'),
        ]
    elif 'colored pencil' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('count', 'NUMBER', 'Number of colors'),
            ('type', 'STRING', 'Type (Wax, Oil)'),
            ('lightfast', 'BOOLEAN', 'Lightfast'),
        ]
    elif 'crayon' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('count', 'NUMBER', 'Number of colors'),
            ('size', 'STRING', 'Size'),
        ]
    elif 'marker' in combined and 'art' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Permanent, Water-based)'),
            ('count', 'NUMBER', 'Number of colors'),
            ('tip_size', 'STRING', 'Tip size'),
        ]
    elif 'pastel' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Soft, Oil)'),
            ('count', 'NUMBER', 'Number of colors'),
        ]
    elif 'charcoal' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Compressed, Vine)'),
            ('count', 'NUMBER', 'Number of sticks'),
        ]
    elif 'sketch pad' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('pages', 'NUMBER', 'Number of pages'),
            ('paper_weight', 'STRING', 'Paper weight'),
        ]
    elif 'easel' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Tabletop, Floor)'),
            ('height', 'STRING', 'Height'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'palette' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('number_of_wells', 'NUMBER', 'Number of wells'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'smock' in combined or 'apron' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'glue' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (School, Craft, Super)'),
            ('size', 'STRING', 'Size'),
            ('drying_time', 'STRING', 'Drying time'),
        ]
    elif 'glue stick' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('count', 'NUMBER', 'Number of sticks'),
        ]
    elif 'mod podge' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('finish', 'STRING', 'Finish (Matte, Gloss)'),
            ('size', 'STRING', 'Size'),
        ]
    elif 'tape' in combined and 'double' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('width', 'STRING', 'Width'),
            ('length', 'STRING', 'Length'),
        ]
    elif 'washi tape' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('width', 'STRING', 'Width'),
            ('length', 'STRING', 'Length'),
            ('design', 'STRING', 'Design'),
        ]
    elif 'foam' in combined and 'sheet' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('thickness', 'STRING', 'Thickness'),
            ('color', 'STRING', 'Color'),
            ('size', 'STRING', 'Size'),
        ]
    elif 'felt' in combined and 'sheet' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('color', 'STRING', 'Color'),
            ('size', 'STRING', 'Size'),
            ('thickness', 'STRING', 'Thickness'),
        ]
    elif 'pipe cleaner' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('color', 'STRING', 'Color'),
            ('count', 'NUMBER', 'Number of cleaners'),
        ]
    elif 'pom pom' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('count', 'NUMBER', 'Number of pom poms'),
        ]
    elif 'googly eye' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('count', 'NUMBER', 'Number of eyes'),
        ]
    elif 'sequin' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('count', 'NUMBER', 'Number of sequins'),
        ]
    elif 'bead' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('count', 'NUMBER', 'Number of beads'),
        ]
    elif 'yarn' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight', 'STRING', 'Yarn weight'),
            ('fiber_content', 'STRING', 'Fiber content'),
            ('color', 'STRING', 'Color'),
            ('yardage', 'STRING', 'Yardage'),
        ]
    elif 'crochet hook' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Hook size'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'knitting needle' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Needle size'),
            ('length', 'STRING', 'Length'),
            ('material', 'STRING', 'Material'),
            ('type', 'STRING', 'Type (Straight, Circular, Double-pointed)'),
        ]
    elif 'sewing machine' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Mechanical, Electronic, Computerized)'),
            ('stitches', 'NUMBER', 'Number of stitches'),
            ('buttonhole_styles', 'NUMBER', 'Number of buttonhole styles'),
        ]
    elif 'fabric' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('width', 'STRING', 'Width'),
            ('color', 'STRING', 'Color'),
            ('pattern', 'STRING', 'Pattern'),
        ]
    elif 'thread' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('color', 'STRING', 'Color'),
            ('weight', 'STRING', 'Thread weight'),
            ('material', 'STRING', 'Material'),
            ('length', 'STRING', 'Length'),
        ]
    elif 'button' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('color', 'STRING', 'Color'),
            ('material', 'STRING', 'Material'),
            ('count', 'NUMBER', 'Number of buttons'),
        ]
    elif 'zipper' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('color', 'STRING', 'Color'),
            ('type', 'STRING', 'Type'),
        ]
    elif 'elastic' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('width', 'STRING', 'Width'),
            ('length', 'STRING', 'Length'),
        ]
    elif 'bias tape' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('width', 'STRING', 'Width'),
            ('length', 'STRING', 'Length'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'interfacing' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Fusible, Sew-in)'),
            ('weight', 'STRING', 'Weight'),
            ('width', 'STRING', 'Width'),
        ]
    elif 'pattern' in combined and 'sewing' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('design', 'STRING', 'Design/Pattern name'),
            ('size_range', 'STRING', 'Size range'),
            ('difficulty', 'STRING', 'Difficulty level'),
        ]
    elif 'pin' in combined and 'safety' not in combined and 'push' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Straight, Quilting)'),
            ('length', 'STRING', 'Length'),
            ('count', 'NUMBER', 'Number of pins'),
        ]
    elif 'safety pin' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('count', 'NUMBER', 'Number of pins'),
        ]
    elif 'needle' in combined and 'knitting' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('count', 'NUMBER', 'Number of needles'),
        ]
    elif 'thimble' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'seam ripper' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'measuring tape' in combined and 'sewing' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('unit', 'STRING', 'Unit'),
        ]
    elif 'rotary cutter' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('blade_size', 'STRING', 'Blade size'),
            ('safety_lock', 'BOOLEAN', 'Safety lock'),
        ]
    elif 'cutting mat' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('thickness', 'STRING', 'Thickness'),
        ]
    elif 'iron' in combined and 'steam' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('power', 'STRING', 'Power (watts)'),
            ('water_capacity', 'STRING', 'Water capacity'),
            ('steam_settings', 'STRING', 'Steam settings'),
        ]
    elif 'ironing board' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('height', 'STRING', 'Height'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'steamer' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('water_capacity', 'STRING', 'Water capacity'),
            ('heat_up_time', 'STRING', 'Heat-up time'),
        ]
    elif 'garment steamer' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('water_capacity', 'STRING', 'Water capacity'),
            ('heat_up_time', 'STRING', 'Heat-up time'),
            ('steam_time', 'STRING', 'Steam time'),
        ]
    elif 'sewing box' in combined or 'sewing kit' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('includes', 'STRING', 'What\'s included'),
        ]
    elif 'pincushion' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'bobbin' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
            ('count', 'NUMBER', 'Number of bobbins'),
        ]
    elif 'presser foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Foot type'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'needle plate' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'feed dog' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'tension' in combined and 'disc' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'spool pin' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'thread stand' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'extension table' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'knee lift' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'free arm' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'drop feed' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'walking foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'zipper foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'buttonhole foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'blind hem foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'overlock foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'ruffler foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'gathering foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'rolled hem foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'edge stitch foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'quilting foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'darning foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'free motion foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'embroidery foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'monogramming foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'button foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'snap foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'piping foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'cording foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'beading foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'sequin foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'fringe foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'tuck foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'pleating foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'scallop foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'hemmer foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'bias binder foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'felling foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'welt foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'cording foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'piping foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'bias tape foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'elastic foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'gathering foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'ruffler foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'tuck foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'pleating foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'scallop foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'hemmer foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'bias binder foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'felling foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'welt foot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('compatibility', 'STRING', 'Machine compatibility'),
        ]
    elif 'air purifier' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('room_size', 'STRING', 'Room size coverage'),
            ('filter_type', 'STRING', 'Filter type'),
            ('noise_level', 'STRING', 'Noise level (dB)'),
            ('energy_rating', 'STRING', 'Energy rating'),
        ]
    elif 'vacuum' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Upright, Canister, Stick, Robot)'),
            ('power', 'STRING', 'Power (watts)'),
            ('bagless', 'BOOLEAN', 'Bagless'),
            ('cordless', 'BOOLEAN', 'Cordless'),
        ]
    elif 'treadmill' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('max_speed', 'STRING', 'Maximum speed (mph)'),
            ('incline', 'STRING', 'Incline range'),
            ('display', 'STRING', 'Display type'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
        ]
    elif 'bike' in combined and 'electric' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model'),
            ('frame_size', 'STRING', 'Frame size'),
            ('battery_range', 'STRING', 'Battery range (miles)'),
            ('max_speed', 'STRING', 'Maximum speed (mph)'),
            ('weight', 'STRING', 'Weight'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'car seat' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('age_range', 'STRING', 'Age range'),
            ('weight_range', 'STRING', 'Weight range'),
            ('installation_type', 'STRING', 'Installation type'),
            ('safety_rating', 'STRING', 'Safety rating'),
        ]
    elif 'stroller' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Full-size, Lightweight, Jogging)'),
            ('weight', 'STRING', 'Weight'),
            ('folded_dimensions', 'STRING', 'Folded dimensions'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'crib' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('mattress_size', 'STRING', 'Mattress size'),
            ('color', 'STRING', 'Color'),
            ('convertible', 'BOOLEAN', 'Convertible'),
            ('safety_certification', 'STRING', 'Safety certification'),
        ]
    elif 'diaper' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('count', 'NUMBER', 'Count per pack'),
            ('type', 'STRING', 'Type (Disposable, Cloth)'),
        ]
    elif 'pacifier' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('age_range', 'STRING', 'Age range'),
            ('material', 'STRING', 'Material'),
            ('orthodontic', 'BOOLEAN', 'Orthodontic'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'formula' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Powder, Liquid, Ready-to-feed)'),
            ('size', 'STRING', 'Size'),
            ('age_range', 'STRING', 'Age range'),
            ('ingredients', 'STRING', 'Key ingredients'),
        ]
    elif 'baby food' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('flavor', 'STRING', 'Flavor'),
            ('age_range', 'STRING', 'Age range'),
            ('size', 'STRING', 'Size'),
            ('organic', 'BOOLEAN', 'Organic'),
        ]
    elif 'car tire' in combined or 'tire' in combined and 'wheel' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Tire size'),
            ('type', 'STRING', 'Type (All-season, Winter, Summer)'),
            ('speed_rating', 'STRING', 'Speed rating'),
            ('load_index', 'STRING', 'Load index'),
        ]
    elif 'car battery' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('voltage', 'STRING', 'Voltage'),
            ('capacity', 'STRING', 'Capacity (CCA)'),
            ('type', 'STRING', 'Type'),
            ('warranty', 'STRING', 'Warranty period'),
        ]
    elif 'motor oil' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('viscosity', 'STRING', 'Viscosity (e.g., 5W-30)'),
            ('type', 'STRING', 'Type (Conventional, Synthetic, Blend)'),
            ('size', 'STRING', 'Size (quarts)'),
        ]
    elif 'dog food' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Bag size (lbs)'),
            ('life_stage', 'STRING', 'Life stage (Puppy, Adult, Senior)'),
            ('breed_size', 'STRING', 'Breed size'),
            ('ingredients', 'STRING', 'Key ingredients'),
        ]
    elif 'cat food' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Bag size (lbs)'),
            ('life_stage', 'STRING', 'Life stage (Kitten, Adult, Senior)'),
            ('type', 'STRING', 'Type (Dry, Wet)'),
            ('ingredients', 'STRING', 'Key ingredients'),
        ]
    elif 'cat litter' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Bag size (lbs)'),
            ('type', 'STRING', 'Type (Clumping, Non-clumping, Crystal)'),
            ('scented', 'BOOLEAN', 'Scented'),
        ]
    elif 'dog collar' in combined or 'leash' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('width', 'STRING', 'Width'),
        ]
    elif 'dog bed' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('washable', 'BOOLEAN', 'Washable'),
        ]
    elif 'fish food' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Flakes, Pellets, Freeze-dried)'),
            ('size', 'STRING', 'Size'),
            ('fish_type', 'STRING', 'Fish type'),
        ]
    elif 'aquarium' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (gallons)'),
            ('material', 'STRING', 'Material (Glass, Acrylic)'),
            ('dimensions', 'STRING', 'Dimensions'),
            ('shape', 'STRING', 'Shape'),
        ]
    elif 'bird cage' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('bar_spacing', 'STRING', 'Bar spacing'),
            ('includes_accessories', 'BOOLEAN', 'Includes accessories'),
        ]
    elif 'bird food' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('bird_type', 'STRING', 'Bird type'),
        ]
    elif 'hamster cage' in combined or 'small animal cage' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('includes_accessories', 'BOOLEAN', 'Includes accessories'),
        ]
    elif 'small animal food' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('animal_type', 'STRING', 'Animal type'),
        ]
    elif 'plant' in combined and 'pot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('drainage_holes', 'BOOLEAN', 'Drainage holes'),
        ]
    elif 'seed' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('plant_type', 'STRING', 'Plant type'),
            ('quantity', 'NUMBER', 'Seed count'),
            ('organic', 'BOOLEAN', 'Organic'),
        ]
    elif 'fertilizer' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Liquid, Granular)'),
            ('npk_ratio', 'STRING', 'NPK ratio'),
            ('size', 'STRING', 'Size'),
        ]
    elif 'garden tool' in combined or 'gardening tool' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Tool type'),
            ('material', 'STRING', 'Material'),
            ('handle_length', 'STRING', 'Handle length'),
        ]
    elif 'hose' in combined and 'garden' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length (feet)'),
            ('diameter', 'STRING', 'Diameter'),
            ('material', 'STRING', 'Material'),
            ('kink_resistant', 'BOOLEAN', 'Kink resistant'),
        ]
    elif 'lawn mower' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Push, Self-propelled, Riding)'),
            ('cutting_width', 'STRING', 'Cutting width'),
            ('power_source', 'STRING', 'Power source (Gas, Electric, Battery)'),
        ]
    elif 'grill' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Gas, Charcoal, Electric)'),
            ('cooking_area', 'STRING', 'Cooking area (sq in)'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'cooler' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Capacity (quarts)'),
            ('type', 'STRING', 'Type (Hard, Soft)'),
            ('number_of_wheels', 'NUMBER', 'Number of wheels'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'tent' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Capacity (person)'),
            ('type', 'STRING', 'Type (Dome, Cabin, Backpacking)'),
            ('weight', 'STRING', 'Weight'),
            ('seasons', 'STRING', 'Seasons (3-season, 4-season)'),
        ]
    elif 'sleeping bag' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('temperature_rating', 'STRING', 'Temperature rating'),
            ('type', 'STRING', 'Type (Mummy, Rectangular)'),
            ('weight', 'STRING', 'Weight'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'backpack' in combined and 'hiking' in combined or 'backpacking' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Capacity (liters)'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
            ('weight', 'STRING', 'Weight'),
            ('water_resistant', 'BOOLEAN', 'Water resistant'),
        ]
    elif 'hiking boot' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (US)'),
            ('width', 'STRING', 'Width'),
            ('material', 'STRING', 'Material'),
            ('waterproof', 'BOOLEAN', 'Waterproof'),
            ('ankle_height', 'STRING', 'Ankle height'),
        ]
    elif 'fishing rod' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('action', 'STRING', 'Action (Light, Medium, Heavy)'),
            ('power', 'STRING', 'Power rating'),
            ('pieces', 'STRING', 'Number of pieces'),
        ]
    elif 'fishing tackle' in combined or 'lure' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('color', 'STRING', 'Color'),
            ('weight', 'STRING', 'Weight'),
        ]
    elif 'kayak' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Sit-on-top, Sit-in)'),
            ('length', 'STRING', 'Length'),
            ('capacity', 'STRING', 'Capacity (lbs)'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'paddle' in combined and 'kayak' in combined or 'canoe' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('material', 'STRING', 'Material'),
            ('blade_shape', 'STRING', 'Blade shape'),
        ]
    elif 'ski' in combined or 'snowboard' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('type', 'STRING', 'Type'),
            ('ability_level', 'STRING', 'Ability level'),
            ('width', 'STRING', 'Width'),
        ]
    elif 'ice skate' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('type', 'STRING', 'Type (Figure, Hockey, Recreational)'),
            ('blade_material', 'STRING', 'Blade material'),
        ]
    elif 'surfboard' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('width', 'STRING', 'Width'),
            ('thickness', 'STRING', 'Thickness'),
            ('volume', 'STRING', 'Volume (liters)'),
            ('fin_setup', 'STRING', 'Fin setup'),
        ]
    elif 'wetsuit' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('thickness', 'STRING', 'Thickness (mm)'),
            ('type', 'STRING', 'Type (Full, Spring, Shorty)'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'golf club' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Club type'),
            ('hand', 'STRING', 'Hand (Right, Left)'),
            ('shaft_material', 'STRING', 'Shaft material'),
            ('flex', 'STRING', 'Flex'),
        ]
    elif 'tennis racket' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('head_size', 'STRING', 'Head size (sq in)'),
            ('weight', 'STRING', 'Weight'),
            ('grip_size', 'STRING', 'Grip size'),
            ('string_pattern', 'STRING', 'String pattern'),
        ]
    elif 'basketball' in combined and 'hoop' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Ball size'),
            ('material', 'STRING', 'Material'),
            ('indoor_outdoor', 'STRING', 'Indoor/Outdoor'),
        ]
    elif 'basketball hoop' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('height', 'STRING', 'Height'),
            ('backboard_size', 'STRING', 'Backboard size'),
            ('adjustable', 'BOOLEAN', 'Adjustable height'),
        ]
    elif 'soccer ball' in combined or 'football' in combined and 'american' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Ball size'),
            ('material', 'STRING', 'Material'),
            ('indoor_outdoor', 'STRING', 'Indoor/Outdoor'),
        ]
    elif 'baseball' in combined and 'glove' not in combined and 'bat' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Ball size'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'baseball bat' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('weight', 'STRING', 'Weight'),
            ('material', 'STRING', 'Material (Wood, Aluminum, Composite)'),
            ('diameter', 'STRING', 'Barrel diameter'),
        ]
    elif 'baseball glove' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('position', 'STRING', 'Position'),
            ('hand', 'STRING', 'Hand (Right, Left)'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'volleyball' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Ball size'),
            ('material', 'STRING', 'Material'),
            ('indoor_outdoor', 'STRING', 'Indoor/Outdoor'),
        ]
    elif 'yoga mat' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('thickness', 'STRING', 'Thickness (mm)'),
            ('material', 'STRING', 'Material'),
            ('length', 'STRING', 'Length'),
            ('width', 'STRING', 'Width'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'dumbbell' in combined or 'weight' in combined and 'dumbbell' not in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight', 'STRING', 'Weight (lbs)'),
            ('material', 'STRING', 'Material'),
            ('type', 'STRING', 'Type (Fixed, Adjustable)'),
        ]
    elif 'resistance band' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('resistance_level', 'STRING', 'Resistance level'),
            ('length', 'STRING', 'Length'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'foam roller' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('diameter', 'STRING', 'Diameter'),
            ('density', 'STRING', 'Density'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'protein powder' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('flavor', 'STRING', 'Flavor'),
            ('size', 'STRING', 'Size (lbs)'),
            ('protein_per_serving', 'STRING', 'Protein per serving (g)'),
            ('type', 'STRING', 'Type (Whey, Casein, Plant-based)'),
        ]
    elif 'shaker bottle' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('capacity', 'STRING', 'Capacity (oz)'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'yoga block' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('material', 'STRING', 'Material'),
            ('density', 'STRING', 'Density'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'jump rope' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('material', 'STRING', 'Material'),
            ('weight', 'STRING', 'Weight'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'kettlebell' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight', 'STRING', 'Weight (lbs)'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'pull up bar' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Doorway, Wall-mounted)'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'medicine ball' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight', 'STRING', 'Weight (lbs)'),
            ('diameter', 'STRING', 'Diameter'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'exercise bike' in combined or 'stationary bike' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Upright, Recumbent)'),
            ('resistance_type', 'STRING', 'Resistance type'),
            ('display', 'STRING', 'Display type'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
        ]
    elif 'elliptical' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('stride_length', 'STRING', 'Stride length'),
            ('resistance_levels', 'NUMBER', 'Resistance levels'),
            ('display', 'STRING', 'Display type'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
        ]
    elif 'rowing machine' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('model', 'STRING', 'Model name'),
            ('type', 'STRING', 'Type (Water, Air, Magnetic)'),
            ('resistance_levels', 'NUMBER', 'Resistance levels'),
            ('display', 'STRING', 'Display type'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
        ]
    elif 'bench' in combined and 'weight' in combined or 'exercise bench' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type (Flat, Incline, Adjustable)'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'barbell' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight', 'STRING', 'Weight (lbs)'),
            ('length', 'STRING', 'Length'),
            ('diameter', 'STRING', 'Diameter'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'weight plate' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight', 'STRING', 'Weight (lbs)'),
            ('diameter', 'STRING', 'Diameter'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'power rack' in combined or 'squat rack' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('height', 'STRING', 'Height'),
            ('width', 'STRING', 'Width'),
            ('depth', 'STRING', 'Depth'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
        ]
    elif 'smith machine' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
            ('included_weight', 'STRING', 'Included weight (lbs)'),
        ]
    elif 'cable machine' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight_stack', 'STRING', 'Weight stack (lbs)'),
            ('number_of_stations', 'NUMBER', 'Number of stations'),
        ]
    elif 'leg press' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
            ('angle', 'STRING', 'Angle'),
        ]
    elif 'lat pulldown' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight_stack', 'STRING', 'Weight stack (lbs)'),
        ]
    elif 'chest press' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight_stack', 'STRING', 'Weight stack (lbs)'),
        ]
    elif 'shoulder press' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight_stack', 'STRING', 'Weight stack (lbs)'),
        ]
    elif 'leg curl' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight_stack', 'STRING', 'Weight stack (lbs)'),
        ]
    elif 'leg extension' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight_stack', 'STRING', 'Weight stack (lbs)'),
        ]
    elif 'ab machine' in combined or 'abdominal' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
        ]
    elif 'punching bag' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight', 'STRING', 'Weight (lbs)'),
            ('type', 'STRING', 'Type (Heavy bag, Speed bag)'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'punching bag stand' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
            ('height', 'STRING', 'Height'),
        ]
    elif 'speed bag' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'boxing glove' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (oz)'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'hand wrap' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'mouthguard' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('type', 'STRING', 'Type (Boil-and-bite, Custom)'),
        ]
    elif 'headgear' in combined and 'boxing' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'martial arts' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'wrestling' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'mma' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'karate' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'taekwondo' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'judo' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'jiu jitsu' in combined or 'bjj' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'muay thai' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'kickboxing' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'boxing' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'punching' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'strike' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('type', 'STRING', 'Type'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'focus mitt' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'paddle' in combined and 'tennis' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'target' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'shield' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'dummy' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'bag' in combined and 'punching' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('weight', 'STRING', 'Weight (lbs)'),
            ('type', 'STRING', 'Type (Heavy bag, Speed bag)'),
            ('material', 'STRING', 'Material'),
        ]
    elif 'glove' in combined and 'boxing' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size (oz)'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'wrap' in combined and 'hand' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('length', 'STRING', 'Length'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    elif 'guard' in combined and 'mouth' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('type', 'STRING', 'Type (Boil-and-bite, Custom)'),
        ]
    elif 'gear' in combined and 'head' in combined:
        attributes = [
            ('brand', 'STRING', 'Brand'),
            ('size', 'STRING', 'Size'),
            ('material', 'STRING', 'Material'),
            ('color', 'STRING', 'Color'),
        ]
    
    # === DEFAULT FALLBACK ===
    # If no specific match, analyze the category name/description to generate sensible defaults
    else:
        # Try to infer attributes from common patterns
        if any(word in combined for word in ['size', 'sized', 'sizing']):
            attributes.append(('size', 'STRING', 'Size'))
        if any(word in combined for word in ['color', 'colored', 'colour']):
            attributes.append(('color', 'STRING', 'Color'))
        if any(word in combined for word in ['material', 'fabric', 'fiber']):
            attributes.append(('material', 'STRING', 'Material'))
        if any(word in combined for word in ['brand', 'manufacturer']):
            attributes.append(('brand', 'STRING', 'Brand'))
        if any(word in combined for word in ['model', 'version']):
            attributes.append(('model', 'STRING', 'Model'))
        if any(word in combined for word in ['weight', 'heavy', 'light']):
            attributes.append(('weight', 'STRING', 'Weight'))
        if any(word in combined for word in ['dimension', 'measurement', 'length', 'width', 'height']):
            attributes.append(('dimensions', 'STRING', 'Dimensions'))
        
        # If we still don't have attributes, use a minimal default set
        if not attributes:
            attributes = [
                ('brand', 'STRING', 'Brand'),
                ('model', 'STRING', 'Model'),
                ('color', 'STRING', 'Color'),
                ('size', 'STRING', 'Size'),
            ]
    
    return attributes

def main():
    """Main function to generate category attributes"""
    categories = []
    
    # Read categories from CSV
    with open('categories.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            categories.append({
                'id': int(row['id']),
                'name': row['name'],
                'description': row['description'] or ''
            })
    
    # Generate attributes for each category
    category_attributes = []
    for cat in categories:
        attrs = generate_attributes_for_category(cat['id'], cat['name'], cat['description'])
        category_attributes.append({
            'id': cat['id'],
            'name': cat['name'],
            'attributes': attrs
        })
    
    # Write to Python file
    with open('categories_attributes.py', 'w', encoding='utf-8') as f:
        f.write('"""\n')
        f.write('Category attributes mapping\n')
        f.write('Generated automatically from categories.csv\n')
        f.write('Each category has been analyzed individually to generate specific, relevant attributes.\n')
        f.write('"""\n\n')
        f.write('CATEGORY_ATTRIBUTES = [\n')
        
        for cat_attr in category_attributes:
            f.write(f"  {{\n")
            f.write(f"    # {cat_attr['name']}\n")
            f.write(f"    'id': {cat_attr['id']},\n")
            f.write(f"    'attributes': [\n")
            for attr in cat_attr['attributes']:
                # Escape single quotes in display names
                display_name = attr[2].replace("'", "\\'")
                f.write(f"      ('{attr[0]}', '{attr[1]}', '{display_name}'),\n")
            f.write(f"    ]\n")
            f.write(f"  }},\n")
        
        f.write(']\n')
    
    print(f"Generated attributes for {len(category_attributes)} categories")
    print("Saved to categories_attributes.py")
    
    # Print some statistics
    total_attrs = sum(len(cat['attributes']) for cat in category_attributes)
    avg_attrs = total_attrs / len(category_attributes) if category_attributes else 0
    print(f"Total attributes: {total_attrs}")
    print(f"Average attributes per category: {avg_attrs:.1f}")

if __name__ == '__main__':
    main()
