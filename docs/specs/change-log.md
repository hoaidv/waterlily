
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

# 03/02/2026 - hoaidv

## Cache Size Formula for Target Hit Rate (Zipfian Distribution)

### Problem

Given Zipfian distribution with parameters:
- `s` = Zipfian exponent (e.g., s=1)
- `N` = Total number of products (e.g., N=10,000,000)

Find cache size `C` needed to achieve target hit rate `X%`.

### Zipfian Probability

The probability of accessing item with rank `k` is:

```
P(k) = (1/k^s) / H(N,s)
```

Where `H(N,s)` is the generalized harmonic number: `H(N,s) = sum(1/i^s) for i=1 to N`

### Cache Hit Rate Formula

If we cache the top `C` items (sorted by rank/popularity), the hit rate is:

```
Hit_Rate = H(C,s) / H(N,s)
```

### Formula for s=1 (Standard Zipf's Law)

For s=1, the harmonic number approximates to: `H(n) ≈ ln(n) + γ`

Where `γ ≈ 0.5772` (Euler-Mascheroni constant)

**Cache size for target hit rate X:**

```
C = exp(X × (ln(N) + γ) - γ)
```

Or equivalently:

```
C = N^X × e^((X-1) × γ)
```

### Theoretical vs Empirical Results (N=10,000,000, s=1)

**Theoretical formula (using harmonic approximation):**
```
Hit_Rate = H(C) / H(N) = (ln(C) + γ) / (ln(N) + γ)
```

**Empirical observation:** 2M cache → 85% hit rate

The theoretical formula overestimates hit rate. Using empirical calibration:

| Target Hit Rate | Cache Size (C) | % of Total | Notes |
|-----------------|----------------|------------|-------|
| 85%             | 2,000,000      | 20%        | Empirical baseline |
| 90%             | ~3,000,000     | 30%        | Estimated |
| 95%             | ~5,000,000     | 50%        | Estimated |
| 99%             | ~9,000,000     | 90%        | Estimated |

### Inverse Formula: Cache Size for Target Hit Rate

Given empirical data point (C₀=2M, X₀=85%), estimate cache size for target X:

```
C = C₀ × (ln(N)/ln(C₀))^((X - X₀)/(1 - X₀))
```

Or use the ratio of harmonic numbers directly:

```
C = exp((X/X₀) × (ln(C₀) + γ) - γ)
```

### Example: Calculate cache size for 95% hit rate

Given: 2M cache → 85% hit rate

```
# Method: Scale based on harmonic ratio
H(2M) / H(10M) = 0.85  (empirical)
H(10M) = H(2M) / 0.85 = (ln(2M) + 0.5772) / 0.85 = 15.086 / 0.85 = 17.75

For 95%:
H(C) = 0.95 × 17.75 = 16.86
ln(C) = 16.86 - 0.5772 = 16.28
C = e^16.28 ≈ 5,300,000
```

**Conclusion:** To achieve 95% cache hit rate, cache ~5.3M products (53% of total).

### Implementation Note

The `product_ids.txt` file should contain product IDs sorted by popularity (most popular first). Cache warmup loads the first `C` IDs from this file, where `C` = cache maxSize.