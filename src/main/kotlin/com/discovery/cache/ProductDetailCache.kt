package com.discovery.cache

import com.discovery.model.ProductDetail
import com.discovery.repository.ProductRepository
import com.github.benmanes.caffeine.cache.Cache
import com.github.benmanes.caffeine.cache.Caffeine
import java.util.concurrent.atomic.AtomicLong

/**
 * LRU cache for ProductDetail by ID with metrics tracking.
 * 
 * Design decisions:
 * - Cache only non-null results (products that exist)
 * - Null results (product not found) are not cached to allow retry
 * - No cache invalidation (as per spec)
 * - No warmup strategy - cache fills naturally on first access
 */
class ProductDetailCache(
    private val repository: ProductRepository,
    maxSize: Long = DEFAULT_MAX_SIZE
) {
    companion object {
        const val DEFAULT_MAX_SIZE = 1_000_000L
    }

    private val cache: Cache<Long, ProductDetail> = Caffeine.newBuilder()
        .maximumSize(maxSize)
        .build()

    // Metrics counters
    private val requestsTotal = AtomicLong(0)
    private val cacheHitsTotal = AtomicLong(0)
    private val dbHitsTotal = AtomicLong(0)
    private val startTimeMs = System.currentTimeMillis()

    /**
     * Get product by ID, using cache when available.
     * On cache miss, fetches from repository and caches non-null results.
     */
    suspend fun getById(id: Long): ProductDetail? {
        requestsTotal.incrementAndGet()

        // Check cache first
        val cached = cache.getIfPresent(id)
        if (cached != null) {
            cacheHitsTotal.incrementAndGet()
            return cached
        }

        // Cache miss - fetch from database
        dbHitsTotal.incrementAndGet()
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
        val requests = requestsTotal.get()
        val hits = cacheHitsTotal.get()
        val dbHits = dbHitsTotal.get()
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

    /**
     * Reset statistics (useful for benchmarking).
     */
    fun resetStats() {
        requestsTotal.set(0)
        cacheHitsTotal.set(0)
        dbHitsTotal.set(0)
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
