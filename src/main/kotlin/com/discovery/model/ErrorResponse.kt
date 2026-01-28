package com.discovery.model

import kotlinx.serialization.Serializable

/**
 * Standard error response format
 */
@Serializable
data class ErrorResponse(
    val error: String,
    val message: String
)

/**
 * Error response for product not found
 */
@Serializable
data class ProductNotFoundResponse(
    val error: String = "NOT_FOUND",
    val message: String = "Product not found",
    val productId: Long
)

/**
 * Error response for invalid batch request
 */
@Serializable
data class BatchLimitExceededResponse(
    val error: String = "INVALID_REQUEST",
    val message: String = "Maximum 50 product IDs allowed per request",
    val requestedCount: Int,
    val maxAllowed: Int = 50
)

/**
 * Custom exceptions for the application
 */
class ProductNotFoundException(val productId: Long) : RuntimeException("Product not found: $productId")
class InvalidRequestException(override val message: String) : RuntimeException(message)
class BatchLimitExceededException(val requestedCount: Int) : RuntimeException("Maximum 50 product IDs allowed per request")
