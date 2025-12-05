Starting from the generated @generate_attribute_defs.py we will modify it to create product_defs, product_def_attributes and binding categories to `product_def`.

1. In the function get_attributes_for_category, you did the great job clustering attributes into groups.
2. Now modify this function, for each group
2.1. create one `product_defs` object then 
2.2. create corresponding `product_def_attributes` objects
2.3. finally we have a greate lookup table
     From `product_defs` To
        + many `product_def_attributes`
        + many keywords to match categories with this `product_defs` 

2.4. CHECKPOINT here for me to review.

3. Insert `product_defs` to MySQL
4. Insert `product_def_attributes` to MySQL
5. Match categories with `product_defs`, update its `product_def_id` in MySQL
