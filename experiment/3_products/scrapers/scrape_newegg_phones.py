#!/usr/bin/env python3
"""
Scrape 20 products from Newegg Phones category and save to JSON
"""

import json
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, quote_plus


def extract_newegg_products(category: str = "Phones", max_products: int = 20) -> List[Dict[str, Any]]:
    """
    Scrape Newegg products with enhanced attribute extraction
    """
    products = []
    
    # Setup session with realistic headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    })
    
    try:
        # Newegg search URL for phones - try different formats
        # First try visiting homepage to establish session
        print("Establishing session with Newegg...")
        homepage_response = session.get('https://www.newegg.com', timeout=15)
        time.sleep(random.uniform(1, 2))
        
        # Try search URL with different format
        search_url = f"https://www.newegg.com/p/pl?d={quote_plus('cell phone')}"
        
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
            
            # If blocked, return empty list
            if 'blocked' in page_title.lower() or 'access denied' in page_title.lower():
                print("Newegg appears to be blocking requests.")
                return products
        
        # Find product containers - Newegg uses various class names
        product_containers = []
        
        # Try different selectors for Newegg product items
        selectors = [
            'div.item-cell',
            'div.item-container',
            'div[class*="item"]',
            'a.item-title',
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
                
                # Extract product name/title
                title_elem = container.find('a', class_=lambda x: x and ('title' in str(x).lower() or 'item-title' in str(x)))
                if not title_elem:
                    title_elem = container.find('a', href=re.compile(r'/p/'))
                if not title_elem:
                    title_elem = container.find('div', class_=lambda x: x and 'title' in str(x).lower())
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if not title:
                        title = title_elem.get('title', '').strip()
                    if not title:
                        title = title_elem.get('aria-label', '').strip()
                    
                    # Clean up title - remove extra whitespace and trailing text
                    title = re.sub(r'\s+', ' ', title).strip()
                    # Fix "Open Box" prefix - add space if missing
                    title = re.sub(r'^Open Box([A-Z])', r'Open Box \1', title)
                    # Fix "Refurbished" prefix - add space if missing
                    title = re.sub(r'^Refurbished([A-Z])', r'Refurbished \1', title)
                    # Remove trailing "Phone" or "Smartphone" if it appears as separate word
                    title = re.sub(r'\s+(Phone|Smartphone|Cell Phone)$', '', title, flags=re.IGNORECASE)
                    # Remove newlines and extra text
                    title = re.sub(r'\n.*$', '', title).strip()
                    # Remove any trailing whitespace
                    title = title.strip()
                    
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
                        product['url'] = 'https://www.newegg.com' + href
                    else:
                        product['url'] = href
                    
                    # Extract product ID from URL
                    product_id_match = re.search(r'/p/([A-Z0-9-]+)', href)
                    if product_id_match:
                        product['product_id'] = product_id_match.group(1)
                
                # Extract price - Newegg uses $ symbol
                # Try multiple selectors for price
                price_elem = container.find('li', class_=lambda x: x and ('price-current' in str(x).lower() or 'price' in str(x).lower()))
                if not price_elem:
                    price_elem = container.find('span', class_=lambda x: x and ('price-current' in str(x).lower() or 'price' in str(x).lower()))
                if not price_elem:
                    price_elem = container.find('strong', class_=lambda x: x and 'price' in str(x).lower())
                if not price_elem:
                    # Try finding any element with price text
                    price_elem = container.find(string=re.compile(r'\$\d+'))
                    if price_elem:
                        price_elem = price_elem.find_parent()
                
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Extract price value - handle formats like "$459.99" or "$459"
                    price_match = re.search(r'\$([\d,]+\.?\d*)', price_text)
                    if price_match:
                        price_val = float(price_match.group(1).replace(',', ''))
                        if 50 < price_val < 2000:  # Reasonable phone price range
                            product['price'] = f"${price_match.group(1)}"
                
                # If still no price, try searching container text
                if 'price' not in product:
                    container_text = container.get_text()
                    price_match = re.search(r'\$([\d,]+\.?\d*)', container_text)
                    if price_match:
                        price_val = float(price_match.group(1).replace(',', ''))
                        if 50 < price_val < 2000:
                            product['price'] = f"${price_match.group(1)}"
                
                # Extract rating - try multiple methods
                rating_elem = container.find('a', class_=lambda x: x and ('rating' in str(x).lower()))
                if rating_elem:
                    rating_text = rating_elem.get('title', '')
                    if not rating_text:
                        rating_text = rating_elem.get_text(strip=True)
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        product['rating'] = rating_match.group(1)
                
                # If not found, try finding rating in container text or other elements
                if 'rating' not in product:
                    # Look for star ratings or rating patterns
                    rating_elem = container.find('i', class_=lambda x: x and ('star' in str(x).lower() or 'rating' in str(x).lower()))
                    if rating_elem:
                        # Check parent for rating value
                        parent = rating_elem.find_parent()
                        if parent:
                            rating_text = parent.get_text(strip=True)
                            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                            if rating_match:
                                product['rating'] = rating_match.group(1)
                
                # Extract number of reviews
                reviews_elem = container.find('a', class_=lambda x: x and ('review' in str(x).lower()))
                if reviews_elem:
                    reviews_text = reviews_elem.get_text(strip=True)
                    reviews_match = re.search(r'\((\d+)\)', reviews_text)
                    if reviews_match:
                        product['review_count'] = reviews_match.group(1)
                    else:
                        # Try alternative pattern
                        reviews_match = re.search(r'(\d+)\s*(?:reviews?|ratings?)', reviews_text, re.IGNORECASE)
                        if reviews_match:
                            product['review_count'] = reviews_match.group(1)
                
                # Extract shipping info - try multiple methods
                shipping_elem = container.find('li', class_=lambda x: x and ('shipping' in str(x).lower()))
                if not shipping_elem:
                    shipping_elem = container.find('span', class_=lambda x: x and 'shipping' in str(x).lower())
                if not shipping_elem:
                    shipping_elem = container.find('div', class_=lambda x: x and 'shipping' in str(x).lower())
                
                if shipping_elem:
                    shipping_text = shipping_elem.get_text(strip=True)
                    # Clean up shipping text - extract just the shipping info
                    if shipping_text:
                        # Look for "Free Shipping" or shipping cost patterns
                        free_shipping_match = re.search(r'Free\s+Shipping', shipping_text, re.IGNORECASE)
                        if free_shipping_match:
                            product['shipping'] = 'Free Shipping'
                        else:
                            # Try to extract shipping cost
                            shipping_cost_match = re.search(r'\$\d+\.?\d*\s*(?:Shipping|Ships)', shipping_text, re.IGNORECASE)
                            if shipping_cost_match:
                                product['shipping'] = shipping_cost_match.group(0)
                            elif len(shipping_text) < 80:  # Only use if reasonably short
                                product['shipping'] = shipping_text
                else:
                    # Try finding shipping in container text
                    container_text = container.get_text()
                    free_shipping_match = re.search(r'Free\s+Shipping', container_text, re.IGNORECASE)
                    if free_shipping_match:
                        product['shipping'] = 'Free Shipping'
                    else:
                        shipping_match = re.search(r'\$\d+\.?\d*\s*(?:Shipping|Ships)', container_text, re.IGNORECASE)
                        if shipping_match:
                            product['shipping'] = shipping_match.group(0)
                
                # Extract promo/rebate info
                promo_elem = container.find('span', class_=lambda x: x and ('promo' in str(x).lower() or 'rebate' in str(x).lower()))
                if promo_elem:
                    promo_text = promo_elem.get_text(strip=True)
                    if promo_text:
                        product['promo'] = promo_text
                
                # Extract attributes from product name (for phones)
                attributes = {}
                title_lower = product['name'].lower()
                
                # Brand extraction
                phone_brands = ['Apple', 'Samsung', 'Google', 'OnePlus', 'Xiaomi', 'Motorola', 
                              'Nokia', 'Sony', 'LG', 'Huawei', 'Oppo', 'Vivo', 'Realme', 
                              'Nothing', 'ASUS', 'TCL', 'ZTE', 'Alcatel', 'Redmi', 'POCO',
                              'BLU', 'Tracfone', 'Unihertz', 'Ulefone']
                for brand in phone_brands:
                    if brand.lower() in title_lower:
                        attributes['brand'] = brand
                        break
                
                # Storage capacity
                storage_patterns = [
                    r'(\d+)\s*GB\s*(?:Storage|ROM|Memory)',
                    r'(\d+)\s*GB\s*(?!RAM)',
                    r'(\d+)\s*TB',
                ]
                for pattern in storage_patterns:
                    match = re.search(pattern, product['name'], re.IGNORECASE)
                    if match:
                        # Clean up storage value - remove trailing spaces
                        storage_val = match.group(0).strip()
                        attributes['storage'] = storage_val
                        break
                
                # RAM
                ram_patterns = [
                    r'(\d+)\s*GB\s*RAM',
                    r'(\d+)\s*GB\s*Memory',
                    r'(\d+)\s*GB\s*RAM\s*Memory',
                ]
                for pattern in ram_patterns:
                    match = re.search(pattern, product['name'], re.IGNORECASE)
                    if match:
                        attributes['ram'] = match.group(0)
                        break
                
                # Screen size
                screen_patterns = [
                    r'(\d+\.?\d*)\s*inch',
                    r'(\d+\.?\d*)"',
                    r'(\d+\.?\d*)\s*in',
                ]
                for pattern in screen_patterns:
                    match = re.search(pattern, product['name'], re.IGNORECASE)
                    if match:
                        attributes['screen_size'] = match.group(0)
                        break
                
                # Color
                colors = ['Black', 'White', 'Blue', 'Red', 'Green', 'Purple', 'Pink', 
                         'Gold', 'Silver', 'Gray', 'Grey', 'Titanium', 'Starlight', 
                         'Midnight', 'Graphite', 'Sierra Blue', 'Alpine Green', 'Rose Gold',
                         'Space Gray', 'Space Grey', 'Jet Black', 'Product Red', 'Coral',
                         'Yellow', 'Orange', 'Lavender', 'Mint']
                for color in colors:
                    if color.lower() in title_lower:
                        attributes['color'] = color
                        break
                
                # Model/Series extraction
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
                
                # Carrier/Unlocked status
                if 'unlocked' in title_lower:
                    attributes['carrier'] = 'Unlocked'
                elif 'at&t' in title_lower or 'att' in title_lower:
                    attributes['carrier'] = 'AT&T'
                elif 'verizon' in title_lower:
                    attributes['carrier'] = 'Verizon'
                elif 't-mobile' in title_lower or 'tmobile' in title_lower:
                    attributes['carrier'] = 'T-Mobile'
                elif 'sprint' in title_lower:
                    attributes['carrier'] = 'Sprint'
                
                # Condition extraction
                if 'new' in title_lower:
                    attributes['condition'] = 'New'
                elif 'renewed' in title_lower or 'refurbished' in title_lower:
                    attributes['condition'] = 'Refurbished'
                elif 'used' in title_lower or 'pre-owned' in title_lower:
                    attributes['condition'] = 'Used'
                
                # Add extracted attributes
                product['attributes'] = attributes
                
                # Add brand to top level if found in attributes
                if 'brand' in attributes:
                    product['brand'] = attributes['brand']
                
                # Add metadata
                product['source'] = 'newegg'
                
                products.append(product)
                
            except Exception as e:
                print(f"  Error extracting product: {e}")
                continue
        
        print(f"Successfully extracted {len(products)} products")
        
    except Exception as e:
        print(f"Error scraping Newegg: {e}")
        import traceback
        traceback.print_exc()
    
    return products


def main():
    """Main function"""
    print("=" * 60)
    print("Newegg Phones Scraper")
    print("=" * 60)
    
    # Scrape 20 products
    products = extract_newegg_products(category="Phones", max_products=20)
    
    if not products:
        print("\nNo products found. This might be due to:")
        print("- Newegg's anti-scraping measures")
        print("- HTML structure changes")
        print("- Network issues")
        print("\nCannot generate sample data - need real data only.")
        return
    
    # Save to JSON file
    output_file = "newegg.sample.json"
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
        print(f"   Shipping: {product.get('shipping', 'N/A')}")
        print(f"   Attributes: {product.get('attributes', {})}")


if __name__ == "__main__":
    main()

