
# CONTEXT

When creating a product, use will choose a category for that product. 
This chosen category will define that product's attributes. 

Therefore, with each category we define 2-20 relevant attributes 
+ Books have publisher, isbn
+ Clothings have brand (required), color (optional), size (optional)
+ Computers have "CPU", "RAM", "Storage", "Year of Release"...
+ Phones have "Color", "Storage", "Year of Release"
+ ...
+ Furniture
+ Kitchen
+ Bedding
+ ...
+ Fishing
+ ...
+ Camera have resolution (24MP), sensor (DIGIC10), model (Z6 II)...
+ Camera accessories
+ ...

# INSTRUCTIONS

Let's create category-attributes mapping for @categories.csv

0. List categories (> 1000) from generated masterdata "categories.csv"
1. We generate as many attributes per category as possible.
   Save to `categories_attributes.py`.
- I want this category-attributes to be fine-grain, 
  by really THINK about attributes per category, 
  not pre-group them with terms.
- DO NOT match category name & desc for attributes, 
  as this pre-matching strategy will always
  limit the number of category-specific attribute.

```python
CATEGORY_ATTRIBUTES = [
  {
    # Batteries
    'id': 102105,   
    'attributes': [
      # name, datatype, display_name
      ('voltage', 'STRING', 'Voltage per cell'),
      ('cells', 'NUMBER', 'Number of battery cells'),
      ...
    ]    
  },
  {
    ...
  }
]
```

2. Checkpoint here to review the file.
