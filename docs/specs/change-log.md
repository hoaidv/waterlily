
# 03/02/2026 - hoaidv

Cache for ProductDetail per ID

- Cache ProductDetail so we save time querying 
- Choose a library for caching locally
- We will not cache all products in memory
- Products access pattern
  + Some products will be accessed more frequently than others
  + Distribution: Zipfian with exponent s=4, N=10M products (count from DB).
- Cache design
  + Use LRU strategy to evict cache 
  + No cache invalidation yet 
  + Capacity 1M entries
  + Suggest me a cache warmup strategy 
    * e.g. no strategy, let the application warmup for 2 minutes itself base on access
    * e.g. save cache statistics per product, and cache products with most access
    * **Question:** Which cache warmup strategy to implement (no warmup / passive warmup / stats-based)?
    * **Answer:** No warmup – cache fills naturally on first access.
- Metrics
  + Requests per Second
  + Cache hits per Second
  + Cache hits (%)
  + DB hits per Second
- Benchmark this by:
  + Randomly load N=10M product IDs into a file
  + Simulating the product access pattern in benchmark script

# 03/02/2026 - hoaidv

Real-time Monitoring with Prometheus and Grafana

## Data Collection

- Library: Micrometer with Prometheus registry
- Dependencies to add:
  + `io.ktor:ktor-server-metrics-micrometer` (Ktor plugin)
  + `io.micrometer:micrometer-registry-prometheus`
- Expose metrics at `GET /metrics` in Prometheus format (for external scraper)
- Prometheus server already running. No need to do anything.

## Metrics to Collect

The following prometheus metrics are expected at the `GET /metrics` endpoint 

- JVM Vitals (automatic via Micrometer)
- Ktor Server Vitals (automatic via ktor-server-metrics-micrometer)
- Cache Metrics (custom counters)
  - `product_cache_requests_total` - total requests to cache
  - `product_cache_hits_total` - cache hits
  - `product_db_hits_total` - database hits (cache misses)

### Cache Metrics - Prometheus Queries

| Metric | PromQL Query |
|--------|-------------|
| Cache Hits/sec | `rate(product_cache_hits_total[1m])` |
| DB Hits/sec | `rate(product_db_hits_total[1m])` |
| Cache Hit Rate (%) | `100 * rate(product_cache_hits_total[1m]) / rate(product_cache_requests_total[1m])` |

### Request Metrics

Request Rate

```promQL
sum(rate(ktor_http_server_requests_seconds_count{instance="localhost:8080"}[30s])) by (method, route, status)
```

Response Time

```promQL
sum by (route, method, status) (
    rate(ktor_http_server_requests_seconds_sum{instance="localhost:8080"}[30s])
)
/
sum by (route, method, status) (
    rate(ktor_http_server_requests_seconds_count{instance="localhost:8080"}[30s])
)
```

## Dashboards

- Grafana server already running, no need to do anything
  - JVM Dashboard: Use **4701** (JVM Micrometer)
  - Ktor Dashboard: Build it yourself.

# 03/02/2026 - hoaidv

Adding cache warmup
- Warmup the cache by loading first x millions products from a file of product IDs
- Number of products to load is = Cache limit
- Warmup the cache before declaring the app is ready
- Report warming progress by percent(%) and number of loaded products
- Product IDs are provided via a file path
  + In production, it is a file in a mounted volume.
  + In local, it is provided as `product_ids.txt` (full path)

# 04/02/2026 - hoaidv

Add a new metrics: Number of concurrent user using the server.