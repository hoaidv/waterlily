# What will we do

+ Size:       100 000
+ Size:     1 000 000 
+ Size:    10 000 000
+ Size:   100 000 000
+ Size: 1 000 000 000


We start with 1 000 000 products first.

## Relationship refinements
- 1000 categories
- 100 attribute defs
- 100 product defs, each defines about 5 to less than 30 attribute defs
- 1 000 000 products, each with 0 - 3 variant attributes, result in 1-8 variants
  + We may change this number for subsequence benchmark

## How to do
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
