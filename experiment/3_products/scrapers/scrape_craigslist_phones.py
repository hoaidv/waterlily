#!/usr/bin/env python3
"""
Scrape 20 products from Craigslist Phones category and save to JSON
Note: Craigslist is a classified ads site, so products are individual listings
"""

import json
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, quote_plus


def extract_craigslist_products(category: str = "Phones", max_products: int = 20, location: str = "sfbay") -> List[Dict[str, Any]]:
    """
    Scrape Craigslist products with enhanced attribute extraction
    location: Craigslist location code (e.g., 'sfbay', 'nyc', 'losangeles')
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
        # Craigslist search URL for electronics/phones
        # Using electronics category with phone search
        search_url = f"https://{location}.craigslist.org/search/sss?query={quote_plus(category + ' cell phone')}&sort=rel"
        
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
        
        # Find product listings - Craigslist uses various class names
        product_rows = []
        
        # Try different selectors for Craigslist listings
        selectors = [
            ('li', {'class': 'result-row'}),
            ('li', {'class': lambda x: x and 'result' in str(x).lower()}),
            ('div', {'class': 'result-row'}),
            ('div', {'class': lambda x: x and 'result' in str(x).lower()}),
            ('li', {'data-pid': True}),
        ]
        
        for tag, attrs in selectors:
            rows = soup.find_all(tag, attrs)
            if rows:
                product_rows = rows
                print(f"Found {len(product_rows)} product listings using {tag} with {attrs}")
                break
        
        # Alternative: find by links to post pages
        if not product_rows:
            post_links = soup.find_all('a', href=re.compile(r'/\d+\.html'))
            seen_links = set()
            for link in post_links:
                href = link.get('href', '')
                if href and href not in seen_links:
                    parent = link.find_parent(['li', 'div'])
                    if parent:
                        product_rows.append(parent)
                        seen_links.add(href)
                        if len(product_rows) >= max_products:
                            break
            if product_rows:
                print(f"Found {len(product_rows)} product listings using post links")
        
        print(f"Total found: {len(product_rows)} product listings")
        
        # Extract product information
        for row in product_rows[:max_products]:
            try:
                product = {}
                
                # Extract product name/title - try multiple methods
                title_elem = row.find('a', class_='result-title')
                if not title_elem:
                    title_elem = row.find('a', class_=lambda x: x and 'title' in str(x).lower())
                if not title_elem:
                    title_elem = row.find('a', href=re.compile(r'/\d+\.html'))
                if not title_elem:
                    # Try finding any link in the row
                    title_elem = row.find('a', href=True)
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if not title:
                        title = title_elem.get('title', '').strip()
                    if not title:
                        title = title_elem.get('aria-label', '').strip()
                    
                    # Clean up title - remove embedded prices and locations
                    title = re.sub(r'\s+', ' ', title).strip()
                    
                    # Extract price from title if not already extracted
                    if 'price' not in product:
                        # Try to find price pattern - $ followed by digits
                        price_match = re.search(r'\$(\d+)', title)
                        if price_match:
                            price_val = float(price_match.group(1))
                            if 5 < price_val < 2000:  # Reasonable price range
                                product['price'] = f"${price_match.group(1)}"
                                # Remove price from title - handle various patterns
                                # Pattern: $XXlocation, $XX location, or $XX at end
                                price_str = f"${price_match.group(1)}"
                                # Remove price and any text immediately following it
                                title = re.sub(re.escape(price_str) + r'\s*[A-Za-z\s/]*', '', title).strip()
                                title = re.sub(re.escape(price_str) + r'$', '', title).strip()
                                title = re.sub(re.escape(price_str), '', title).strip()
                    
                    # Extract location from title (common pattern: location at end)
                    # Common Bay Area locations - check longer names first
                    bay_area_locations = ['union city', 'san jose', 'san francisco', 'palo alto',
                                        'mountain view', 'santa clara', 'livermore', 'fremont', 
                                        'newark', 'gilroy', 'oakland', 'berkeley', 'sunnyvale', 'cupertino']
                    title_lower = title.lower()
                    
                    # Try to find location pattern (usually at end)
                    if 'location' not in product:
                        # Look for location patterns like "fremont / union city / newark" or "san jose north"
                        loc_patterns = [
                            r'(fremont\s*/\s*union\s*city\s*/\s*newark)',
                            r'(san\s+jose\s+(?:north|south|east|west)?)',
                            r'((?:fremont|union\s*city|newark|livermore|gilroy|oakland|berkeley|san\s+jose|san\s+francisco|palo\s+alto|mountain\s+view|santa\s+clara|sunnyvale|cupertino)(?:\s+/\s+(?:fremont|union\s*city|newark|livermore|gilroy|oakland|berkeley|san\s+jose|san\s+francisco|palo\s+alto|mountain\s+view|santa\s+clara|sunnyvale|cupertino))*(?:\s+(?:north|south|east|west))?)',
                        ]
                        
                        for pattern in loc_patterns:
                            loc_match = re.search(pattern, title_lower)
                            if loc_match:
                                product['location'] = loc_match.group(1).title()
                                # Remove location from title
                                title = re.sub(rf'{re.escape(loc_match.group(1))}', '', title, flags=re.IGNORECASE).strip()
                                break
                    
                    # Remove any remaining price patterns at the end
                    title = re.sub(r'\$\d+$', '', title).strip()
                    # Remove common suffixes and clean up
                    title = re.sub(r'\s*(Reduced Price|Price|Sale|New|Used|Refurbished|,?\s*Ca\.?|,?\s*CA\.?)$', '', title, flags=re.IGNORECASE).strip()
                    # Remove trailing location fragments like "city / newark", "north", etc.
                    title = re.sub(r'\s*(city|north|south|east|west|/\s*\w+).*$', '', title, flags=re.IGNORECASE).strip()
                    # Remove trailing commas and periods
                    title = re.sub(r'[,\.]+$', '', title).strip()
                    # Remove any remaining location-like patterns at the end
                    title = re.sub(r'\s*[A-Z][a-z]+\s*/\s*[A-Z][a-z]+.*$', '', title).strip()
                    # Final cleanup - remove any remaining price patterns
                    title = re.sub(r'\$\d+', '', title).strip()
                    title = re.sub(r'\s+', ' ', title).strip()
                    
                    if title and len(title) > 5:
                        product['name'] = title
                    else:
                        continue
                else:
                    continue
                
                # Extract product URL
                if title_elem:
                    href = title_elem.get('href', '')
                    if href.startswith('/'):
                        product['url'] = f"https://{location}.craigslist.org{href}"
                    elif href.startswith('http'):
                        product['url'] = href
                    else:
                        product['url'] = f"https://{location}.craigslist.org/{href}"
                    
                    # Extract post ID from URL
                    post_id_match = re.search(r'/(\d+)\.html', href)
                    if post_id_match:
                        product['post_id'] = post_id_match.group(1)
                
                # Extract price - try multiple methods
                price_elem = row.find('span', class_='result-price')
                if not price_elem:
                    price_elem = row.find('span', class_=lambda x: x and 'price' in str(x).lower())
                if not price_elem:
                    price_elem = row.find('span', string=re.compile(r'\$'))
                if not price_elem:
                    # Try finding price in row text
                    row_text = row.get_text()
                    price_match = re.search(r'\$([\d,]+)', row_text)
                    if price_match:
                        price_val = float(price_match.group(1).replace(',', ''))
                        if 20 < price_val < 2000:
                            product['price'] = f"${price_match.group(1)}"
                
                if price_elem and 'price' not in product:
                    price_text = price_elem.get_text(strip=True)
                    price_match = re.search(r'\$([\d,]+)', price_text)
                    if price_match:
                        price_val = float(price_match.group(1).replace(',', ''))
                        if 20 < price_val < 2000:  # Reasonable phone price range
                            product['price'] = price_text
                
                # Extract location/neighborhood - try multiple methods
                location_elem = row.find('span', class_='result-hood')
                if not location_elem:
                    location_elem = row.find('span', class_='nearby')
                if not location_elem:
                    location_elem = row.find('span', class_=lambda x: x and ('hood' in str(x).lower() or 'location' in str(x).lower()))
                
                if location_elem:
                    location_text = location_elem.get_text(strip=True)
                    if location_text:
                        product['location'] = location_text.strip('()')
                
                # If location not found in element, try extracting from row text
                if 'location' not in product:
                    row_text = row.get_text()
                    # Look for common location patterns
                    location_match = re.search(r'([A-Z][a-z]+(?:\s+/\s+[A-Z][a-z]+)*(?:\s+/\s+[A-Z][a-z]+)*)', row_text)
                    if location_match:
                        loc_text = location_match.group(1)
                        # Check if it's a known location (not a brand or model)
                        bay_area_locations = ['Livermore', 'Fremont', 'Union City', 'Newark', 'San Jose', 
                                            'Gilroy', 'Oakland', 'Berkeley', 'San Francisco', 'Palo Alto']
                        if any(loc.lower() in loc_text.lower() for loc in bay_area_locations):
                            product['location'] = loc_text
                
                # Extract post date
                date_elem = row.find('time', class_='result-date')
                if not date_elem:
                    date_elem = row.find('time')
                if date_elem:
                    date_text = date_elem.get('datetime', '')
                    if not date_text:
                        date_text = date_elem.get_text(strip=True)
                    if date_text:
                        product['date'] = date_text
                
                # Extract image URL if available
                img_elem = row.find('img')
                if img_elem:
                    img_src = img_elem.get('src', '')
                    if img_src:
                        product['image_url'] = img_src
                
                # Extract attributes from product name (for phones)
                attributes = {}
                title_lower = product['name'].lower()
                
                # Brand extraction
                phone_brands = ['Apple', 'Samsung', 'Google', 'OnePlus', 'Xiaomi', 'Motorola', 
                              'Nokia', 'Sony', 'LG', 'Huawei', 'Oppo', 'Vivo', 'Realme', 
                              'Nothing', 'ASUS', 'TCL', 'ZTE', 'Alcatel', 'iPhone', 'Galaxy',
                              'Pixel', 'BLU', 'Tracfone']
                for brand in phone_brands:
                    if brand.lower() in title_lower:
                        # Normalize brand names
                        if brand == 'iPhone':
                            attributes['brand'] = 'Apple'
                        elif brand == 'Galaxy':
                            attributes['brand'] = 'Samsung'
                        elif brand == 'Pixel':
                            attributes['brand'] = 'Google'
                        else:
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
                        attributes['storage'] = match.group(0)
                        break
                
                # RAM
                ram_patterns = [
                    r'(\d+)\s*GB\s*RAM',
                    r'(\d+)\s*GB\s*Memory',
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
                         'Space Gray', 'Space Grey', 'Jet Black', 'Product Red']
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
                    r'([A-Z]\d+[a-zA-Z]*)',  # Generic model numbers
                ]
                for pattern in model_patterns:
                    match = re.search(pattern, product['name'], re.IGNORECASE)
                    if match:
                        attributes['model'] = match.group(1)
                        break
                
                # Condition extraction
                if 'new' in title_lower and ('sealed' in title_lower or 'unopened' in title_lower):
                    attributes['condition'] = 'New Sealed'
                elif 'new' in title_lower:
                    attributes['condition'] = 'New'
                elif 'renewed' in title_lower or 'refurbished' in title_lower:
                    attributes['condition'] = 'Refurbished'
                elif 'used' in title_lower or 'pre-owned' in title_lower:
                    attributes['condition'] = 'Used'
                elif 'broken' in title_lower or 'parts' in title_lower:
                    attributes['condition'] = 'For Parts'
                
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
                
                # Add extracted attributes
                product['attributes'] = attributes
                
                # Add brand to top level if found in attributes
                if 'brand' in attributes:
                    product['brand'] = attributes['brand']
                
                # Add metadata
                product['source'] = 'craigslist'
                product['location_code'] = location
                
                products.append(product)
                
            except Exception as e:
                print(f"  Error extracting product: {e}")
                continue
        
        print(f"Successfully extracted {len(products)} products")
        
    except Exception as e:
        print(f"Error scraping Craigslist: {e}")
        import traceback
        traceback.print_exc()
    
    return products


def main():
    """Main function"""
    print("=" * 60)
    print("Craigslist Phones Scraper")
    print("=" * 60)
    
    # Scrape 20 products from San Francisco Bay Area
    products = extract_craigslist_products(category="Phones", max_products=20, location="sfbay")
    
    if not products:
        print("\nNo products found. This might be due to:")
        print("- Craigslist's anti-scraping measures")
        print("- HTML structure changes")
        print("- Network issues")
        print("- No listings available in the selected location")
        return
    
    # Save to JSON file
    output_file = "craigslist.sample.json"
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
        print(f"   Location: {product.get('location', 'N/A')}")
        print(f"   Condition: {product.get('attributes', {}).get('condition', 'N/A')}")
        print(f"   Attributes: {product.get('attributes', {})}")


if __name__ == "__main__":
    main()

