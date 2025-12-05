#!/usr/bin/env python3
"""
Scrape 20 products from Flipkart Phones category and save to JSON
"""

import json
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, quote_plus


def extract_flipkart_products(category: str = "Phones", max_products: int = 20) -> List[Dict[str, Any]]:
    """
    Scrape Flipkart products with enhanced attribute extraction
    """
    products = []
    
    # Setup session with realistic headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    try:
        # Flipkart search URL for phones
        search_url = f"https://www.flipkart.com/search?q={quote_plus(category + ' mobile')}"
        
        print(f"Fetching: {search_url}")
        time.sleep(random.uniform(1, 3))  # Be respectful
        
        response = session.get(search_url, timeout=15)
        
        if response.status_code != 200:
            print(f"Error: Got status code {response.status_code}")
            return products
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Debug: check page title
        title_tag = soup.find('title')
        if title_tag:
            page_title = title_tag.get_text(strip=True)
            print(f"Page title: {page_title[:100]}")
          
        # Find product containers - Flipkart uses various class names
        product_containers = []
        
        # Try different selectors for Flipkart product cards
        selectors = [
            'div[data-id]',
            'div._1AtVbE',
            'div._2kHMtA',
            'div._1YokD2',
            'a._1fQZEK',
        ]
        
        for selector in selectors:
            containers = soup.select(selector)
            if containers and len(containers) > 5:  # Ensure we found actual products
                product_containers = containers
                print(f"Found {len(product_containers)} product containers using {selector}")
                break
        
        # Alternative: find by product links
        if not product_containers:
            product_links = soup.find_all('a', href=re.compile(r'/p/'))
            seen_links = set()
            for link in product_links:
                href = link.get('href', '')
                if href and href not in seen_links:
                    parent = link.find_parent(['div', 'li'])
                    if parent:
                        product_containers.append(parent)
                        seen_links.add(href)
                        if len(product_containers) >= max_products:
                            break
        
        print(f"Total found: {len(product_containers)} product containers")
        
        # Extract product information
        for container in product_containers[:max_products]:
            try:
                product = {}
                
                # Extract product name/title - Flipkart structure
                title_elem = container.find('a', class_=lambda x: x and ('IRpwTa' in str(x) or 's1Q9rs' in str(x) or '_4rR01T' in str(x)))
                if not title_elem:
                    title_elem = container.find('div', class_=lambda x: x and ('_4rR01T' in str(x)))
                if not title_elem:
                    title_elem = container.find('a', href=re.compile(r'/p/'))
                
                if title_elem:
                    # Get text and clean it up
                    title = title_elem.get_text(strip=True)
                    if not title:
                        title = title_elem.get('title', '').strip()
                    
                    # Clean up title - remove "Add to Compare" and extract just the product name
                    # Pattern: "Brand Model (Color, Storage GB)" usually comes before ratings
                    title = re.sub(r'^Add to Compare', '', title, flags=re.IGNORECASE).strip()
                    
                    # Try to extract clean product name - look for pattern ending before ratings
                    # Pattern: Product name usually ends with ") GB" or ")GB" followed by rating number
                    # Match: "Brand Model (Color, Storage GB)" - capture everything up to closing paren and GB
                    clean_title_match = re.search(r'^([^0-9]+?\([^,)]+,\s*\d+\s*GB\))', title)
                    if clean_title_match:
                        title = clean_title_match.group(1).strip()
                    else:
                        # Alternative: look for pattern ending with ") GB" or ")GB" followed by number
                        clean_title_match = re.search(r'^([^)]+\))\s*(?=\d+\.?\d)', title)
                        if clean_title_match:
                            title = clean_title_match.group(1).strip()
                        else:
                            # Last resort: extract up to first occurrence of rating pattern (number.number)
                            # But preserve the product name part
                            title = re.sub(r'\)\s*(\d+\.\d).*$', ')', title).strip()
                            # Remove if there's text after the closing paren that starts with a number
                            title = re.sub(r'\)\s*\d+.*$', ')', title).strip()
                    
                    # Remove common suffixes that might be in the title (but preserve product name)
                    # Only remove if they appear after the product name pattern
                    title = re.sub(r'\s*(Ratings?|Reviews?|Off|Exchange|Bank Offer|RAM|ROM|Display|Camera|Battery|Processor|Warranty|Expandable|Upto|Max|clock|speed|GHz|A75|A55|mAh|MP|HD\+|Quad|Unisoc|Tensor).*$', '', title, flags=re.IGNORECASE).strip()
                    
                    # Final cleanup: remove any trailing numbers, commas, or special characters that aren't part of product name
                    # But be careful not to remove numbers that are part of model names
                    title = re.sub(r'\s*[0-9,]+\s*(?:Ratings?|Reviews?).*$', '', title).strip()
                    title = re.sub(r'\s*&.*$', '', title).strip()
                    
                    if title and len(title) > 5:
                        product['name'] = title
                    else:
                        continue
                else:
                    continue
                
                # Extract product URL
                link_elem = container.find('a', href=re.compile(r'/p/'))
                if link_elem:
                    href = link_elem.get('href', '')
                    if href.startswith('/'):
                        product['url'] = 'https://www.flipkart.com' + href
                    else:
                        product['url'] = href
                    
                    # Extract product ID from URL
                    product_id_match = re.search(r'/p/([a-zA-Z0-9]+)', href)
                    if product_id_match:
                        product['product_id'] = product_id_match.group(1)
                
                # Extract price - Flipkart uses ₹ symbol
                price_elem = container.find('div', class_=lambda x: x and ('price' in str(x).lower() or '_30jeq3' in str(x) or '_1_WHN1' in str(x)))
                if not price_elem:
                    price_elem = container.find('div', string=re.compile(r'₹'))
                
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Extract price value
                    price_match = re.search(r'₹\s*([\d,]+)', price_text)
                    if price_match:
                        price_val = float(price_match.group(1).replace(',', ''))
                        if 5000 < price_val < 200000:  # Reasonable phone price range in INR
                            product['price'] = price_text
                
                # Extract rating - try multiple methods
                rating_elem = container.find('div', class_=lambda x: x and ('rating' in str(x).lower() or '_3LWZlK' in str(x)))
                if rating_elem:
                    rating_text = rating_elem.get_text(strip=True)
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        product['rating'] = rating_match.group(1)
                
                # If not found, try finding rating in container text
                if 'rating' not in product:
                    container_text = container.get_text()
                    # Look for pattern: "4.6" or "3.8" followed by "Ratings" or "Stars"
                    rating_match = re.search(r'(\d+\.\d+)\s*(?:Ratings?|Stars?)', container_text, re.IGNORECASE)
                    if rating_match:
                        product['rating'] = rating_match.group(1)
                    else:
                        # Alternative: look for number.number pattern near the beginning
                        rating_match = re.search(r'\)\s*(\d+\.\d+)', container_text)
                        if rating_match:
                            product['rating'] = rating_match.group(1)
                
                # Extract number of reviews/ratings - try multiple methods
                reviews_elem = container.find('span', class_=lambda x: x and ('review' in str(x).lower() or '_2_R_DZ' in str(x)))
                if not reviews_elem:
                    # Try finding reviews in text content
                    container_text = container.get_text()
                    reviews_match = re.search(r'(\d+(?:,\d+)*)\s*(?:Ratings?|Reviews?)', container_text, re.IGNORECASE)
                    if reviews_match:
                        product['review_count'] = reviews_match.group(1).replace(',', '')
                else:
                    reviews_text = reviews_elem.get_text(strip=True)
                    reviews_match = re.search(r'([\d,]+)', reviews_text.replace(',', ''))
                    if reviews_match:
                        product['review_count'] = reviews_match.group(1)
                
                # Extract discount/offer
                discount_elem = container.find('div', class_=lambda x: x and ('discount' in str(x).lower() or '_3Ay6Sb' in str(x)))
                if discount_elem:
                    discount_text = discount_elem.get_text(strip=True)
                    if discount_text:
                        product['discount'] = discount_text
                
                # Extract attributes from product name (for phones)
                # Use original title text for attribute extraction (before cleaning)
                original_title = title_elem.get_text(strip=True) if title_elem else product['name']
                attributes = {}
                title_lower = product['name'].lower()
                original_title_lower = original_title.lower()
                
                # Brand extraction
                phone_brands = ['Apple', 'Samsung', 'Google', 'OnePlus', 'Xiaomi', 'Motorola', 
                              'Nokia', 'Sony', 'LG', 'Huawei', 'Oppo', 'Vivo', 'Realme', 
                              'Nothing', 'ASUS', 'TCL', 'ZTE', 'Alcatel', 'Redmi', 'POCO',
                              'Infinix', 'Tecno', 'Micromax', 'Lava', 'iQOO']
                for brand in phone_brands:
                    if brand.lower() in title_lower:
                        attributes['brand'] = brand
                        break
                
                # Storage capacity - extract from original title or cleaned name
                storage_patterns = [
                    r'(\d+)\s*GB\s*(?:Storage|ROM|Memory)',
                    r'(\d+)\s*GB\s*(?!RAM)',
                    r'(\d+)\s*TB',
                ]
                for pattern in storage_patterns:
                    match = re.search(pattern, original_title, re.IGNORECASE)
                    if match:
                        attributes['storage'] = match.group(0)
                        break
                
                # RAM - extract from original title
                ram_patterns = [
                    r'(\d+)\s*GB\s*RAM',
                    r'(\d+)\s*GB\s*Memory',
                    r'(\d+)\s*GB\s*RAM\s*Memory',
                ]
                for pattern in ram_patterns:
                    match = re.search(pattern, original_title, re.IGNORECASE)
                    if match:
                        attributes['ram'] = match.group(0)
                        break
                
                # Screen size - extract from original title
                screen_patterns = [
                    r'(\d+\.?\d*)\s*inch',
                    r'(\d+\.?\d*)"',
                    r'(\d+\.?\d*)\s*cm',
                ]
                for pattern in screen_patterns:
                    match = re.search(pattern, original_title, re.IGNORECASE)
                    if match:
                        attributes['screen_size'] = match.group(0)
                        break
                
                # Color - extract from parentheses first, then from name
                color_match = re.search(r'\(([^,)]+),\s*\d+\s*GB\)', original_title)
                if color_match:
                    # Color is usually the first part in parentheses
                    color_text = color_match.group(1).strip()
                    attributes['color'] = color_text
                else:
                    # Fallback to color list
                    colors = ['Black', 'White', 'Blue', 'Red', 'Green', 'Purple', 'Pink', 
                             'Gold', 'Silver', 'Gray', 'Grey', 'Titanium', 'Starlight', 
                             'Midnight', 'Graphite', 'Sierra Blue', 'Alpine Green', 'Rose Gold',
                             'Space Gray', 'Space Grey', 'Jet Black', 'Product Red', 'Coral',
                             'Yellow', 'Orange', 'Lavender', 'Mint', 'Ocean Blue', 'Forest Green',
                             'Moonstone', 'Obsidian', 'Porcelain', 'Cool Blue', 'Desert Gold']
                    for color in colors:
                        if color.lower() in original_title_lower:
                            attributes['color'] = color
                            break
                
                # Model/Series extraction - use cleaned name
                model_patterns = [
                    r'(iPhone\s*\d+[a-zA-Z]*(?:\s*Pro\s*Max)?(?:\s*Plus)?)',
                    r'(Galaxy\s*[A-Z]\d+[a-zA-Z]*)',
                    r'(Pixel\s*\d+[a-zA-Z]*)',
                    r'(OnePlus\s*\d+[a-zA-Z]*)',
                    r'(Redmi\s*[A-Za-z]+\s*\d+)',
                    r'(POCO\s*[A-Z]\d+)',
                    r'([A-Z]\d+[a-zA-Z]*)',  # Generic model numbers
                ]
                for pattern in model_patterns:
                    match = re.search(pattern, product['name'], re.IGNORECASE)
                    if match:
                        attributes['model'] = match.group(1)
                        break
                
                # Add extracted attributes
                product['attributes'] = attributes
                
                # Add brand to top level if found in attributes
                if 'brand' in attributes:
                    product['brand'] = attributes['brand']
                
                # Add metadata
                product['source'] = 'flipkart'
                
                products.append(product)
                
            except Exception as e:
                print(f"  Error extracting product: {e}")
                continue
        
        print(f"Successfully extracted {len(products)} products")
        
    except Exception as e:
        print(f"Error scraping Flipkart: {e}")
        import traceback
        traceback.print_exc()
    
    return products


def main():
    """Main function"""
    print("=" * 60)
    print("Flipkart Phones Scraper")
    print("=" * 60)
    
    # Scrape 20 products
    products = extract_flipkart_products(category="Phones", max_products=20)
    
    if not products:
        print("\nNo products found. This might be due to:")
        print("- Flipkart's anti-scraping measures")
        print("- HTML structure changes")
        print("- Network issues")
        print("\nCannot generate sample data - need real data only.")
        return
    
    # Save to JSON file
    output_file = "flipkart.sample.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 60}")
    print(f"Results saved to: {output_file}")
    print(f"Total products: {len(products)}")
    print(f"{'=' * 60}")
    
    # Show sample products
    print("\nSample products:")
    for idx, product in enumerate(products[:5], 1):
        print(f"\n{idx}. {product.get('name', 'N/A')}")
        print(f"   Brand: {product.get('attributes', {}).get('brand', 'N/A')}")
        print(f"   Price: {product.get('price', 'N/A')}")
        print(f"   Rating: {product.get('rating', 'N/A')}")
        print(f"   Attributes: {product.get('attributes', {})}")


if __name__ == "__main__":
    main()

