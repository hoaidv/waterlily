
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