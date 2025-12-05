#!/usr/bin/env python3
"""
Scrape 20 products from Amazon Phones category and save to JSON
"""

import json
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, quote_plus


def extract_amazon_products(category: str = "Phones", max_products: int = 20) -> List[Dict[str, Any]]:
    """
    Scrape Amazon products with enhanced attribute extraction
    """
    products = []
    
    # Setup session with realistic headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
    })
    
    try:
        # First, visit Amazon homepage to establish session
        print("Establishing session with Amazon...")
        try:
            homepage_response = session.get('https://www.amazon.com', timeout=15)
            time.sleep(random.uniform(2, 4))
        except:
            pass
        
        # Amazon search URL for phones - try different formats
        search_urls = [
            f"https://www.amazon.com/s?k={quote_plus(category + ' cell phone')}&i=electronics",
            f"https://www.amazon.com/s?k={quote_plus(category)}&i=electronics&ref=sr_pg_1",
        ]
        
        response = None
        for search_url in search_urls:
            print(f"Fetching: {search_url}")
            time.sleep(random.uniform(2, 4))  # Be respectful
            
            try:
                response = session.get(search_url, timeout=15, allow_redirects=True)
                if response.status_code == 200:
                    print(f"Successfully accessed: {search_url}")
                    break
                elif response.status_code == 503:
                    print(f"Got 503 error, waiting longer and retrying...")
                    time.sleep(random.uniform(5, 8))
                    response = session.get(search_url, timeout=15, allow_redirects=True)
                    if response.status_code == 200:
                        break
            except Exception as e:
                print(f"Error with {search_url}: {e}")
                continue
        
        if response.status_code != 200:
            print(f"Error: Got status code {response.status_code}")
            return products
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Method 1: Try to find JSON data in script tags (Amazon embeds product data)
        script_tags = soup.find_all('script', type='application/json')
        product_data_list = []
        
        for script in script_tags:
            try:
                data = json.loads(script.string)
                # Look for product data structures
                if isinstance(data, dict):
                    # Check various possible structures
                    if 'props' in data:
                        props = data['props']
                        if 'pageProps' in props:
                            page_props = props['pageProps']
                            if 'results' in page_props:
                                product_data_list.extend(page_props['results'])
            except:
                continue
        
        # Method 2: Parse HTML structure (Amazon search results)
        # Find product containers - Amazon uses various class names
        product_containers = []
        
        # Try different selectors for Amazon product cards
        selectors = [
            'div[data-component-type="s-search-result"]',
            'div.s-result-item',
            'div[data-asin]',
        ]
        
        for selector in selectors:
            containers = soup.select(selector)
            if containers:
                product_containers = containers
                break
        
        print(f"Found {len(product_containers)} product containers")
        
        # Extract product information
        for container in product_containers[:max_products]:
            try:
                product = {}
                
                # Extract ASIN (Amazon Standard Identification Number)
                asin = container.get('data-asin', '')
                if not asin:
                    asin_elem = container.find(attrs={'data-asin': True})
                    if asin_elem:
                        asin = asin_elem.get('data-asin', '')
                
                # Extract product name/title
                title_elem = container.find('h2', class_=lambda x: x and ('a-size-mini' in str(x) or 'a-size-base' in str(x) or 'a-text-normal' in str(x)))
                if not title_elem:
                    title_elem = container.find('h2')
                if not title_elem:
                    title_elem = container.find('span', class_=lambda x: x and 'a-text-normal' in str(x))
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if title and len(title) > 5:
                        product['name'] = title
                    else:
                        continue
                else:
                    continue
                
                # Extract price - Amazon uses various structures
                # Method 1: Look for a-price class structure
                price_elem = container.find('span', class_=lambda x: x and 'a-price' in str(x))
                if price_elem:
                    # Try to find price whole and fraction
                    price_whole = price_elem.find('span', class_=lambda x: x and 'a-price-whole' in str(x))
                    price_fraction = price_elem.find('span', class_=lambda x: x and 'a-price-fraction' in str(x))
                    if price_whole:
                        price_text = price_whole.get_text(strip=True).replace(',', '')
                        # Validate price is reasonable (under $10,000 for phones)
                        try:
                            price_val = float(price_text)
                            if price_val < 10000:  # Reasonable phone price
                                price = price_text
                                if price_fraction:
                                    price += '.' + price_fraction.get_text(strip=True)
                                product['price'] = f"${price}"
                        except ValueError:
                            pass
                
                # Method 2: Look for price symbol in text
                if 'price' not in product:
                    # Search in container text for price patterns
                    container_text = container.get_text()
                    price_match = re.search(r'\$([\d,]+\.?\d{2})', container_text)
                    if price_match:
                        price_val = float(price_match.group(1).replace(',', ''))
                        if 20 < price_val < 2000:  # Reasonable phone price range
                            product['price'] = f"${price_match.group(1)}"
                
                # Method 3: Look for price spans with dollar signs
                if 'price' not in product:
                    price_spans = container.find_all('span', string=re.compile(r'\$\d+'))
                    for span in price_spans:
                        price_match = re.search(r'\$([\d,]+\.?\d*)', span.get_text())
                        if price_match:
                            price_val = float(price_match.group(1).replace(',', ''))
                            if 20 < price_val < 2000:  # Reasonable phone price range
                                product['price'] = f"${price_match.group(1)}"
                                break
                
                # Method 4: Look for data-a-color attribute with price
                if 'price' not in product:
                    price_attrs = container.find_all(attrs={'data-a-color': re.compile(r'price')})
                    for elem in price_attrs:
                        price_text = elem.get_text(strip=True)
                        price_match = re.search(r'\$([\d,]+\.?\d*)', price_text)
                        if price_match:
                            price_val = float(price_match.group(1).replace(',', ''))
                            if 20 < price_val < 2000:
                                product['price'] = f"${price_match.group(1)}"
                                break
                
                # Extract rating
                rating_elem = container.find('span', class_=lambda x: x and ('a-icon-alt' in str(x) or 'a-icon-star' in str(x)))
                if rating_elem:
                    rating_text = rating_elem.get_text(strip=True)
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        product['rating'] = rating_match.group(1)
                
                # Extract number of reviews
                reviews_elem = container.find('a', class_=lambda x: x and 'a-link-normal' in str(x))
                if reviews_elem:
                    reviews_text = reviews_elem.get_text(strip=True)
                    reviews_match = re.search(r'([\d,]+)', reviews_text.replace(',', ''))
                    if reviews_match:
                        product['review_count'] = reviews_match.group(1)
                
                # Extract brand will be done in attributes extraction below
                
                # Extract attributes from product name (for phones)
                attributes = {}
                
                # Brand extraction
                phone_brands = ['Apple', 'Samsung', 'Google', 'OnePlus', 'Xiaomi', 'Motorola', 
                              'Nokia', 'Sony', 'LG', 'Huawei', 'Oppo', 'Vivo', 'Realme', 
                              'Nothing', 'ASUS', 'TCL', 'ZTE', 'Alcatel']
                title_lower = product['name'].lower()
                for brand in phone_brands:
                    if brand.lower() in title_lower:
                        attributes['brand'] = brand
                        break
                
                # Storage capacity
                storage_patterns = [
                    r'(\d+)\s*GB',
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
                         'Midnight', 'Graphite', 'Sierra Blue', 'Alpine Green']
                for color in colors:
                    if color.lower() in title_lower:
                        attributes['color'] = color
                        break
                
                # Model/Series extraction
                model_patterns = [
                    r'(iPhone\s*\d+[a-zA-Z]*)',
                    r'(Galaxy\s*[A-Z]\d+)',
                    r'(Pixel\s*\d+)',
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
                product['source'] = 'amazon'
                product['asin'] = asin
                product['url'] = f"https://www.amazon.com/dp/{asin}" if asin else None
                
                products.append(product)
                
            except Exception as e:
                print(f"  Error extracting product: {e}")
                continue
        
        print(f"Successfully extracted {len(products)} products")
        
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        import traceback
        traceback.print_exc()
    
    return products


def main():
    """Main function"""
    print("=" * 60)
    print("Amazon Phones Scraper")
    print("=" * 60)
    
    # Scrape 20 products
    products = extract_amazon_products(category="Phones", max_products=20)
    
    if not products:
        print("\nNo products found. This might be due to:")
        print("- Amazon's anti-scraping measures")
        print("- HTML structure changes")
        print("- Network issues")
        return
    
    # Save to JSON file
    output_file = "amazon.sample.json"
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
        print(f"   Price: ${product.get('price', 'N/A')}")
        print(f"   Rating: {product.get('rating', 'N/A')}")
        print(f"   Attributes: {product.get('attributes', {})}")


if __name__ == "__main__":
    main()

