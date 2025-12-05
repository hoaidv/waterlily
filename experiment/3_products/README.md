# Product Scraping System

A comprehensive web scraping framework for extracting product information and attributes from multiple e-commerce websites.

## Features

- **Multi-Website Support**: Scrapes from Amazon, Flipkart, Newegg, and Craigslist
- **Configurable Attribute Extraction**: Uses JSON configuration files for flexible attribute extraction
- **Database Integration**: Loads categories and attributes from MySQL database
- **Rate Limiting**: Respects website policies with configurable delays
- **Checkpoint System**: Resume interrupted scrapes
- **Attribute Validation**: Validates extracted attributes against database schema

## Architecture

```
3_products/
├── config/                          # Configuration files
│   ├── scraping_config.json        # Global settings
│   └── {category}_{website}.json  # Category-website specific configs
├── scrapers/                        # Scraper modules
│   ├── base_scraper.py             # Base scraper framework
│   ├── amazon_scraper.py           # Amazon-specific scraper
│   ├── flipkart_scraper.py         # Flipkart-specific scraper
│   ├── newegg_scraper.py           # Newegg-specific scraper
│   ├── craigslist_scraper.py       # Craigslist-specific scraper
│   ├── attribute_extractor.py      # Attribute extraction engine
│   ├── orchestrator.py             # Main orchestrator
│   └── validate_scraped_data.py    # Data validation
├── utils/                           # Utility modules
│   └── db_connector.py             # Database connection utilities
└── output/                          # Scraped data output

```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure MySQL connection in `../mysql-config.json`

## Usage

### Sample Scrape (5 products per website)
```bash
./run_scraper.sh --sample
```

### Full Scrape (10 products per website)
```bash
./run_scraper.sh --full
```

### Resume from Checkpoint
```bash
./run_scraper.sh --resume
```

### Direct Python Usage
```bash
cd scrapers
python3 orchestrator.py --sample          # Sample mode
python3 orchestrator.py                   # Full mode
python3 orchestrator.py --resume          # Resume
```

## Configuration

### Global Configuration
Edit `config/scraping_config.json`:
- `target_categories`: List of categories to scrape
- `websites`: List of websites to scrape
- `products_per_category_per_website`: Number of products per website (full mode)
- `sample_mode.products_per_website`: Number of products per website (sample mode)
- `rate_limiting`: Delay and retry settings
- `checkpoint`: Checkpoint settings

### Category-Website Configuration
Each `config/{category}_{website}.json` file defines:
- Search query for the category
- HTML selectors for product listing
- HTML selectors for product details
- Attribute extraction rules (regex patterns, CSS selectors, fallbacks)

## Target Categories

1. **iPhones**: Smartphone products
   - Attributes: brand, model, storage, color, condition, carrier

2. **Men's Clothing**: Apparel products
   - Attributes: brand, clothing_type, size, color, material, fit

3. **Mirrorless Cameras**: Camera equipment
   - Attributes: brand, model, megapixels, sensor_type, video_capability, kit_type

## Output

Scraped data is saved to `output/scraped_products.json`:
```json
{
  "metadata": {
    "timestamp": "2024-01-01 12:00:00",
    "total_products": 150,
    "categories": ["iPhones", "Men's Clothing", "Mirrorless Cameras"],
    "websites": ["amazon", "flipkart", "newegg", "craigslist"]
  },
  "stats": {
    "categories_processed": 3,
    "products_scraped": 150,
    "products_with_attributes": 145
  },
  "products": [...]
}
```

## Data Validation

Validate scraped data:
```bash
cd scrapers
python3 validate_scraped_data.py --products ../output/scraped_products.json
```

## Extending the System

### Adding a New Website
1. Create `scrapers/{website}_scraper.py` inheriting from `BaseScraper`
2. Implement required methods: `get_website_name()`, `build_search_url()`, `scrape_listing_page()`, etc.
3. Add website to `config/scraping_config.json`
4. Create configuration files for each category

### Adding a New Category
1. Add category to database
2. Create configuration files: `config/{category}_{website}.json` for each website
3. Add category name to `config/scraping_config.json`

## Error Handling

- Automatic retries with exponential backoff
- Rate limiting to avoid blocking
- Checkpoint system for recovery
- Detailed error logging

## Notes

- Respect website terms of service
- Use appropriate rate limiting
- Some websites may block scrapers (especially Newegg)
- Craigslist results vary by location (default: sfbay)

