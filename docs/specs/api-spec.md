# API Specification

This document defines the REST API contract for the Waterlily product service.

## Base URL

```
http://localhost:8080/api/v1
```

## Content Type

All requests and responses use `application/json`.

---

## Endpoints

### GET Product by ID

Retrieve a single product with its complete details.

```
GET /api/v1/products/{id}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Product UUID |

#### Response

**200 OK**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "baseSku": "WL-PROD-001",
  "name": "Example Product",
  "description": "Product description text",
  "features": ["Feature 1", "Feature 2"],
  "status": "ACTIVE",
  "source": "AMZ",
  "sourceSku": "B08N5WRWNW",
  "sourceUrl": "https://amazon.com/dp/B08N5WRWNW",
  "attributes": {
    "color": "Black",
    "material": "Aluminum"
  },
  "category": {
    "id": "cat-001",
    "name": "Electronics",
    "description": "Electronic devices and accessories"
  },
  "variants": [
    {
      "id": "var-001",
      "variantSku": "WL-PROD-001-BLK-S",
      "quantity": 100,
      "price": 29.99,
      "currency": "USD",
      "attributes": {
        "size": "Small"
      }
    }
  ],
  "media": [
    {
      "id": "media-001",
      "type": "IMAGE",
      "resolution": "high_res",
      "url": "https://example.com/images/product-001.jpg",
      "variantId": null
    }
  ]
}
```

**404 Not Found**

```json
{
  "error": "NOT_FOUND",
  "message": "Product not found",
  "productId": "550e8400-e29b-41d4-a716-446655440000"
}
```

**400 Bad Request**

```json
{
  "error": "INVALID_REQUEST",
  "message": "Invalid product ID format"
}
```

**500 Internal Server Error**

```json
{
  "error": "INTERNAL_ERROR",
  "message": "An unexpected error occurred"
}
```

---

### GET Products Batch

Retrieve multiple products by their IDs in a single request.

```
POST /api/v1/products/batch
```

#### Request Body

```json
{
  "ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "550e8400-e29b-41d4-a716-446655440001"
  ]
}
```

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| ids | string[] | Yes | 1-50 items | Array of product UUIDs |

#### Response

**200 OK**

```json
{
  "products": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "baseSku": "WL-PROD-001",
      "name": "Example Product 1",
      "description": "...",
      "category": { "..." },
      "variants": [ "..." ],
      "media": [ "..." ]
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "baseSku": "WL-PROD-002",
      "name": "Example Product 2",
      "description": "...",
      "category": { "..." },
      "variants": [ "..." ],
      "media": [ "..." ]
    }
  ],
  "count": 2
}
```

**400 Bad Request** (too many IDs)

```json
{
  "error": "INVALID_REQUEST",
  "message": "Maximum 50 product IDs allowed per request",
  "requestedCount": 75,
  "maxAllowed": 50
}
```

**400 Bad Request** (empty list)

```json
{
  "error": "INVALID_REQUEST",
  "message": "At least one product ID is required"
}
```

---

### Health Check

Verify service availability.

```
GET /health
```

#### Response

**200 OK**

```json
{
  "status": "ok",
  "timestamp": "2026-01-28T10:30:00Z"
}
```

---

## Data Models

### ProductDetail

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | string | No | Product UUID |
| baseSku | string | No | Generated SKU |
| name | string | No | Product name |
| description | string | Yes | Product description (text/html/json) |
| features | string[] | Yes | List of product features |
| status | string | No | Product status (ACTIVE, INACTIVE, etc.) |
| source | string | No | Data source (AMZ, etc.) |
| sourceSku | string | Yes | Original SKU from source |
| sourceUrl | string | Yes | Original product URL |
| attributes | object | Yes | Product-specific attributes as JSON |
| category | CategoryDetail | No | Associated category |
| variants | VariantDetail[] | No | Product variants (may be empty) |
| media | MediaDetail[] | No | Product media (may be empty) |

### CategoryDetail

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | string | No | Category UUID |
| name | string | No | Category name |
| description | string | Yes | Category description |

### VariantDetail

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | string | No | Variant UUID |
| variantSku | string | No | Variant SKU |
| quantity | integer | No | Available quantity |
| price | decimal | No | Variant price |
| currency | string | No | Currency code (USD, EUR, etc.) |
| attributes | object | Yes | Variant-specific attributes |

### MediaDetail

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | string | No | Media UUID |
| type | string | No | Media type (IMAGE, VIDEO) |
| resolution | string | No | Resolution descriptor |
| url | string | No | Media URL |
| variantId | string | Yes | Associated variant (if any) |

### ErrorResponse

| Field | Type | Description |
|-------|------|-------------|
| error | string | Error code |
| message | string | Human-readable error message |

---

## HTTP Status Codes Summary

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid input, too many IDs, malformed JSON |
| 404 | Not Found | Product ID does not exist |
| 500 | Internal Server Error | Unexpected server error |
