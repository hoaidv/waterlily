package com.discovery.service

import com.discovery.cache.CacheStats
import com.discovery.cache.ProductDetailCache
import com.discovery.model.ProductDetail
import com.discovery.repository.ProductRepository

class ProductService(
    private val repository: ProductRepository = ProductRepository(),
    private val cache: ProductDetailCache? = null
) {
    
    /**
     * Get a single product by ID with all related details.
     * Uses cache when available for improved performance.
     * 
     * This is a suspend function - it will not block the calling thread.
     * The actual database work happens on the DatabaseDispatcher.
     */
    suspend fun getProductById(id: Long): ProductDetail? {
        // Use cache if available, otherwise fall back to direct repository access
        return cache?.getById(id) ?: repository.findById(id)
    }

    /**
     * Get multiple products by their IDs with all related details.
     * Note: Batch endpoint is not cached (as per spec).
     * 
     * This is a suspend function - it will not block the calling thread.
     * The actual database work happens on the DatabaseDispatcher.
     */
    suspend fun getProductsByIds(ids: List<Long>): List<ProductDetail> {
        if (ids.isEmpty()) return emptyList()
        return repository.findByIds(ids)
    }

    /**
     * Get cache statistics if caching is enabled.
     */
    fun getCacheStats(): CacheStats? = cache?.getStats()
}
