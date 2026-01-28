package com.discovery.service

import com.discovery.models.ProductDetail
import com.discovery.repository.ProductRepository

class ProductService(
    private val productRepository: ProductRepository = ProductRepository()
) {
    
    /**
     * Get a single product by ID with all related details.
     * @param id The product ID
     * @return ProductDetail if found, null otherwise
     */
    fun getProductById(id: String): ProductDetail? {
        if (id.isBlank()) {
            return null
        }
        return productRepository.findById(id)
    }

    /**
     * Get multiple products by their IDs with all related details.
     * @param ids List of product IDs
     * @return List of ProductDetail for found products
     */
    fun getProductsByIds(ids: List<String>): List<ProductDetail> {
        // Filter out blank IDs and limit batch size for performance
        val validIds = ids.filter { it.isNotBlank() }.take(MAX_BATCH_SIZE)
        
        if (validIds.isEmpty()) {
            return emptyList()
        }
        
        return productRepository.findByIds(validIds)
    }

    companion object {
        const val MAX_BATCH_SIZE = 100
    }
}

