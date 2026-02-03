package com.discovery.routes

import com.discovery.AppReadiness
import com.discovery.config.R2dbcConfig
import io.ktor.http.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.serialization.Serializable
import java.time.Instant

@Serializable
data class HealthResponse(
    val healthy: Boolean,
    val status: String,
    val timestamp: String,
    val dbConnected: Boolean
)

@Serializable
data class WarmupProgress(
    val inProgress: Boolean,
    val complete: Boolean,
    val loaded: Long,
    val notFound: Long,
    val totalRequested: Long,
    val percentComplete: Int,
    val durationMs: Long
)

@Serializable
data class ReadinessResponse(
    val ready: Boolean,
    val status: String,
    val timestamp: String,
    val dbConnected: Boolean,
    val cacheSize: Long? = null,
    val cacheMaxSize: Long? = null,
    val warmup: WarmupProgress? = null
)

fun Route.healthRoutes() {
    /**
     * Liveness probe - checks if app is alive and DB is connected.
     * Healthy = DB Connected
     * 
     * Returns 200 if healthy, 503 if unhealthy.
     */
    get("/health") {
        val dbConnected = R2dbcConfig.isHealthy()
        
        val response = HealthResponse(
            healthy = dbConnected,
            status = if (dbConnected) "healthy" else "unhealthy",
            timestamp = Instant.now().toString(),
            dbConnected = dbConnected
        )
        
        if (dbConnected) {
            call.respond(response)
        } else {
            call.respond(HttpStatusCode.ServiceUnavailable, response)
        }
    }
    
    /**
     * Readiness probe - checks if app is ready to serve traffic.
     * Ready = DB Connected & Warmup Completed
     * 
     * Returns 200 if ready, 503 if not ready.
     * Includes warmup progress for monitoring.
     */
    get("/ready") {
        val dbConnected = R2dbcConfig.isHealthy()
        val cache = AppReadiness.cache
        val cacheStats = cache?.getStats()
        val warmupStats = cacheStats?.warmupStats
        
        // Determine warmup status
        val warmupEnabled = cache != null
        val warmupInProgress = AppReadiness.warmupInProgress
        val warmupComplete = cacheStats?.warmupComplete ?: true  // true if no cache/warmup
        
        // Calculate warmup progress
        val warmupProgress = if (warmupEnabled) {
            val loaded = warmupStats?.loaded ?: cacheStats?.cacheSize ?: 0L
            val notFound = warmupStats?.notFound ?: 0L
            val totalRequested = warmupStats?.totalRequested ?: cacheStats?.maxSize ?: 0L
            val processed = loaded + notFound
            val percentComplete = if (totalRequested > 0 && warmupInProgress) {
                ((processed * 100) / totalRequested).toInt().coerceIn(0, 100)
            } else if (warmupComplete) {
                100
            } else {
                0
            }
            
            WarmupProgress(
                inProgress = warmupInProgress,
                complete = warmupComplete,
                loaded = loaded,
                notFound = notFound,
                totalRequested = totalRequested,
                percentComplete = percentComplete,
                durationMs = warmupStats?.durationMs ?: 0L
            )
        } else {
            null
        }
        
        // Ready = DB Connected & Warmup Completed
        val ready = dbConnected && warmupComplete
        
        val status = when {
            !dbConnected -> "db_disconnected"
            warmupInProgress -> "warmup_in_progress"
            !warmupComplete -> "warmup_pending"
            else -> "ready"
        }
        
        val response = ReadinessResponse(
            ready = ready,
            status = status,
            timestamp = Instant.now().toString(),
            dbConnected = dbConnected,
            cacheSize = cacheStats?.cacheSize,
            cacheMaxSize = cacheStats?.maxSize,
            warmup = warmupProgress
        )
        
        if (ready) {
            call.respond(response)
        } else {
            call.respond(HttpStatusCode.ServiceUnavailable, response)
        }
    }
}
