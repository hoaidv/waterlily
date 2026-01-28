package com.discovery.models

import kotlinx.serialization.Serializable

@Serializable
data class ProductMedia(
    val id: String,
    val productId: String,
    val variantId: String?,
    val type: String,
    val resolution: String?,
    val url: String
)

