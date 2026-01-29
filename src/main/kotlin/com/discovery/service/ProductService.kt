package com.discovery.service

import com.discovery.model.ProductDetail
import com.discovery.repository.ProductRepository

class ProductService(
    private val repository: ProductRepository = ProductRepository()
) {
    
    /**
     * Get a single product by ID with all related details.
     * 
     * This is a suspend function - it will not block the calling thread.
     * The actual database work happens on the DatabaseDispatcher.
     */
    suspend fun getProductById(id: Long): ProductDetail? {
        return repository.findById(id)
    }

    /**
     * Get multiple products by their IDs with all related details.
     * 
     * This is a suspend function - it will not block the calling thread.
     * The actual database work happens on the DatabaseDispatcher.
     */
    suspend fun getProductsByIds(ids: List<Long>): List<ProductDetail> {
        if (ids.isEmpty()) return emptyList()
        return repository.findByIds(ids)
    }
}
