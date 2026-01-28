package com.discovery.models

import kotlinx.serialization.Serializable

@Serializable
data class ProductVariant(
    val id: String,
    val productId: String,
    val variantSku: String,
    val quantity: Int,
    val price: Double,
    val currency: String,
    val attributes: String? // JSON string
)

