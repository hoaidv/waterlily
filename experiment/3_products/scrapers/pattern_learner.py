#!/usr/bin/env python3
"""
Pattern learner for extracting structured data from HTML
Analyzes HTML pages to learn extraction patterns for product attributes
"""

import re
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import Counter, defaultdict
from lxml import html, etree
import logging


class PatternLearner:
    """
    Learns extraction patterns from HTML pages
    Focuses on finding tables and structured data
    """
    
    def __init__(self):
        """Initialize pattern learner"""
        self.patterns = {}
        self.pattern_frequency = defaultdict(lambda: defaultdict(int))
    
    def analyze_product_page(self, html_content: str, product_url: str) -> Dict[str, Any]:
        """
        Analyze a product page to find extraction patterns
        
        Args:
            html_content: HTML content of the page
            product_url: URL of the product (for logging)
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            tree = html.fromstring(html_content)
        except Exception as e:
            logging.error(f"Failed to parse HTML: {e}")
            return {
                'success': False,
                'error': str(e),
                'url': product_url
            }
        
        analysis = {
            'success': True,
            'url': product_url,
            'tables_found': [],
            'structured_data': [],
            'key_value_pairs': [],
            'extraction_rules': []
        }
        
        # Find all tables
        tables = tree.xpath('//table')
        logging.info(f"Found {len(tables)} tables on page")
        
        for idx, table in enumerate(tables):
            table_info = self._analyze_table(table, idx)
            if table_info['has_attributes']:
                analysis['tables_found'].append(table_info)
        
        # Find structured div/dl patterns (key-value pairs)
        structured_divs = self._find_structured_divs(tree)
        analysis['structured_data'].extend(structured_divs)
        
        # Find definition lists (dl/dt/dd)
        definition_lists = self._find_definition_lists(tree)
        analysis['structured_data'].extend(definition_lists)
        
        # Generate extraction rules from found patterns
        analysis['extraction_rules'] = self._generate_extraction_rules(analysis)
        
        return analysis
    
    def _analyze_table(self, table_elem, table_index: int) -> Dict[str, Any]:
        """
        Analyze a table element to determine if it contains product attributes
        
        Args:
            table_elem: lxml table element
            table_index: Index of the table on the page
            
        Returns:
            Dictionary with table analysis
        """
        table_info = {
            'index': table_index,
            'has_attributes': False,
            'rows': 0,
            'key_value_pairs': [],
            'xpath': None,
            'id': None,
            'class': None
        }
        
        # Get table attributes
        table_info['id'] = table_elem.get('id')
        table_info['class'] = table_elem.get('class')
        
        # Generate XPath
        if table_info['id']:
            table_info['xpath'] = f"//table[@id='{table_info['id']}']"
        elif table_info['class']:
            table_info['xpath'] = f"//table[@class='{table_info['class']}']"
        else:
            table_info['xpath'] = f"(//table)[{table_index + 1}]"
        
        # Analyze table rows
        rows = table_elem.xpath('.//tr')
        table_info['rows'] = len(rows)
        
        for row in rows:
            # Look for key-value pattern in rows
            cells = row.xpath('.//th | .//td')
            
            if len(cells) == 2:
                # Potential key-value pair
                key = self._extract_text(cells[0]).strip()
                value = self._extract_text(cells[1]).strip()
                
                if key and value and len(key) < 100 and self._is_valid_attribute_name(key):
                    table_info['key_value_pairs'].append({
                        'key': key,
                        'value': value
                    })
                    table_info['has_attributes'] = True
        
        return table_info
    
    def _find_structured_divs(self, tree) -> List[Dict[str, Any]]:
        """
        Find div elements with structured key-value data
        
        Args:
            tree: lxml tree
            
        Returns:
            List of structured data patterns
        """
        structured_data = []
        
        # Common patterns for product specifications
        patterns = [
            "//div[contains(@class, 'spec')]",
            "//div[contains(@class, 'detail')]",
            "//div[contains(@class, 'attribute')]",
            "//div[contains(@class, 'feature')]",
            "//div[contains(@id, 'spec')]",
            "//div[contains(@id, 'detail')]",
        ]
        
        for pattern in patterns:
            elements = tree.xpath(pattern)
            
            for elem in elements[:5]:  # Limit to first 5 matches per pattern
                # Try to extract key-value pairs
                kv_pairs = self._extract_key_values_from_div(elem)
                
                if kv_pairs:
                    structured_data.append({
                        'type': 'div',
                        'xpath': pattern,
                        'id': elem.get('id'),
                        'class': elem.get('class'),
                        'key_value_pairs': kv_pairs
                    })
        
        return structured_data
    
    def _find_definition_lists(self, tree) -> List[Dict[str, Any]]:
        """
        Find definition lists (dl/dt/dd) with product attributes
        
        Args:
            tree: lxml tree
            
        Returns:
            List of definition list patterns
        """
        definition_lists = []
        
        dl_elements = tree.xpath('//dl')
        
        for idx, dl in enumerate(dl_elements):
            kv_pairs = []
            
            # Extract dt (term) and dd (definition) pairs
            terms = dl.xpath('.//dt')
            definitions = dl.xpath('.//dd')
            
            for term, definition in zip(terms, definitions):
                key = self._extract_text(term).strip()
                value = self._extract_text(definition).strip()
                
                if key and value and self._is_valid_attribute_name(key):
                    kv_pairs.append({
                        'key': key,
                        'value': value
                    })
            
            if kv_pairs:
                dl_id = dl.get('id')
                dl_class = dl.get('class')
                
                if dl_id:
                    xpath = f"//dl[@id='{dl_id}']"
                elif dl_class:
                    xpath = f"//dl[@class='{dl_class}']"
                else:
                    xpath = f"(//dl)[{idx + 1}]"
                
                definition_lists.append({
                    'type': 'dl',
                    'xpath': xpath,
                    'id': dl_id,
                    'class': dl_class,
                    'key_value_pairs': kv_pairs
                })
        
        return definition_lists
    
    def _extract_key_values_from_div(self, div_elem) -> List[Dict[str, str]]:
        """
        Extract key-value pairs from a div element
        
        Args:
            div_elem: lxml div element
            
        Returns:
            List of key-value dictionaries
        """
        kv_pairs = []
        
        # Look for nested spans or divs with key-value pattern
        # Pattern 1: <span class="label">Key</span><span class="value">Value</span>
        labels = div_elem.xpath('.//span[contains(@class, "label") or contains(@class, "key")]')
        
        for label in labels:
            key = self._extract_text(label).strip()
            # Try to find the corresponding value
            value_elem = label.xpath('./following-sibling::span[1]')
            if value_elem:
                value = self._extract_text(value_elem[0]).strip()
                if key and value and self._is_valid_attribute_name(key):
                    kv_pairs.append({'key': key, 'value': value})
        
        # Pattern 2: Look for text with colon separator
        text = self._extract_text(div_elem)
        lines = text.split('\n')
        
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key and value and len(key) < 100 and self._is_valid_attribute_name(key):
                        kv_pairs.append({'key': key, 'value': value})
        
        return kv_pairs
    
    def _is_valid_attribute_name(self, name: str) -> bool:
        """
        Check if a name looks like a valid product attribute (not code)
        
        Args:
            name: Attribute name to validate
            
        Returns:
            True if valid, False if it looks like code
        """
        if not name:
            return False
        
        # Filter out obvious code patterns
        code_patterns = [
            r'function\s*\(',  # JavaScript functions
            r'var\s+\w+',      # Variable declarations
            r'window\.',       # Window object
            r'return\s+',      # Return statements
            r'\.push\(',       # Array push
            r'\.load\(',       # Load calls
            r'\.create\(',     # Create calls
            r'\.execute\(',    # Execute calls
            r'=>',             # Arrow functions
            r'const\s+',       # Const declarations
            r'let\s+',         # Let declarations
            r'\{.*\}',         # Curly braces (objects/blocks)
            r'\[.*\]',         # Square brackets (arrays)
            r'===|!==',        # Strict comparison
            r'typeof\s+',      # Typeof operator
            r'^\w+\(',         # Function calls at start
            r'javascript:',    # JavaScript protocol
            r'void\(',         # Void operator
            r'__\w+__',        # Double underscore names (internal)
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, name, re.IGNORECASE):
                return False
        
        # Filter out CSS property names
        css_properties = {
            'color', 'background', 'margin', 'padding', 'border', 'width', 'height',
            'display', 'position', 'top', 'left', 'right', 'bottom', 'float',
            'font-size', 'font-weight', 'font-family', 'line-height', 'text-align',
            'word-wrap', 'overflow', 'z-index', 'opacity', 'cursor', 'visibility'
        }
        
        if name.lower() in css_properties:
            return False
        
        # Must contain at least one letter
        if not re.search(r'[a-zA-Z]', name):
            return False
        
        # Shouldn't start with special characters or numbers
        if re.match(r'^[^a-zA-Z]', name):
            return False
        
        # Shouldn't contain too many special characters (indicates code)
        special_char_count = len(re.findall(r'[^a-zA-Z0-9\s\-_]', name))
        if special_char_count > 2:
            return False
        
        return True
    
    def _extract_text(self, elem) -> str:
        """
        Extract all text from an element, excluding script and style tags
        
        Args:
            elem: lxml element
            
        Returns:
            Extracted text
        """
        # Remove script and style elements first
        for script in elem.xpath('.//script | .//style'):
            script.getparent().remove(script)
        
        return ' '.join(elem.itertext()).strip()
    
    def _generate_extraction_rules(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate extraction rules based on analysis
        
        Args:
            analysis: Analysis results
            
        Returns:
            List of extraction rules
        """
        rules = []
        
        # Rules from tables
        for table in analysis['tables_found']:
            if table['has_attributes']:
                sample_keys = [kv['key'] for kv in table['key_value_pairs'][:5]]
                
                # Validate that sample keys look legitimate
                valid_keys = [k for k in sample_keys if self._is_valid_attribute_name(k)]
                
                # Only add rule if most keys are valid
                if len(valid_keys) >= len(sample_keys) * 0.6:  # At least 60% valid
                    rule = {
                        'type': 'table',
                        'priority': 1 if table['id'] else (2 if table['class'] else 3),
                        'xpath': table['xpath'],
                        'extraction_method': 'table_key_value',
                        'sample_keys': valid_keys[:5]
                    }
                    rules.append(rule)
        
        # Rules from structured data
        for struct in analysis['structured_data']:
            sample_keys = [kv['key'] for kv in struct['key_value_pairs'][:5]]
            
            # Validate that sample keys look legitimate
            valid_keys = [k for k in sample_keys if self._is_valid_attribute_name(k)]
            
            # Only add rule if most keys are valid (stricter for divs)
            if len(valid_keys) >= len(sample_keys) * 0.8:  # At least 80% valid for divs
                rule = {
                    'type': struct['type'],
                    'priority': 1 if struct['id'] else (2 if struct['class'] else 3),
                    'xpath': struct['xpath'],
                    'extraction_method': 'key_value_pairs',
                    'sample_keys': valid_keys[:5]
                }
                rules.append(rule)
        
        # Sort by priority (lower is better)
        rules.sort(key=lambda x: x['priority'])
        
        return rules
    
    def learn_patterns(self, analyses: List[Dict[str, Any]], category_name: str) -> Dict[str, Any]:
        """
        Learn extraction patterns from multiple product analyses
        
        Args:
            analyses: List of analysis results from multiple products
            category_name: Name of the category
            
        Returns:
            Learned patterns for the category
        """
        # Collect all rules from all analyses
        all_rules = []
        for analysis in analyses:
            if analysis.get('success'):
                all_rules.extend(analysis.get('extraction_rules', []))
        
        if not all_rules:
            return {
                'category': category_name,
                'patterns_found': False,
                'rules': []
            }
        
        # Count frequency of each rule type and xpath
        rule_counter = Counter()
        xpath_counter = Counter()
        
        for rule in all_rules:
            rule_key = f"{rule['type']}:{rule['xpath']}"
            rule_counter[rule_key] += 1
            xpath_counter[rule['xpath']] += 1
        
        # Select the most common rules
        learned_rules = []
        for rule_key, count in rule_counter.most_common(5):
            # Find the original rule
            for rule in all_rules:
                if f"{rule['type']}:{rule['xpath']}" == rule_key:
                    learned_rule = rule.copy()
                    learned_rule['frequency'] = count
                    learned_rule['confidence'] = count / len(analyses)
                    learned_rules.append(learned_rule)
                    break
        
        return {
            'category': category_name,
            'patterns_found': True,
            'total_products_analyzed': len(analyses),
            'rules': learned_rules
        }
    
    def extract_with_rules(self, html_content: str, rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract product attributes using learned rules
        
        Args:
            html_content: HTML content
            rules: List of extraction rules
            
        Returns:
            Extracted attributes dictionary
        """
        try:
            tree = html.fromstring(html_content)
        except Exception as e:
            logging.error(f"Failed to parse HTML: {e}")
            return {}
        
        attributes = {}
        
        for rule in rules:
            try:
                xpath = rule['xpath']
                extraction_method = rule['extraction_method']
                
                elements = tree.xpath(xpath)
                
                if not elements:
                    continue
                
                elem = elements[0]  # Take first match
                
                if extraction_method == 'table_key_value':
                    # Extract from table
                    rows = elem.xpath('.//tr')
                    for row in rows:
                        cells = row.xpath('.//th | .//td')
                        if len(cells) == 2:
                            key = self._extract_text(cells[0]).strip()
                            value = self._extract_text(cells[1]).strip()
                            if key and value and self._is_valid_attribute_name(key):
                                # Normalize key
                                normalized_key = self._normalize_attribute_name(key)
                                attributes[normalized_key] = value
                
                elif extraction_method == 'key_value_pairs':
                    # Extract key-value pairs
                    if rule['type'] == 'dl':
                        terms = elem.xpath('.//dt')
                        definitions = elem.xpath('.//dd')
                        for term, definition in zip(terms, definitions):
                            key = self._extract_text(term).strip()
                            value = self._extract_text(definition).strip()
                            if key and value and self._is_valid_attribute_name(key):
                                normalized_key = self._normalize_attribute_name(key)
                                attributes[normalized_key] = value
                    else:
                        # Try to extract from div
                        kv_pairs = self._extract_key_values_from_div(elem)
                        for kv in kv_pairs:
                            if self._is_valid_attribute_name(kv['key']):
                                normalized_key = self._normalize_attribute_name(kv['key'])
                                attributes[normalized_key] = kv['value']
                
            except Exception as e:
                logging.warning(f"Error applying rule {rule.get('xpath')}: {e}")
                continue
        
        return attributes
    
    def _normalize_attribute_name(self, name: str) -> str:
        """
        Normalize attribute name to a standard format
        
        Args:
            name: Raw attribute name
            
        Returns:
            Normalized name
        """
        # Convert to lowercase
        normalized = name.lower().strip()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', '_', normalized)
        
        # Remove special characters except underscore
        normalized = re.sub(r'[^\w\s-]', '', normalized)
        
        # Remove leading/trailing underscores
        normalized = normalized.strip('_')
        
        return normalized

