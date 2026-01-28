package com.discovery.model

import kotlinx.serialization.Serializable

/**
 * Category entity - used for both DB mapping and API response
 */
@Serializable
data class Category(
    val id: Long,
    val name: String,
    val description: String?
)
