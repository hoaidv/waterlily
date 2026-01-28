package com.discovery.model

import kotlinx.serialization.Serializable

/**
 * Request body for batch product retrieval
 */
@Serializable
data class BatchRequest(
    val ids: List<Long>
) {
    companion object {
        const val MAX_IDS = 50
    }
}
