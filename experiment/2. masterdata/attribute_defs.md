When creating a product, use will choose a category for that product. This chosen category will define that product's attributes.

0. List categories from generated masterdata "categories.csv"
1. For each Category, we define 2-20 attributes relevant to the category.
  + Books have publisher, isbn
  + Clothings have brand (required), color (optional), size (optional)
  + Computers have "CPU", "RAM", "Storage", "Year of Release"...
  + Phones have "Color", "Storage", "Year of Release"
  + ...
  + Furniture
  + Kitchen
  + Bedding
  + ...
  +  

WE NEED TO DO THAT FOR EVERY SINGLE CATEGORY, even with duplication of attributes.

2. Generate attribute defs into a .csv file (check the format below)
3. Check point here for me to check data

Format for attribute defs CSV: 
This is a "merged" version of `attribute_defs`, `categories` 
The format is simple: each row of `categories` is followed by N rows of `attribute_defs`.

```csv
category_id, attribute_name, attribute_display_name, default_value, validation_rules
378472     ,               ,                       ,              ,                 
           , brand         , Brand                 ,              , {}              
           , color         , Color                 ,              , {}              
           , size          , Size                  ,              , {}              
184854     ,               ,                       ,              ,                 
           , cpu           , Cpu                   ,              , {}              
           , ram           , Ram                   ,              , {}              
           , storage       , Storage               ,              , {}              
...
```