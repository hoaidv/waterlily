package com.discovery.models

import kotlinx.serialization.Serializable

@Serializable
data class Category(
    val id: String,
    val name: String,
    val description: String?,
    val productDefId: String?
)

