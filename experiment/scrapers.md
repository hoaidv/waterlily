# GOAL 1

We need to build a scraper for products on amazon website.

# CONTEXT

- Root folder ./3_products
- We need to search products by categories loaded from MySQL, with connection provided
- Total 1000 categories
- The product details HTML is dynamic, and we do not know its significant table and technical detail table, we have to learn while parsing 

# INSTRUCTION


1. Write code to scrape -> analyze web page -> learn extraction -> save config to `./config/amazon_config.json`

- List products by category
- Go to 7-10 product details
- Parse the each product details page and look for product information/attributes, they likely reside within <table> tags
- Write log to a logfile, so I can see the progress `./output/amazon_<category_name>_log.json`
  + Which category
  + How many products listed 
  + Which product detail
  + Found patterns (tables, class, id)
  + Or no pattern found 
  + One log file per category
- Write learned patterns to config file `./config/amazon_config.json`
  + Mapping from category to {} extraction rules
  + Extraction rules
    - Prefer xpath with ID > CLASS > TAG, because xpath is a better match 
    - Regex is OK 
  + This file contains all configs for all categories
- If no information table found
  + you may need to save fragment or save webpage content to `./config/amazon_<category_name>_analyze.txt`
  + analyze it next round of thinking
- Write scraped extracted product information/attributes to `./output/amazon_products.json` 
  so I can see how good the extracted information

2. Next round of thinking: 
- If there are problems, you analyze saved content in `./config/amazon_<category_name>_analyze.txt` deeply learn patterns
- Write learned patterns to config file `./config/amazon_config.json`
  + Prefer xpath with ID > CLASS > TAG, because xpath is a better match 
- Fix code if necessary to scrape again
  + If code is abstracted enough, we may only need to change the xpath/regex patterns

3. When start, choose 3-5 common categories to start 

# EXPECTED RESULT

- scraper code
- config to correctly extract product information/attributes
- content to analyze in next round of thinking by this or another agent , in another run 