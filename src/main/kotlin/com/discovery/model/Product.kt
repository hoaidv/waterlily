package com.discovery.model

import kotlinx.serialization.Serializable

/**
 * Product entity - used for both DB mapping and API response
 */
@Serializable
data class Product(
    val id: Long,
    val baseSku: String,
    val name: String,
    val description: String?,
    val features: String?,
    val status: String,
    val source: String?,
    val sourceSku: String?,
    val sourceUrl: String?,
    val categoryId: Long?,
    val attributes: String?
)

/**
 * Complete product detail with related entities - API response format
 */
@Serializable
data class ProductDetail(
    val id: Long,
    val baseSku: String,
    val name: String,
    val description: String?,
    val features: String?,
    val status: String,
    val source: String?,
    val sourceSku: String?,
    val sourceUrl: String?,
    val attributes: String?,
    val category: Category?,
    val variants: List<ProductVariant>,
    val media: List<ProductMedia>
) {
    companion object {
        fun fromProduct(
            product: Product,
            category: Category?,
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
                category = category,
                variants = variants,
                media = media
            )
        }
    }
}

/**
 * API response DTO for batch product retrieval
 */
@Serializable
data class BatchProductResponse(
    val products: List<ProductDetail>,
    val count: Int
)
