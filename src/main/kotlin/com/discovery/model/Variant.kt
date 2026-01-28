package com.discovery.model

import kotlinx.serialization.Serializable

/**
 * ProductVariant entity - used for both DB mapping and API response
 * Uses Double for price to avoid BigDecimal overhead
 */
@Serializable
data class ProductVariant(
    val id: Long,
    val productId: Long,
    val variantSku: String,
    val quantity: Int,
    val price: Double,
    val currency: String,
    val attributes: String?
)
