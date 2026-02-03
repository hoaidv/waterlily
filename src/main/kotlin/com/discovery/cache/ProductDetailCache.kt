package com.discovery.cache

import com.discovery.model.ProductDetail
import com.discovery.repository.ProductRepository
import com.github.benmanes.caffeine.cache.Cache
import com.github.benmanes.caffeine.cache.Caffeine
import io.micrometer.core.instrument.Counter
import io.micrometer.core.instrument.MeterRegistry
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Semaphore
import org.slf4j.LoggerFactory

/**
 * LRU cache for ProductDetail by ID with metrics tracking and warmup support.
 * 
 * Design decisions:
 * - Cache only non-null results (products that exist)
 * - Null results (product not found) are not cached to allow retry
 * - No cache invalidation (as per spec)
 * - Warmup strategy: load products from file before app is ready
 * - Metrics exposed via Micrometer for Prometheus scraping
 */
class ProductDetailCache(
    private val repository: ProductRepository,
    private val meterRegistry: MeterRegistry,
    private val maxSize: Long = DEFAULT_MAX_SIZE
) {
    companion object {
        const val DEFAULT_MAX_SIZE = 1_000_000L
        private const val WARMUP_CONCURRENCY = 50  // Number of concurrent DB requests during warmup
        private const val PROGRESS_REPORT_INTERVAL = 10  // Report every 10%
    }

    private val log = LoggerFactory.getLogger(ProductDetailCache::class.java)

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

    // Warmup state
    @Volatile
    private var warmupComplete: Boolean = false
    @Volatile
    private var warmupStats: WarmupStats? = null

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
     * Warmup the cache by loading products from a list of IDs.
     * Loads up to maxSize products concurrently and reports progress.
     * 
     * @param productIds List of product IDs to load
     * @param onProgress Optional callback for progress updates (percent, loaded count)
     * @return WarmupStats with results of the warmup operation
     */
    suspend fun warmup(
        productIds: List<Long>,
        onProgress: ((percent: Int, loaded: Long) -> Unit)? = null
    ): WarmupStats = coroutineScope {
        val startTime = System.currentTimeMillis()
        val idsToLoad = productIds.take(maxSize.toInt())
        val totalToLoad = idsToLoad.size
        
        if (totalToLoad == 0) {
            log.info("Cache warmup: No product IDs to load")
            val stats = WarmupStats(
                totalRequested = 0,
                loaded = 0,
                notFound = 0,
                durationMs = 0
            )
            warmupStats = stats
            warmupComplete = true
            return@coroutineScope stats
        }

        log.info("Cache warmup: Starting to load $totalToLoad products (cache limit: $maxSize)")
        
        var loadedCount = 0L
        var notFoundCount = 0L
        var lastReportedPercent = 0
        
        // Use semaphore to limit concurrent DB requests
        val semaphore = Semaphore(WARMUP_CONCURRENCY)
        
        // Process all IDs with controlled concurrency
        val jobs = idsToLoad.mapIndexed { index, id ->
            launch {
                semaphore.acquire()
                try {
                    val product = repository.findById(id)
                    if (product != null) {
                        cache.put(id, product)
                        synchronized(this@ProductDetailCache) {
                            loadedCount++
                        }
                    } else {
                        synchronized(this@ProductDetailCache) {
                            notFoundCount++
                        }
                    }
                    
                    // Report progress
                    val processed = loadedCount + notFoundCount
                    val percent = ((processed * 100) / totalToLoad).toInt()
                    if (percent >= lastReportedPercent + PROGRESS_REPORT_INTERVAL) {
                        synchronized(this@ProductDetailCache) {
                            if (percent >= lastReportedPercent + PROGRESS_REPORT_INTERVAL) {
                                lastReportedPercent = (percent / PROGRESS_REPORT_INTERVAL) * PROGRESS_REPORT_INTERVAL
                                log.info("Cache warmup: $lastReportedPercent% complete ($loadedCount loaded, $notFoundCount not found)")
                                onProgress?.invoke(lastReportedPercent, loadedCount)
                            }
                        }
                    }
                } finally {
                    semaphore.release()
                }
            }
        }
        
        // Wait for all jobs to complete
        jobs.forEach { it.join() }
        
        val durationMs = System.currentTimeMillis() - startTime
        val stats = WarmupStats(
            totalRequested = totalToLoad.toLong(),
            loaded = loadedCount,
            notFound = notFoundCount,
            durationMs = durationMs
        )
        
        warmupStats = stats
        warmupComplete = true
        
        log.info("Cache warmup: Complete! Loaded $loadedCount products, $notFoundCount not found, took ${durationMs}ms")
        
        stats
    }

    /**
     * Check if cache warmup is complete.
     */
    fun isWarmupComplete(): Boolean = warmupComplete

    /**
     * Get warmup statistics (null if warmup hasn't been performed).
     */
    fun getWarmupStats(): WarmupStats? = warmupStats

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
            maxSize = maxSize,
            warmupComplete = warmupComplete,
            warmupStats = warmupStats
        )
    }
}

/**
 * Statistics from cache warmup operation.
 */
data class WarmupStats(
    val totalRequested: Long,
    val loaded: Long,
    val notFound: Long,
    val durationMs: Long
)

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
    val maxSize: Long,
    val warmupComplete: Boolean = false,
    val warmupStats: WarmupStats? = null
)
