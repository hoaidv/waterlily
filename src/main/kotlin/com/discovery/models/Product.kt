package com.discovery.models

import kotlinx.serialization.Serializable

@Serializable
data class Product(
    val id: String,
    val baseSku: String,
    val name: String,
    val description: String?,
    val features: String?,
    val status: String,
    val source: String?,
    val sourceSku: String?,
    val sourceUrl: String?,
    val categoryId: String?,
    val productDefId: String?,
    val attributes: String? // JSON string
)

