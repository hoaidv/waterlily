package com.discovery.routes

import com.discovery.monitor.NettyBlockingMonitor
import com.discovery.service.ProductService
import io.ktor.http.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.serialization.Serializable

@Serializable
data class CacheStatsResponse(
    val requestsTotal: Long,
    val cacheHitsTotal: Long,
    val dbHitsTotal: Long,
    val cacheHitPercent: Double,
    val uptimeMs: Long,
    val cacheSize: Long,
    val maxSize: Long,
    val enabled: Boolean
)

@Serializable
data class BlockingMonitorStats(
    val uptimeMs: Long,
    val totalBlockingEvents: Long,
    val totalBlockingTimeMs: Long,
    val monitoredThreads: Int,
    val currentlyBlockedThreads: Int,
    val avgBlockingTimePerEvent: Double
)

@Serializable
data class ThreadInfo(
    val id: Long,
    val name: String,
    val state: String,
    val isNettyThread: Boolean
)

@Serializable
data class MonitorResponse(
    val status: String,
    val stats: BlockingMonitorStats,
    val threads: List<ThreadInfo>
)

/**
 * Routes for monitoring Netty thread blocking and cache statistics.
 */
fun Route.monitorRoutes(productService: ProductService) {
    route("/monitor") {
        /**
         * GET /monitor/cache
         * Returns ProductDetail cache statistics
         */
        get("/cache") {
            val stats = productService.getCacheStats()
            if (stats != null) {
                call.respond(CacheStatsResponse(
                    requestsTotal = stats.requestsTotal,
                    cacheHitsTotal = stats.cacheHitsTotal,
                    dbHitsTotal = stats.dbHitsTotal,
                    cacheHitPercent = stats.cacheHitPercent,
                    uptimeMs = stats.uptimeMs,
                    cacheSize = stats.cacheSize,
                    maxSize = stats.maxSize,
                    enabled = true
                ))
            } else {
                call.respond(CacheStatsResponse(
                    requestsTotal = 0,
                    cacheHitsTotal = 0,
                    dbHitsTotal = 0,
                    cacheHitPercent = 0.0,
                    uptimeMs = 0,
                    cacheSize = 0,
                    maxSize = 0,
                    enabled = false
                ))
            }
        }

        /**
         * GET /monitor/blocking
         * Returns current blocking monitor statistics
         */
        get("/blocking") {
            val monitor = NettyBlockingMonitor.getInstance()
            val stats = monitor.getStatistics()
            
            val avgTime = if (stats.totalBlockingEvents > 0) {
                stats.totalBlockingTimeMs.toDouble() / stats.totalBlockingEvents
            } else {
                0.0
            }
            
            val response = BlockingMonitorStats(
                uptimeMs = stats.uptimeMs,
                totalBlockingEvents = stats.totalBlockingEvents,
                totalBlockingTimeMs = stats.totalBlockingTimeMs,
                monitoredThreads = stats.monitoredThreads,
                currentlyBlockedThreads = stats.currentlyBlockedThreads,
                avgBlockingTimePerEvent = avgTime
            )
            
            call.respond(response)
        }
        
        /**
         * GET /monitor/threads
         * Returns information about all threads
         */
        get("/threads") {
            val threadMXBean = java.lang.management.ManagementFactory.getThreadMXBean()
            val threadInfos = threadMXBean.dumpAllThreads(false, false)
            
            val nettyPatterns = listOf(
                "ktor-cio",
                "eventLoopGroup",
                "nioEventLoopGroup",
                "epollEventLoopGroup",
                "kqueueEventLoopGroup",
                "ktor-netty"
            )
            
            val threads = threadInfos.map { info ->
                val isNetty = nettyPatterns.any { pattern ->
                    info.threadName.contains(pattern, ignoreCase = true)
                }
                ThreadInfo(
                    id = info.threadId,
                    name = info.threadName,
                    state = info.threadState.name,
                    isNettyThread = isNetty
                )
            }.sortedByDescending { it.isNettyThread }
            
            call.respond(threads)
        }
        
        /**
         * GET /monitor/threads/netty
         * Returns information about Netty event loop threads only
         */
        get("/threads/netty") {
            val threadMXBean = java.lang.management.ManagementFactory.getThreadMXBean()
            val threadInfos = threadMXBean.dumpAllThreads(false, false)
            
            val nettyPatterns = listOf(
                "ktor-cio",
                "eventLoopGroup",
                "nioEventLoopGroup",
                "epollEventLoopGroup",
                "kqueueEventLoopGroup",
                "ktor-netty"
            )
            
            val threads = threadInfos
                .filter { info ->
                    nettyPatterns.any { pattern ->
                        info.threadName.contains(pattern, ignoreCase = true)
                    }
                }
                .map { info ->
                    ThreadInfo(
                        id = info.threadId,
                        name = info.threadName,
                        state = info.threadState.name,
                        isNettyThread = true
                    )
                }
            
            call.respond(threads)
        }
        
        /**
         * GET /monitor/status
         * Returns overall monitor health status
         */
        get("/status") {
            val monitor = NettyBlockingMonitor.getInstance()
            val stats = monitor.getStatistics()
            
            val avgTime = if (stats.totalBlockingEvents > 0) {
                stats.totalBlockingTimeMs.toDouble() / stats.totalBlockingEvents
            } else {
                0.0
            }
            
            // Determine status based on blocking metrics
            val status = when {
                stats.currentlyBlockedThreads > 0 -> "DEGRADED"
                stats.totalBlockingEvents > 100 && avgTime > 100 -> "WARNING"
                stats.totalBlockingEvents > 0 -> "OK_WITH_BLOCKING"
                else -> "HEALTHY"
            }
            
            val threadMXBean = java.lang.management.ManagementFactory.getThreadMXBean()
            val threadInfos = threadMXBean.dumpAllThreads(false, false)
            
            val nettyPatterns = listOf(
                "ktor-cio",
                "eventLoopGroup",
                "nioEventLoopGroup",
                "epollEventLoopGroup",
                "kqueueEventLoopGroup",
                "ktor-netty"
            )
            
            val nettyThreads = threadInfos.filter { info ->
                nettyPatterns.any { pattern ->
                    info.threadName.contains(pattern, ignoreCase = true)
                }
            }.map { info ->
                ThreadInfo(
                    id = info.threadId,
                    name = info.threadName,
                    state = info.threadState.name,
                    isNettyThread = true
                )
            }
            
            val response = MonitorResponse(
                status = status,
                stats = BlockingMonitorStats(
                    uptimeMs = stats.uptimeMs,
                    totalBlockingEvents = stats.totalBlockingEvents,
                    totalBlockingTimeMs = stats.totalBlockingTimeMs,
                    monitoredThreads = stats.monitoredThreads,
                    currentlyBlockedThreads = stats.currentlyBlockedThreads,
                    avgBlockingTimePerEvent = avgTime
                ),
                threads = nettyThreads
            )
            
            val statusCode = when (status) {
                "DEGRADED" -> HttpStatusCode.ServiceUnavailable
                "WARNING" -> HttpStatusCode.OK
                else -> HttpStatusCode.OK
            }
            
            call.respond(statusCode, response)
        }
    }
}
