package com.discovery.models

import kotlinx.serialization.Serializable

/**
 * Helper object that combines product with its related entities.
 * This is the response format for the product detail API.
 */
@Serializable
data class ProductDetail(
    val id: String,
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

