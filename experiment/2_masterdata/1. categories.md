Let's generate 1000 categories directly to `categories.csv` file.

1. Which categories?
- Think of high-level categories: Clothing, Electronics, Household, Books
- Think of lower level categories: 
  + Clothing -> Men's, Women's 
  + Men's -> Shirts, Sweaters, T-shirts, Trousers, Pants...
  + Women's -> ...

2. Some minor details
  - Column id, randomly generate id in range 100000-999999
  - Ignore column `product_def_id` as we did not define it yet, we will define it later.
3. Generate flat list of categories into a .csv file
4. Check point here for me to check data
5. When it's OK, insert the .csv content into MySQL
