package com.discovery.model

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject

/**
 * Database entity for products table
 */
data class Product(
    val id: Long,
    val baseSku: String,
    val name: String,
    val description: String?,
    val features: String?,
    val status: String,
    val source: String,
    val sourceSku: String?,
    val sourceUrl: String?,
    val categoryId: Long,
    val attributes: String?
)

/**
 * API response DTO for complete product details including category, variants, and media
 */
@Serializable
data class ProductDetail(
    val id: Long,
    val baseSku: String,
    val name: String,
    val description: String?,
    val features: String?,
    val status: String,
    val source: String,
    val sourceSku: String?,
    val sourceUrl: String?,
    val attributes: String?,
    val category: CategoryDetail,
    val variants: List<VariantDetail>,
    val media: List<MediaDetail>
)

/**
 * API response DTO for batch product retrieval
 */
@Serializable
data class BatchProductResponse(
    val products: List<ProductDetail>,
    val count: Int
)
