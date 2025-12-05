
# Base schema 

- We keep this simple by not introducing seller entity yet
- We may further define an attribute's datatype by adding options 
  (single select, multi select...), but let's keep it simple here.
- We may also remove this table, and allow product definition attributes 
  to define all attribute names, data types and display name
  to make it even more flexible, but let's keep it simple here for demonstration purpose.

## Product

Name: `products`
Role: Main product entity
Who use it: Sellers

- id: BIGINT, This is generated randomly by application, not incremental
- base_sku: "C-2025-TSHIRT", this is user-defined
- name: 512
- status: ACTIVE, INACTIVE
- created_at: timestamp
- category_id -> categories(id)
- product_def_id -> product_defs(id)
- attributes: json

## Category

Name: `categories`
Role: Categorize the product

- id: INT; This is generated randomly [100000, 999999] by application, not incremental
- name
- description
- product_def_id -> product_defs(id)


## Product definition

Name: `product_defs`
Role: Define how to dictate a product's attributes. This refers to a list of attributes a product must have.
Who use it: Moderator

- id: INT
- name: 512

## Product definition attributes

Name: `product_def_attributes`
Role: List of attributes a product must have
Who use it: Moderator

- id
- product_def_id -> product_defs(id)
- name
- datatype
- display_name
- default_value: varchar (application convert this to proper datatype)
- validation_rules: json; default {}
  + example 1: { is_required: true }
  + example 2: { min: 1000; max: 100000 }
  + example 3: { equal: "3 * some_other_attribute" }
- UNIQUE(product_def_id, name)

## Product variant attributes

Name: `product_variant_defs`
Role: Maps products to which attributes are used for creating variants
      This is dynamic and bounds to the particular product.
      This table is almost the same as "Product definition attributes", with 
      a the main difference: This table defines attributes of variants, while the 
      "Product definition attributes" defines attributes of base products.
Who use it: Seller

- product_id -> products(id)
- attribute_name
  + e.g. color, size
- order: 1,2... in the list of variant attributes

## Product variants

Name: product_variants
Role: Actual product variants (combinations of attribute values)

- id: This is generated randomly by application, not incremental
- product_id -> products(id)
- variant_sku: C-2025-TSHIRT-BEIGE-XL, C-2025-TSHIRT-BEIGE-XXL, C-2025-TSHIRT-RED-M...
- quantity
- price
- attributes: json
  + e.g. { color: Beige, size: XL }, { color: Red, size: M }

