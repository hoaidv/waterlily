
# API

## Get one product details

/v1/products/{id}

## Get many product details

/v1/products/?ids=id1,id2,id3

# Helper object

## Product details

This is product detail. It includes:

- Product fields
- Product category object
- List of product variants. Each include
  + id
  + variant_sku
  + price
  + currency
  + quantity
  + attributes
- List of product media
  + url
  + resolution
  + type
  + variant_id (which it describe)
