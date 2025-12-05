# CONTEXT

We already have the mapping from category to attributes in @category_attributes.py
These categories are very product specific, therefore this mapping
is also a very good the product_defs -> product_def_attributes mapping.
Now we use these categories to create 1 product def per category.

# INSTRUCTION

1. Read the @category_attributes.py and use this mapping to create `product_defs`.
- 1 category ~ 1 `product_defs`
- Generate random id for each `product_defs`
2. For each `product_defs`, create corresponding `product_def_attributes`.
- No need to generate temporary `product_defs.csv` file or `product_defs.py` file.

3. Link categories.product_def_id with `product_defs`

May need to clear old `product_defs`, `product_def_attributes` data 
together with old `categories`.`product_def_id` link

Use the mysql connection provided @mysql-config.json