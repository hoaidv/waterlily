#!/usr/bin/env python3
"""
Attribute extraction engine using configuration-based rules
"""

import json
import os
import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup


class AttributeExtractor:
    """Extract product attributes based on configuration rules"""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize attribute extractor
        
        Args:
            config_dir: Directory containing configuration files
        """
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
        
        self.config_dir = config_dir
        self.config_cache = {}
    
    def _load_config(self, category: str, website: str) -> Optional[Dict[str, Any]]:
        """
        Load configuration file for category-website combination
        
        Args:
            category: Category name
            website: Website name
        
        Returns:
            Configuration dictionary or None if not found
        """
        # Normalize category name for filename
        category_filename = category.lower().replace("'", "").replace(" ", "_")
        config_key = f"{category_filename}_{website}"
        
        # Check cache first
        if config_key in self.config_cache:
            return self.config_cache[config_key]
        
        # Load from file
        config_file = os.path.join(self.config_dir, f"{config_key}.json")
        
        if not os.path.exists(config_file):
            print(f"      Warning: Config file not found: {config_file}")
            return None
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            self.config_cache[config_key] = config
            return config
        
        except Exception as e:
            print(f"      Error loading config {config_file}: {e}")
            return None
    
    def _extract_by_regex(self, text: str, pattern: str, flags_str: str = None, 
                         group: int = 0) -> Optional[str]:
        """
        Extract value using regex pattern
        
        Args:
            text: Text to search
            pattern: Regex pattern
            flags_str: Regex flags as string (e.g., "IGNORECASE")
            group: Capture group to return (default 0 for full match)
        
        Returns:
            Extracted value or None
        """
        if not text or not pattern:
            return None
        
        # Convert flags string to re flags
        flags = 0
        if flags_str:
            if 'IGNORECASE' in flags_str.upper():
                flags |= re.IGNORECASE
            if 'MULTILINE' in flags_str.upper():
                flags |= re.MULTILINE
            if 'DOTALL' in flags_str.upper():
                flags |= re.DOTALL
        
        try:
            match = re.search(pattern, text, flags)
            if match:
                if group > 0 and len(match.groups()) >= group:
                    return match.group(group)
                elif match.groups():
                    return match.group(1)
                else:
                    return match.group(0)
        except Exception as e:
            print(f"        Regex error: {e}")
        
        return None
    
    def _extract_by_selector(self, soup: BeautifulSoup, selector: str, 
                            attribute: str = None) -> Optional[str]:
        """
        Extract value using CSS selector
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector
            attribute: HTML attribute to extract (if None, extract text)
        
        Returns:
            Extracted value or None
        """
        if not soup or not selector:
            return None
        
        try:
            elem = soup.select_one(selector)
            if elem:
                if attribute:
                    return elem.get(attribute)
                else:
                    return elem.get_text(strip=True)
        except Exception as e:
            print(f"        Selector error: {e}")
        
        return None
    
    def _extract_attribute(self, attr_config: Dict[str, Any], 
                          soup: BeautifulSoup, 
                          product_data: Dict[str, Any]) -> Optional[str]:
        """
        Extract a single attribute based on its configuration
        
        Args:
            attr_config: Attribute configuration
            soup: BeautifulSoup object of product page
            product_data: Basic product data (name, price, etc.)
        
        Returns:
            Extracted attribute value or None
        """
        method = attr_config.get('method', 'regex')
        
        # Determine source text
        source = attr_config.get('source', 'title')
        if source == 'title':
            source_text = product_data.get('name', '')
        elif source == 'description':
            source_text = product_data.get('description', '')
            # If description not in product_data, try to extract from soup
            if not source_text and soup:
                desc_elem = soup.find('section', id='postingbody')
                if desc_elem:
                    source_text = desc_elem.get_text()
        elif source == 'all':
            source_text = soup.get_text() if soup else ''
        else:
            source_text = product_data.get(source, '')
        
        value = None
        
        # Extract based on method
        if method == 'regex':
            pattern = attr_config.get('pattern')
            flags = attr_config.get('flags')
            group = attr_config.get('group', 0)
            value = self._extract_by_regex(source_text, pattern, flags, group)
        
        elif method == 'selector':
            selector = attr_config.get('selector')
            attribute = attr_config.get('attribute')
            value = self._extract_by_selector(soup, selector, attribute)
        
        # Try fallback if primary method failed
        if not value and 'fallback' in attr_config:
            fallback = attr_config['fallback']
            value = self._extract_attribute(fallback, soup, product_data)
        
        # Use default if no value found
        if not value and 'default' in attr_config:
            value = attr_config['default']
        
        return value
    
    def extract_attributes(self, soup: BeautifulSoup, 
                          product_data: Dict[str, Any],
                          category: str,
                          website: str,
                          required_attributes: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Extract all attributes for a product
        
        Args:
            soup: BeautifulSoup object of product page
            product_data: Basic product data
            category: Product category
            website: Source website
            required_attributes: List of required attributes from database (optional)
        
        Returns:
            Dictionary of extracted attributes
        """
        print(f"      🏷️  Extracting attributes using config for {category} on {website}...")
        
        # Load configuration
        config = self._load_config(category, website)
        if not config:
            print(f"      ✗ No configuration found")
            return {}
        
        extracted_attributes = {}
        attr_configs = config.get('attributes', {})
        
        print(f"      → Configured attributes: {len(attr_configs)}")
        
        # Extract each configured attribute
        for attr_name, attr_config in attr_configs.items():
            value = self._extract_attribute(attr_config, soup, product_data)
            if value:
                extracted_attributes[attr_name] = value
                print(f"         ✓ {attr_name}: {value[:50] if len(str(value)) > 50 else value}")
            else:
                print(f"         ✗ {attr_name}: not found")
        
        print(f"      ✓ Extracted {len(extracted_attributes)}/{len(attr_configs)} attributes")
        return extracted_attributes
    
    def validate_attributes(self, extracted: Dict[str, Any], 
                           required: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate extracted attributes against required schema
        
        Args:
            extracted: Extracted attributes
            required: Required attribute definitions from database
        
        Returns:
            Validation report
        """
        report = {
            'valid': True,
            'coverage': 0.0,
            'missing': [],
            'errors': []
        }
        
        if not required:
            report['coverage'] = 1.0 if extracted else 0.0
            return report
        
        # Check which required attributes are present
        required_names = {attr['name'] for attr in required}
        extracted_names = set(extracted.keys())
        
        missing = required_names - extracted_names
        if missing:
            report['missing'] = list(missing)
        
        report['coverage'] = len(extracted_names) / len(required_names) if required_names else 0.0
        
        # Validate datatypes
        for attr in required:
            attr_name = attr['name']
            if attr_name in extracted:
                value = extracted[attr_name]
                datatype = attr.get('datatype', 'STRING')
                
                # Basic type validation
                if datatype == 'NUMBER':
                    try:
                        float(str(value))
                    except ValueError:
                        report['errors'].append(f"{attr_name}: Expected NUMBER, got {value}")
                        report['valid'] = False
                
                elif datatype == 'BOOLEAN':
                    if str(value).lower() not in ['true', 'false', '1', '0', 'yes', 'no']:
                        report['errors'].append(f"{attr_name}: Expected BOOLEAN, got {value}")
                        report['valid'] = False
        
        return report


def main():
    """Test the attribute extractor"""
    from bs4 import BeautifulSoup
    
    print("Testing Attribute Extractor")
    print("=" * 60)
    
    # Create test data
    test_html = """
    <html>
        <body>
            <h1 id="productTitle">Apple iPhone 14 Pro Max 256GB Space Black Unlocked</h1>
            <span class="price">$1099.99</span>
        </body>
    </html>
    """
    
    soup = BeautifulSoup(test_html, 'html.parser')
    product_data = {
        'name': 'Apple iPhone 14 Pro Max 256GB Space Black Unlocked',
        'price': '$1099.99'
    }
    
    # Test extraction
    extractor = AttributeExtractor()
    
    # Test for iPhones on Amazon
    attributes = extractor.extract_attributes(
        soup, 
        product_data, 
        'iPhones', 
        'amazon'
    )
    
    print("\nExtracted attributes for iPhone on Amazon:")
    for attr_name, attr_value in attributes.items():
        print(f"  {attr_name}: {attr_value}")
    
    print("\n" + "=" * 60)
    print("✓ Attribute extractor test completed")


if __name__ == "__main__":
    main()

