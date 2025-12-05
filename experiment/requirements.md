# What will we do

Let's test performance of MySQL with "real" data volume: 

+ Size:       100 000
+ Size:     1 000 000 
+ Size:    10 000 000
+ Size:   100 000 000
+ Size: 1 000 000 000

# Prepare Data

## Execution overview

1. Convert above description to MySQL to execute. I will revise the generated script and execute it myself. 
  Let's name the file "base-schema.sql" and put it in "./experiment/" folder
2. We generate sample data
  - 1000 categories
  - 100 attribute defs
  - 100 product defs, each defines about 5 to less than 30 attribute defs
  - 1 000 000 products, each with 0 - 3 variant attributes, result in 1-8 variants
    + We may change this number for subsequence benchmark

## Some details

#### How to generate products

This is big, we need to generate some kotlin script in the project, to generate products 
to make the generation reliable and repeatable. 

The generated kotlins script will not use "Exposed" library or any DAO. 
Instead, when a product data is ready, it will generate MySQL statement 
from a prepared statement to insert product.

- Product names are category-specific. 
- We have 1000 categories, to generate 1 000 000 products let's generate 100-10000 products per categories
- Use the category name, we search for products across the internet
  + some e-commerce websites
  + some marketing, branding blogs
  + any particular brand's websites
  + .. other kinds of websites
- In each website, look for product names belong to that particular category
- When building product need to make sure that product has relevant attributes defined by `product_defs`
- Stop at first 10000 products before continue, so I can verify the data.
- Then continue with the rest with my permission.


# Prepare Code

Before going to API part, let's use https://www.jetbrains.com/exposed/ and 
generate DAO layer for above entities.
We will use this layer to generate and insert products later.

# API

+ Leave this and actual logic for later.

# Benchmark

+ Leave this benchmark script for later.