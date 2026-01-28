package com.discovery.model

import kotlinx.serialization.Serializable

/**
 * Database entity for categories table
 */
data class Category(
    val id: Long,
    val name: String,
    val description: String?
)

/**
 * API response DTO for category details
 */
@Serializable
data class CategoryDetail(
    val id: Long,
    val name: String,
    val description: String?
)

fun Category.toDetail() = CategoryDetail(
    id = id,
    name = name,
    description = description
)
