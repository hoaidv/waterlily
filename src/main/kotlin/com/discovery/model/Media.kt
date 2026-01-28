package com.discovery.model

import kotlinx.serialization.Serializable

/**
 * ProductMedia entity - used for both DB mapping and API response
 */
@Serializable
data class ProductMedia(
    val id: Long,
    val productId: Long,
    val variantId: Long?,
    val type: String,
    val resolution: String,
    val url: String
)
