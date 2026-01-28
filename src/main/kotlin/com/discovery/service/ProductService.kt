package com.discovery.service

import com.discovery.model.*
import com.discovery.repository.ProductRepository

class ProductService(
    private val repository: ProductRepository = ProductRepository()
) {
    
    /**
     * Get a single product with all its details (category, variants, media)
     */
    fun getProductById(id: Long): ProductDetail? {
        val product = repository.findById(id) ?: return null
        val category = repository.findCategoryById(product.categoryId) 
            ?: return null // Category should always exist
        val variants = repository.findVariantsByProductId(id)
        val media = repository.findMediaByProductId(id)
        
        return assembleProductDetail(product, category, variants, media)
    }
    
    /**
     * Get multiple products by IDs with all their details.
     * Missing products are omitted from the response.
     * Maintains order consistent with input IDs.
     */
    fun getProductsByIds(ids: List<Long>): List<ProductDetail> {
        if (ids.isEmpty()) return emptyList()
        
        // Fetch all products
        val products = repository.findByIds(ids)
        if (products.isEmpty()) return emptyList()
        
        val productIds = products.map { it.id }
        
        // Batch fetch all related data
        val categoryIds = products.map { it.categoryId }.toSet()
        val categories = repository.findCategoriesByIds(categoryIds)
        val variantsByProduct = repository.findVariantsByProductIds(productIds)
        val mediaByProduct = repository.findMediaByProductIds(productIds)
        
        // Assemble product details maintaining order
        return products.mapNotNull { product ->
            val category = categories[product.categoryId] ?: return@mapNotNull null
            val variants = variantsByProduct[product.id] ?: emptyList()
            val media = mediaByProduct[product.id] ?: emptyList()
            
            assembleProductDetail(product, category, variants, media)
        }
    }
    
    private fun assembleProductDetail(
        product: Product,
        category: Category,
        variants: List<ProductVariant>,
        media: List<ProductMedia>
    ): ProductDetail {
        return ProductDetail(
            id = product.id,
            baseSku = product.baseSku,
            name = product.name,
            description = product.description,
            features = product.features,
            status = product.status,
            source = product.source,
            sourceSku = product.sourceSku,
            sourceUrl = product.sourceUrl,
            attributes = product.attributes,
            category = category.toDetail(),
            variants = variants.map { it.toDetail() },
            media = media.map { it.toDetail() }
        )
    }
}
