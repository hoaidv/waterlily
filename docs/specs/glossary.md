# Glossary

This document defines terms and abbreviations used throughout the Waterlily specification.

## Terms

### A

**API (Application Programming Interface)**  
A set of protocols and tools for building software applications. In this project, refers to the REST endpoints exposed by the Waterlily service.

**Attribute**  
A property or characteristic of a product or variant. Stored as JSON key-value pairs. Examples: color, size, weight, material.

### B

**Batch Request**  
A single API request that retrieves multiple resources. The Waterlily batch endpoint accepts up to 50 product IDs per request.

**Benchmark**  
A standardized test to measure and compare system performance. Waterlily benchmarks measure throughput (RPS) and latency under varying loads.

**Benchmark Context**  
The combination of environmental factors under which a benchmark runs: platform, database type, number of instances, and access pattern.

### C

**CCU (Concurrent Users)**  
The number of simultaneous connections or users making requests to the system. In wrk, controlled by the `--connections` flag.

**Connection Pool**  
A cache of database connections maintained for reuse, reducing the overhead of establishing new connections. HikariCP manages the pool for Waterlily.

**CRUD**  
Create, Read, Update, Delete - the four basic operations for persistent storage. Waterlily implements only Read operations.

### H

**HikariCP**  
A high-performance JDBC connection pool library used in the Waterlily application.

### I

**InnoDB**  
MySQL's default storage engine, supporting transactions, foreign keys, and row-level locking. Used by Waterlily for all tables.

### J

**JDBC (Java Database Connectivity)**  
A Java API for connecting to relational databases. Waterlily uses raw JDBC for database access.

**JSON (JavaScript Object Notation)**  
A lightweight data interchange format. Used for API request/response bodies and storing flexible attributes in the database.

### K

**Ktor**  
A Kotlin framework for building asynchronous servers and clients. The web framework used by Waterlily.

### L

**Latency**  
The time between sending a request and receiving a response. Measured in milliseconds (ms). Key metrics include p50, p95, p99, and average.

**Lua**  
A lightweight scripting language. Used to write custom scripts for the wrk benchmark tool.

### M

**Media**  
Images, videos, or other visual content associated with a product. Stored as URLs in the product_media table.

### N

**NFR (Non-Functional Requirement)**  
A requirement that specifies criteria for system operation rather than specific behaviors. Examples: performance, scalability, reliability.

### P

**p50, p95, p99 (Percentiles)**  
Statistical measures of latency distribution. p95 = 95% of requests completed within this time. Critical for understanding real-world user experience.

**Primary Key (PK)**  
A unique identifier for each row in a database table. Waterlily uses UUIDs as primary keys.

**Product**  
The main business entity representing a consumer good. Contains name, description, attributes, and references to variants, media, and category.

**Product Detail**  
A composite view of a product including its base fields, category information, all variants, and all media. The primary response format for product APIs.

### R

**RPS (Requests Per Second)**  
A measure of throughput - how many requests the system can process per second. Also called TPS (Transactions Per Second).

**REST (Representational State Transfer)**  
An architectural style for web services. Waterlily exposes a REST API with JSON payloads.

### S

**SKU (Stock Keeping Unit)**  
A unique identifier for a product or variant, used for inventory management. Waterlily generates `base_sku` for products and `variant_sku` for variants.

**Source**  
The origin of product data. Currently supports "AMZ" (Amazon). Stored with `source`, `source_sku`, and `source_url` fields.

### T

**TPS (Transactions Per Second)**  
Equivalent to RPS in this context. A measure of system throughput.

**Throughput**  
The rate at which requests are processed. Measured in RPS or TPS.

### U

**UUID (Universally Unique Identifier)**  
A 128-bit identifier used for primary keys. Format: `550e8400-e29b-41d4-a716-446655440000`. Generated randomly by the application.

### V

**Variant**  
A variation of a base product, differing by attributes like size, color, or configuration. Has its own SKU, price, and quantity.

### W

**wrk**  
A modern HTTP benchmarking tool capable of generating significant load. Used with Lua scripts to benchmark Waterlily APIs.

---

## Abbreviations Reference

| Abbreviation | Full Form |
|--------------|-----------|
| API | Application Programming Interface |
| CCU | Concurrent Users |
| CRUD | Create, Read, Update, Delete |
| FK | Foreign Key |
| GB | Gigabyte |
| HTTP | Hypertext Transfer Protocol |
| JDBC | Java Database Connectivity |
| JSON | JavaScript Object Notation |
| JVM | Java Virtual Machine |
| KB | Kilobyte |
| MB | Megabyte |
| ms | Milliseconds |
| NFR | Non-Functional Requirement |
| PK | Primary Key |
| REST | Representational State Transfer |
| RPS | Requests Per Second |
| SKU | Stock Keeping Unit |
| SQL | Structured Query Language |
| TPS | Transactions Per Second |
| UK | Unique Key |
| URL | Uniform Resource Locator |
| UUID | Universally Unique Identifier |
