#!/usr/bin/env python3
"""
Base scraper class with common functionality for all website scrapers
"""

import json
import os
import time
import random
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import logging


class BaseScraper(ABC):
    """Base class for all website scrapers"""
    
    def __init__(self, config: Dict[str, Any], output_dir: str = "./output"):
        """
        Initialize base scraper
        
        Args:
            config: Configuration dictionary
            output_dir: Directory for output files
        """
        self.config = config
        self.output_dir = output_dir
        self.config_dir = os.path.join(os.path.dirname(output_dir), "config")
        self.analyze_dir = os.path.join(os.path.dirname(output_dir), "analyze")
        
        # Create output directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Rate limiting settings
        self.rate_limit = config.get('rate_limiting', {})
        self.delay_range = self.rate_limit.get('delay_range', [1.5, 3.5])
        self.max_retries = self.rate_limit.get('max_retries', 3)
        self.timeout = self.rate_limit.get('timeout', 15)
        
        # Statistics
        self.stats = {
            'categories_processed': 0,
            'products_scraped': 0,
            'products_with_attributes': 0,
            'errors': 0
        }
    
    @abstractmethod
    def get_website_name(self) -> str:
        """Return the website name (e.g., 'amazon', 'flipkart')"""
        pass
    
    @abstractmethod
    def search_products_by_category(self, category: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for products in a given category
        
        Args:
            category: Category data from database
            
        Returns:
            List of product data dictionaries
        """
        pass
    
    @abstractmethod
    def scrape_product_details(self, product_url: str, category: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrape details from a product page
        
        Args:
            product_url: URL of the product page
            category: Category data for context
            
        Returns:
            Dictionary containing product details and attributes
        """
        pass
    
    def wait_between_requests(self):
        """Wait a random amount of time between requests"""
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        time.sleep(delay)
    
    def save_log(self, category_name: str, log_data: Dict[str, Any]):
        """
        Save log file for a category
        
        Args:
            category_name: Name of the category
            log_data: Log data to save
        """
        safe_name = self._sanitize_filename(category_name)
        website = self.get_website_name()
        log_file = os.path.join(self.output_dir, f"{website}_{safe_name}_log.json")
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Saved log to {log_file}")
    
    def save_analyze_content(self, category_name: str, content: str, suffix: str = ""):
        """
        Save content for manual analysis
        
        Args:
            category_name: Name of the category
            content: HTML or text content to analyze
            suffix: Optional suffix for the filename
        """
        safe_name = self._sanitize_filename(category_name)
        website = self.get_website_name()
        filename = f"{website}_{safe_name}_analyze{suffix}.txt"
        analyze_file = os.path.join(self.analyze_dir, filename)
        
        with open(analyze_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logging.info(f"Saved content for analysis to {analyze_file}")
        return analyze_file
    
    def save_config(self, config_data: Dict[str, Any]):
        """
        Save extraction configuration
        
        Args:
            config_data: Configuration data to save
        """
        website = self.get_website_name()
        config_file = os.path.join(self.config_dir, f"{website}_config.json")
        
        # Load existing config if it exists
        existing_config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
        
        # Merge with new config
        existing_config.update(config_data)
        
        # Save merged config
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(existing_config, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Saved config to {config_file}")
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load extraction configuration if it exists
        
        Returns:
            Configuration dictionary or empty dict
        """
        website = self.get_website_name()
        config_file = os.path.join(self.config_dir, f"{website}_config.json")
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {}
    
    def save_products(self, products: List[Dict[str, Any]]):
        """
        Append products to the output file
        
        Args:
            products: List of product dictionaries
        """
        website = self.get_website_name()
        products_file = os.path.join(self.output_dir, f"{website}_products.json")
        
        # Load existing products if file exists
        existing_products = []
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                try:
                    existing_products = json.load(f)
                except json.JSONDecodeError:
                    existing_products = []
        
        # Append new products
        existing_products.extend(products)
        
        # Save all products
        with open(products_file, 'w', encoding='utf-8') as f:
            json.dump(existing_products, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Saved {len(products)} products to {products_file} (total: {len(existing_products)})")
    
    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a string to be used as a filename
        
        Args:
            name: String to sanitize
            
        Returns:
            Sanitized string
        """
        # Replace spaces and special characters
        safe = name.replace(' ', '_').replace("'", '').replace('"', '')
        safe = ''.join(c for c in safe if c.isalnum() or c in ('_', '-'))
        return safe.lower()
    
    def get_stats(self) -> Dict[str, Any]:
        """Return scraping statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset statistics counters"""
        self.stats = {
            'categories_processed': 0,
            'products_scraped': 0,
            'products_with_attributes': 0,
            'errors': 0
        }

