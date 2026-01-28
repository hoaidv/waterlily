package com.discovery.model

import kotlinx.serialization.Serializable

/**
 * Database entity for product_media table
 */
data class ProductMedia(
    val id: Long,
    val productId: Long,
    val variantId: Long?,
    val type: String,
    val resolution: String,
    val url: String
)

/**
 * API response DTO for media details
 */
@Serializable
data class MediaDetail(
    val id: Long,
    val type: String,
    val resolution: String,
    val url: String,
    val variantId: Long?
)

fun ProductMedia.toDetail() = MediaDetail(
    id = id,
    type = type,
    resolution = resolution,
    url = url,
    variantId = variantId
)
