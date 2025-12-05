# Execution Guide - Product Scraping System

## Quick Start

The product scraping system is fully implemented and ready to execute. This guide will help you run the scraper and collect product data.

## Prerequisites

1. **Install Python dependencies**:
```bash
cd /Users/hoaidv/Project/waterlily/experiment/3_products
pip install -r requirements.txt
```

2. **Verify MySQL database is running**:
```bash
# The database should be accessible at:
# Host: localhost:3306
# Database: ecommerce
# User: hoaidv
```

3. **Test database connection**:
```bash
cd utils
python3 db_connector.py
```

Expected output:
```
✓ Found 1004 categories
✓ Loaded 3 target categories (iPhones, Men's Clothing, Mirrorless Cameras)
✓ Found 235 distinct attributes
```

## Execution Options

### Option 1: Sample Scrape (Recommended First)

Scrape 5 products per website to verify the system works:

```bash
cd /Users/hoaidv/Project/waterlily/experiment/3_products
./run_scraper.sh --sample
```

Or directly:
```bash
cd scrapers
python3 orchestrator.py --sample
```

**Expected results**:
- ~60 products total (3 categories × 4 websites × 5 products)
- Duration: 10-15 minutes
- Output: `output/scraped_products.json`

### Option 2: Full Scrape

Scrape 10 products per website:

```bash
cd /Users/hoaidv/Project/waterlily/experiment/3_products
./run_scraper.sh --full
```

Or directly:
```bash
cd scrapers
python3 orchestrator.py
```

**Expected results**:
- ~120 products total (3 categories × 4 websites × 10 products)
- Duration: 20-30 minutes
- Output: `output/scraped_products.json`

### Option 3: Resume from Checkpoint

If scraping was interrupted:

```bash
cd /Users/hoaidv/Project/waterlily/experiment/3_products
./run_scraper.sh --resume
```

Or directly:
```bash
cd scrapers
python3 orchestrator.py --resume
```

## Monitoring Progress

The scraper will display real-time progress:

```
============================================================
Scraping category: iPhones (ID: 704898)
Required attributes: 7
============================================================

  Website: amazon
    Found 5 product URLs
    [1/5] Scraping: https://www.amazon.com/...
      ✓ Extracted 6/7 attributes (85.7%)
    [2/5] Scraping: https://www.amazon.com/...
      ✓ Extracted 5/7 attributes (71.4%)
    ...
```

## Output Location

All scraped data is saved to:
```
/Users/hoaidv/Project/waterlily/experiment/3_products/output/scraped_products.json
```

Output structure:
```json
{
  "metadata": {
    "timestamp": "2024-12-05 10:30:00",
    "total_products": 60,
    "categories": ["iPhones", "Men's Clothing", "Mirrorless Cameras"],
    "websites": ["amazon", "flipkart", "newegg", "craigslist"]
  },
  "stats": {
    "categories_processed": 3,
    "products_scraped": 60,
    "products_with_attributes": 58
  },
  "products": [
    {
      "name": "Apple iPhone 14 Pro Max 256GB",
      "price": "$1099.99",
      "url": "https://...",
      "source": "amazon",
      "category_id": 704898,
      "category_name": "iPhones",
      "attributes": {
        "brand": "Apple",
        "model": "iPhone 14 Pro Max",
        "storage": "256GB",
        "color": "Space Black",
        "condition": "New",
        "carrier": "Unlocked"
      },
      "attribute_coverage": 0.857
    },
    ...
  ]
}
```

## Checkpoints

Checkpoints are automatically saved every 50 products to:
```
/Users/hoaidv/Project/waterlily/experiment/3_products/scrapers/scraping_checkpoint.json
```

You can resume from a checkpoint if the scraper is interrupted.

## Data Validation

After scraping, validate the data quality:

```bash
cd /Users/hoaidv/Project/waterlily/experiment/3_products/scrapers
python3 validate_scraped_data.py --products ../output/scraped_products.json
```

Validation report shows:
- Total products and validation rate
- Attribute coverage distribution
- Most frequently missing attributes
- Duplicate products
- Data type errors

Report saved to:
```
/Users/hoaidv/Project/waterlily/experiment/3_products/scrapers/validation_report.json
```

## Troubleshooting

### Issue: SSL/Permission Errors

If you see errors like:
```
SSLError(PermissionError(1, 'Operation not permitted'))
```

**Solution**: Run the scraper directly in your terminal (not in an IDE sandbox):
```bash
cd /Users/hoaidv/Project/waterlily/experiment/3_products/scrapers
python3 orchestrator.py --sample
```

### Issue: No Products Found

If all websites return "✗ No products found":

1. Check your internet connection
2. Some websites (especially Newegg) may block scrapers
3. Try increasing delays in `config/scraping_config.json`:
   ```json
   "rate_limiting": {
     "delay_range": [2.0, 5.0],
     "max_retries": 5
   }
   ```

### Issue: Low Attribute Coverage

If attribute coverage is below 50%:

1. Review the extraction rules in config files
2. Update regex patterns or CSS selectors
3. Add fallback extraction methods

### Issue: Database Connection Failed

If you see database errors:

1. Verify MySQL is running:
   ```bash
   mysql -h localhost -u hoaidv -p -e "USE ecommerce; SHOW TABLES;"
   ```

2. Check credentials in `experiment/mysql-config.json`

### Issue: Categories Not Found

If you see "Category 'X' not found in database":

1. Verify the category exists:
   ```bash
   cd utils
   python3 -c "from db_connector import *; 
   with DatabaseConnection() as c: 
       cats = load_categories(c); 
       print([v['name'] for v in cats.values() if 'iPhone' in v['name'] or 'Clothing' in v['name'] or 'Camera' in v['name']][:10])"
   ```

2. Update category names in `config/scraping_config.json` if they differ

## Performance Tips

### Faster Scraping
- Reduce `delay_range` in config (be respectful of websites)
- Scrape one website at a time
- Use fewer categories

### Better Results
- Increase `max_retries` for flaky connections
- Add more extraction rules in config files
- Review and update CSS selectors if websites change

### Rate Limiting
Current settings (1.5-3.5 second delays) are conservative. You can adjust:

```json
"rate_limiting": {
  "delay_range": [1.0, 2.0],  // Faster but riskier
  "max_retries": 3,
  "timeout": 15
}
```

## Configuration Customization

### Change Products Per Website

Edit `config/scraping_config.json`:
```json
{
  "products_per_category_per_website": 20,  // Full mode
  "sample_mode": {
    "enabled": true,
    "products_per_website": 10  // Sample mode
  }
}
```

### Change Target Categories

Edit `config/scraping_config.json`:
```json
{
  "target_categories": [
    "iPhones",
    "Men's Clothing",
    "Mirrorless Cameras",
    "Laptops"  // Add new category (need to create config files)
  ]
}
```

### Change Craigslist Location

Edit `config/scraping_config.json`:
```json
{
  "craigslist": {
    "location": "newyork"  // or "losangeles", "chicago", etc.
  }
}
```

## Next Steps After Scraping

1. **Validate data**:
   ```bash
   cd scrapers
   python3 validate_scraped_data.py --products ../output/scraped_products.json
   ```

2. **Review attribute coverage**:
   - Check validation report
   - Identify missing attributes
   - Refine config files

3. **Import to database** (optional):
   - Create import script to insert products into MySQL
   - Match attributes to product_def_attributes
   - Generate product variants

4. **Iterate**:
   - Adjust extraction rules based on results
   - Add more categories
   - Expand to more websites

## Example: Complete Workflow

```bash
# 1. Navigate to project
cd /Users/hoaidv/Project/waterlily/experiment/3_products

# 2. Test database connection
cd utils && python3 db_connector.py && cd ..

# 3. Run sample scrape
./run_scraper.sh --sample

# 4. Wait for completion (10-15 minutes)

# 5. Validate results
cd scrapers
python3 validate_scraped_data.py --products ../output/scraped_products.json

# 6. Review output
cat ../output/scraped_products.json | python3 -m json.tool | head -50

# 7. If satisfied, run full scrape
cd ..
./run_scraper.sh --full
```

## Support

For issues or questions:
1. Check the `IMPLEMENTATION_SUMMARY.md` for system architecture
2. Review `README.md` for detailed documentation
3. Check config files for extraction rule examples
4. Review logs in terminal output

## Important Notes

- **Respect Robots.txt**: Some websites may prohibit scraping
- **Rate Limiting**: Be respectful with request frequency
- **Terms of Service**: Review each website's ToS before scraping
- **Data Usage**: Scraped data is for research/development purposes
- **Legal Compliance**: Ensure compliance with local laws and regulations

---

**System Status**: ✅ Ready for execution
**Last Updated**: December 5, 2024

