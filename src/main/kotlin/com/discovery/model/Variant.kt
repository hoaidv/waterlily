package com.discovery.model

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonObject

/**
 * Database entity for product_variants table
 */
data class ProductVariant(
    val id: Long,
    val productId: Long,
    val variantSku: String,
    val quantity: Int,
    val price: java.math.BigDecimal,
    val currency: String,
    val attributes: JsonObject?
)

/**
 * API response DTO for variant details
 */
@Serializable
data class VariantDetail(
    val id: Long,
    val variantSku: String,
    val quantity: Int,
    val price: Double,
    val currency: String,
    val attributes: JsonObject?
)

fun ProductVariant.toDetail() = VariantDetail(
    id = id,
    variantSku = variantSku,
    quantity = quantity,
    price = price.toDouble(),
    currency = currency,
    attributes = attributes
)
