package com.discovery.cache

import com.discovery.model.ProductDetail
import com.discovery.repository.ProductRepository
import com.github.benmanes.caffeine.cache.Cache
import com.github.benmanes.caffeine.cache.Caffeine
import io.micrometer.core.instrument.Counter
import io.micrometer.core.instrument.MeterRegistry

/**
 * LRU cache for ProductDetail by ID with metrics tracking.
 * 
 * Design decisions:
 * - Cache only non-null results (products that exist)
 * - Null results (product not found) are not cached to allow retry
 * - No cache invalidation (as per spec)
 * - No warmup strategy - cache fills naturally on first access
 * - Metrics exposed via Micrometer for Prometheus scraping
 */
class ProductDetailCache(
    private val repository: ProductRepository,
    private val meterRegistry: MeterRegistry,
    maxSize: Long = DEFAULT_MAX_SIZE
) {
    companion object {
        const val DEFAULT_MAX_SIZE = 1_000_000L
    }

    private val cache: Cache<Long, ProductDetail> = Caffeine.newBuilder()
        .maximumSize(maxSize)
        .build()

    // Micrometer counters (automatically exported as _total for Prometheus)
    private val requestsCounter: Counter = Counter.builder("product_cache_requests")
        .description("Total requests to product cache")
        .register(meterRegistry)
    
    private val cacheHitsCounter: Counter = Counter.builder("product_cache_hits")
        .description("Cache hits")
        .register(meterRegistry)
    
    private val dbHitsCounter: Counter = Counter.builder("product_db_hits")
        .description("Database hits (cache misses)")
        .register(meterRegistry)

    private val startTimeMs = System.currentTimeMillis()

    /**
     * Get product by ID, using cache when available.
     * On cache miss, fetches from repository and caches non-null results.
     */
    suspend fun getById(id: Long): ProductDetail? {
        requestsCounter.increment()

        // Check cache first
        val cached = cache.getIfPresent(id)
        if (cached != null) {
            cacheHitsCounter.increment()
            return cached
        }

        // Cache miss - fetch from database
        dbHitsCounter.increment()
        val product = repository.findById(id)

        // Cache non-null results only
        if (product != null) {
            cache.put(id, product)
        }

        return product
    }

    /**
     * Get current cache statistics.
     */
    fun getStats(): CacheStats {
        val requests = requestsCounter.count().toLong()
        val hits = cacheHitsCounter.count().toLong()
        val dbHits = dbHitsCounter.count().toLong()
        val uptimeMs = System.currentTimeMillis() - startTimeMs

        return CacheStats(
            requestsTotal = requests,
            cacheHitsTotal = hits,
            dbHitsTotal = dbHits,
            cacheHitPercent = if (requests > 0) (hits.toDouble() / requests * 100) else 0.0,
            uptimeMs = uptimeMs,
            cacheSize = cache.estimatedSize(),
            maxSize = DEFAULT_MAX_SIZE
        )
    }
}

/**
 * Cache statistics data class.
 */
data class CacheStats(
    val requestsTotal: Long,
    val cacheHitsTotal: Long,
    val dbHitsTotal: Long,
    val cacheHitPercent: Double,
    val uptimeMs: Long,
    val cacheSize: Long,
    val maxSize: Long
)
