# Scraping Analysis & Learnings

## Overview

Executed sample scraping for **iPhones** category across 4 websites. Analysis of results reveals specific issues and opportunities for improvement.

---

## Website-by-Website Analysis

### 1. 🔴 Amazon - CRITICAL ISSUE
**Status**: NOT WORKING  
**Products Found**: 0/5  
**Attribute Coverage**: N/A

**Issue**:
- Found 24 product containers using `data-component-type` selector
- But extracted 0 product URLs
- Link extraction logic is failing

**Root Cause**:
```python
# Current logic looks for h2 > a structure
link = container.find('h2')
if link:
    link = link.find('a')
```

**Logs Show**:
```
→ Method 1 (data-component-type): 24 containers
🔗 Extracting product URLs from 24 containers...
   [1] ✗ No link found in container
   [2] ✗ No link found in container
   ...
✓ Extracted 0 product URLs
```

**Fix Needed**:
- Amazon's HTML structure has changed
- Need to update selector to find links within containers
- Should look for `a` tags with specific classes or data attributes

---

### 2. 🟡 Flipkart - GOOD (Needs Minor Improvements)
**Status**: WORKING  
**Products Found**: 5/5  
**Attribute Coverage**: 57.1% (4/7 attributes)

**Successfully Extracted**:
- ✅ brand (Apple)
- ✅ model (iPhone 16, iPhone 16 Pro Max)
- ✅ storage (128, 256)
- ✅ color (Teal, Black, White Titanium, Pink)

**Missing Attributes**:
- ❌ RAM - not in product titles
- ❌ screen_size - not in product titles

**Example Products**:
```
1. Apple iPhone 16 (Teal, 128 GB) - 4/7 attributes
2. Apple iPhone 16 (Black, 256 GB) - 4/7 attributes  
3. Apple iPhone 16 Pro Max (White Titanium, 256 GB) - 4/7 attributes
```

**Improvement Needed**:
- RAM: Need to scrape from product specification table, not just title
- screen_size: Same - need to look in specifications or description
- Current extraction relies only on title text

---

### 3. 🟢 Newegg - EXCELLENT
**Status**: WORKING WELL  
**Products Found**: 5/5  
**Attribute Coverage**: 85.7% (6/7 attributes on average)

**Successfully Extracted**:
- ✅ brand (Apple)
- ✅ model (iPhone 15 Pro Max, iPhone 15, iPhone 14 Plus)
- ✅ storage (256GB, 512GB, 128GB, 1TB)
- ✅ color (Blue, Black, White, Midnight, Pink)
- ✅ condition (New)
- ✅ carrier (Unlocked)

**Missing Attributes**:
- ❌ Only 7th database attribute (probably network/screen_size)

**Example Products**:
```
1. Apple iPhone 15 Pro Max - 1TB - Blue Titanium - Fully Unlock - 5/7 (71.4%)
2. Apple iPhone 15 Pro - 256GB - Black Titanium - Fully Unlocked - 6/7 (85.7%)
3. Apple iPhone 15 Pro Max - 512GB - White Titanium - Fully Unl - 6/7 (85.7%)
```

**Why It Works**:
- Newegg product titles are very descriptive
- Include storage, color, condition, and carrier info
- Good regex patterns in configuration

---

### 4. 🔴 Craigslist - POOR EXTRACTION
**Status**: WORKING (But Poor Quality)  
**Products Found**: 5/5  
**Attribute Coverage**: 14.3% (1/7 attributes)

**Successfully Extracted**:
- ✅ brand (Apple/iPhone) - only attribute extracted

**Missing Attributes**:
- ❌ model - not extracted
- ❌ storage - not extracted
- ❌ color - not extracted
- ❌ condition - not extracted
- ❌ carrier - not extracted

**Example Products (Issues)**:
```
1. Battery Case, for Apple iPhones, 5.5" - 1/7 (14.3%)
   → Not an iPhone, it's an accessory

2. Screen protectors for iphones - 1/7 (14.3%)
   → Not an iPhone, it's an accessory

3. iPhones - 1/7 (14.3%)
   → Generic title, no details

4. iPhones 11 64G unlock 99% battery - 1/7 (14.3%)
   → Has model & storage in title but not extracted

5. WANTED CELLPHONES, IPHONES, SAMSUNG ETC - 1/7 (14.3%)
   → Not even a product for sale!
```

**Root Cause**:
1. **Search Quality**: Getting accessories and "WANTED" ads instead of actual iPhones
2. **Extraction Logic**: Only extracting from title, not checking description
3. **Regex Patterns**: Not matching Craigslist's informal naming style
   - Example: "iPhones 11 64G" should match model="iPhone 11" and storage="64"

---

## Attribute Coverage Summary

| Website    | Products | Avg Coverage | Status |
|------------|----------|--------------|--------|
| Amazon     | 0/5      | N/A          | ❌ Broken |
| Flipkart   | 5/5      | 57.1%        | 🟡 Good |
| Newegg     | 5/5      | 85.7%        | 🟢 Excellent |
| Craigslist | 5/5      | 14.3%        | 🔴 Poor |

**Overall**: 15/20 products scraped (75% success rate)

---

## Required Fixes (Priority Order)

### 🔥 Priority 1: Fix Amazon Link Extraction

**Problem**: 0 products extracted despite finding 24 containers

**Solution**:
```python
# Update amazon_scraper.py link extraction
# Try multiple methods:
1. Find all <a> tags with href containing "/dp/"
2. Check for specific Amazon link classes
3. Look in different parts of container (not just h2)
```

**Implementation**:
- Update `scrape_listing_page()` in `amazon_scraper.py`
- Add fallback link extraction methods
- Test with actual Amazon HTML

---

### 🔥 Priority 2: Improve Craigslist Search & Extraction

**Problem 1 - Search Quality**: Getting accessories, not phones

**Solution**:
- Update search query to be more specific
- Filter results to specific categories (e.g., `/search/moa` for mobile phones)
- Add post-filtering to exclude accessories

**Problem 2 - Attribute Extraction**: Only getting brand

**Solution**:
```python
# Current: Only extracts from title using this pattern:
pattern: "(iPhone\\s*\\d+[a-zA-Z]*(?:\\s*Pro\\s*Max)?(?:\\s*Plus)?)"

# Issue: Doesn't match informal styles like "iPhones 11"
# Fix: Update regex patterns to be more flexible
pattern: "(i?Phone\\s*\\d+[a-zA-Z\\s]*)"  # Matches "iPhone 11" and "iPhones 11"
```

**Also**: Extract from description field, not just title

---

### 🟡 Priority 3: Enhance Flipkart Attribute Extraction

**Problem**: Missing RAM and screen_size (in specifications, not title)

**Solution**:
1. **Option A**: Scrape product specifications table on detail page
2. **Option B**: Add screen_size to title regex patterns if mentioned
3. **Option C**: Use default values for known iPhone models

**Implementation**:
```python
# Add to flipkart_scraper.py
def extract_specifications(self, soup):
    """Extract from specifications table"""
    spec_table = soup.find('table', class_='specifications')
    # Parse table rows...
```

---

## Configuration Updates Needed

### 1. Amazon Config (`iphones_amazon.json`)

**Current Issue**: Link extraction failing

**Update listing_selectors**:
```json
{
  "listing_selectors": {
    "product_container": "div[data-component-type='s-search-result']",
    "product_link": [
      "h2 a",
      "a[href*='/dp/']",
      ".s-product-image-container a",
      "a.a-link-normal"
    ]
  }
}
```

---

### 2. Craigslist Config (`iphones_craigslist.json`)

**Update search_query**:
```json
{
  "search_query": "iPhone -case -screen -charger -cable",
  "search_category": "/search/moa"  // Mobile phones category
}
```

**Update model extraction**:
```json
{
  "model": {
    "method": "regex",
    "pattern": "i?Phones?\\s*(\\d+[a-zA-Z\\s]*(?:Pro\\s*Max|Pro|Plus)?)",
    "source": "title",
    "flags": "IGNORECASE",
    "fallback": {
      "method": "regex",
      "pattern": "i?Phones?\\s*(\\d+[a-zA-Z\\s]*(?:Pro\\s*Max|Pro|Plus)?)",
      "source": "description"
    }
  }
}
```

**Update storage extraction**:
```json
{
  "storage": {
    "method": "regex",
    "pattern": "(\\d+)\\s*[GT]B?",  // Matches "64G", "128GB", "256 GB"
    "source": "title",
    "fallback": {
      "method": "regex",
      "pattern": "(\\d+)\\s*[GT]B?",
      "source": "description"
    }
  }
}
```

---

### 3. Flipkart Config (`iphones_flipkart.json`)

**Add specification selectors**:
```json
{
  "product_selectors": {
    "specifications": [
      {"selector": "table._14CFbK"},
      {"selector": "div._2418kt"}
    ]
  },
  "attributes": {
    "screen_size": {
      "method": "selector",
      "selector": "//tr[contains(., 'Display Size')]/td[2]",
      "fallback": {
        "method": "regex",
        "pattern": "(\\d+\\.?\\d*)\\s*(?:inch|cm|\")",
        "source": "specifications"
      }
    },
    "ram": {
      "method": "selector",
      "selector": "//tr[contains(., 'RAM')]/td[2]",
      "fallback": {
        "method": "regex",
        "pattern": "(\\d+)\\s*GB\\s*RAM",
        "source": "specifications"
      }
    }
  }
}
```

---

## Next Steps

1. **Implement Amazon Fix** ✅ High Priority
   - Update link extraction logic
   - Test with multiple selector methods
   
2. **Implement Craigslist Improvements** ✅ High Priority
   - Update search query and category
   - Improve regex patterns for informal naming
   - Extract from description field
   
3. **Enhance Flipkart** ⚡ Medium Priority
   - Add specification table parsing
   - Extract RAM and screen_size from specs
   
4. **Re-run Scraping** 🔄
   - Test all fixes
   - Verify improved attribute coverage
   - Aim for 70%+ coverage across all websites

5. **Test Other Categories** 📦
   - Men's Clothing
   - Mirrorless Cameras
   - Adjust configurations based on learnings

---

## Success Criteria

**Target Metrics** (After Improvements):
- ✅ Amazon: 80%+ products found, 60%+ attribute coverage
- ✅ Flipkart: 70%+ attribute coverage
- ✅ Newegg: Maintain 85%+ coverage
- ✅ Craigslist: 50%+ attribute coverage, filter out accessories

**Overall Goal**: 70%+ average attribute coverage across all websites

---

## Lessons Learned

1. **Website HTML Changes**: Amazon's structure changed - need regular maintenance
2. **Search Quality Matters**: Craigslist needs better search filtering
3. **Title-Only Extraction Limited**: Need to parse specification tables for complete data
4. **Regex Flexibility**: Informal styles (Craigslist) need looser patterns
5. **Logging is Essential**: Detailed logs made it easy to identify issues

---

**Analysis Date**: December 5, 2024  
**Next Review**: After implementing fixes

