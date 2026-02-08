package com.discovery

import com.discovery.cache.CacheWarmup
import com.discovery.cache.ProductDetailCache
import com.discovery.config.R2dbcConfig
import com.discovery.plugins.BlockingMonitorPlugin
import com.discovery.plugins.HighLoadShedderPlugin
import com.discovery.plugins.configureSerialization
import com.discovery.plugins.configureStatusPages
import com.discovery.repository.ProductRepository
import com.discovery.routes.healthRoutes
import com.discovery.routes.metricsRoutes
import com.discovery.routes.monitorRoutes
import com.discovery.routes.productRoutes
import com.discovery.service.ProductService
import io.ktor.server.application.*
import io.ktor.server.metrics.micrometer.*
import io.ktor.server.netty.NettyApplicationEngine
import io.ktor.server.routing.*
import io.micrometer.prometheus.PrometheusConfig
import io.micrometer.prometheus.PrometheusMeterRegistry
import io.netty.channel.ChannelHandlerContext
import io.netty.channel.ChannelInboundHandlerAdapter
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.util.concurrent.atomic.AtomicInteger

fun main(args: Array<String>) {
    io.ktor.server.netty.EngineMain.main(args)
}

/**
 * Application readiness state holder.
 * Used by health routes to report readiness status.
 * 
 * Note: Application is marked ready immediately after routes are configured.
 * Cache warmup runs in the background and doesn't block application startup.
 */
object AppReadiness {
    @Volatile
    var isReady: Boolean = false
        private set
    
    @Volatile
    var cache: ProductDetailCache? = null
        private set
    
    @Volatile
    var warmupInProgress: Boolean = false
        internal set
    
    fun markReady() {
        isReady = true
    }
    
    fun setCache(cache: ProductDetailCache?) {
        this.cache = cache
    }
}

fun Application.module() {
    // Initialize R2DBC connection pool (non-blocking reactive database)
    R2dbcConfig.init(environment)

    // Configure plugins
    configureSerialization()
    configureStatusPages()
    
    // Configure Prometheus metrics
    val prometheusMeterRegistry = PrometheusMeterRegistry(PrometheusConfig.DEFAULT)
    install(MicrometerMetrics) {
        registry = prometheusMeterRegistry
    }

    // Gauges: active client connections (Netty channels) and in-flight requests (Ktor pipeline)
    val activeClientConnections = AtomicInteger(0)
    val inFlightRequests = AtomicInteger(0)
    prometheusMeterRegistry.gauge("active_client_connections", activeClientConnections) { it.get().toDouble() }
    prometheusMeterRegistry.gauge("in_flight_requests", inFlightRequests) { it.get().toDouble() }

    // Count active Netty channels (client connections) via pipeline handler
    (engine as? NettyApplicationEngine)?.configuration?.channelPipelineConfig = {
        addLast(object : ChannelInboundHandlerAdapter() {
            override fun channelActive(ctx: ChannelHandlerContext) {
                activeClientConnections.incrementAndGet()
                ctx.fireChannelActive()
            }
            override fun channelInactive(ctx: ChannelHandlerContext) {
                activeClientConnections.decrementAndGet()
                ctx.fireChannelInactive()
            }
        })
    }

    // High load shedder: 503 when RTW/HTT/TOR/TC/CC conditions are met (before counting in-flight)
    install(HighLoadShedderPlugin) {
        enabled = environment.config.propertyOrNull("highLoadShedder.enabled")?.getString()?.toBoolean() ?: false
        recentTimeWindowSeconds = environment.config.propertyOrNull("highLoadShedder.recentTimeWindowSeconds")?.getString()?.toIntOrNull() ?: 12
        highTrafficThresholdRps = environment.config.propertyOrNull("highLoadShedder.highTrafficThresholdRps")?.getString()?.toIntOrNull() ?: 500
        timeoutRatePercent = environment.config.propertyOrNull("highLoadShedder.timeoutRatePercent")?.getString()?.toDoubleOrNull() ?: 1.0
        responseTimeThresholdMs = environment.config.propertyOrNull("highLoadShedder.responseTimeThresholdMs")?.getString()?.toLongOrNull() ?: 3000L
        checkIntervalSeconds = environment.config.propertyOrNull("highLoadShedder.checkIntervalSeconds")?.getString()?.toLongOrNull() ?: 1L
        triggerConsecutiveChecks = environment.config.propertyOrNull("highLoadShedder.triggerConsecutiveChecks")?.getString()?.toIntOrNull() ?: 3
        cooldownConsecutiveChecks = environment.config.propertyOrNull("highLoadShedder.cooldownConsecutiveChecks")?.getString()?.toIntOrNull() ?: 3
        excludedPaths = environment.config.propertyOrNull("highLoadShedder.excludedPaths")?.getString()
            ?.splitToSequence(',')
            ?.map { it.trim() }
            ?.filter { it.isNotEmpty() }
            ?.toSet()
            .orEmpty()
            .ifEmpty { setOf("/health", "/ready", "/metrics") }
        meterRegistry = prometheusMeterRegistry
    }

    // Count in-flight requests (no exclusion) via application pipeline interceptor
    intercept(ApplicationCallPipeline.Call) {
        inFlightRequests.incrementAndGet()
        try {
            proceed()
        } finally {
            inFlightRequests.decrementAndGet()
        }
    }

    // Configure Netty blocking monitor
    install(BlockingMonitorPlugin) {
        enabled = environment.config.propertyOrNull("monitor.blocking.enabled")?.getString()?.toBoolean() ?: true
        checkIntervalMs = environment.config.propertyOrNull("monitor.blocking.checkIntervalMs")?.getString()?.toLong() ?: 100
        warningThresholdMs = environment.config.propertyOrNull("monitor.blocking.warningThresholdMs")?.getString()?.toLong() ?: 50
        criticalThresholdMs = environment.config.propertyOrNull("monitor.blocking.criticalThresholdMs")?.getString()?.toLong() ?: 200
        stackTraceOnWarning = environment.config.propertyOrNull("monitor.blocking.stackTraceOnWarning")?.getString()?.toBoolean() ?: true
    }

    // Initialize cache and services
    val cacheEnabled = environment.config.propertyOrNull("cache.productDetail.enabled")?.getString()?.toBoolean() ?: true
    val cacheMaxSize = environment.config.propertyOrNull("cache.productDetail.maxSize")?.getString()?.toLongOrNull() 
        ?: ProductDetailCache.DEFAULT_MAX_SIZE
    
    val repository = ProductRepository()
    val cache = if (cacheEnabled) {
        log.info("ProductDetail cache enabled with maxSize=$cacheMaxSize")
        ProductDetailCache(repository, prometheusMeterRegistry, cacheMaxSize)
    } else {
        log.info("ProductDetail cache disabled")
        null
    }
    
    // Store cache reference for health routes
    AppReadiness.setCache(cache)
    
    val productService = ProductService(repository, cache)

    // Configure routes
    routing {
        healthRoutes()
        productRoutes(productService)
        monitorRoutes(productService)
        metricsRoutes(prometheusMeterRegistry)
    }
    
    // Mark application as ready (before warmup - warmup runs in background)
    AppReadiness.markReady()
    log.info("Application is ready to serve requests")

    // Cache warmup (runs in background, does not block application startup)
    val warmupEnabled = environment.config.propertyOrNull("cache.productDetail.warmup.enabled")?.getString()?.toBoolean() ?: false
    val warmupFile = environment.config.propertyOrNull("cache.productDetail.warmup.productIdsFile")?.getString()
    
    if (cache != null && warmupEnabled && warmupFile != null) {
        log.info("Cache warmup enabled, starting background warmup from: $warmupFile")
        AppReadiness.warmupInProgress = true
        
        // Launch warmup in background coroutine
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val productIds = CacheWarmup.readProductIds(warmupFile, cacheMaxSize)
                if (productIds.isNotEmpty()) {
                    cache.warmup(productIds)
                } else {
                    log.warn("No product IDs loaded for warmup - cache will fill naturally on first access")
                }
            } catch (e: Exception) {
                log.error("Cache warmup failed: ${e.message}", e)
            } finally {
                AppReadiness.warmupInProgress = false
            }
        }
    } else if (cache != null && warmupEnabled) {
        log.warn("Cache warmup enabled but productIdsFile not configured")
    }

    // Shutdown hook
    monitor.subscribe(ApplicationStopped) {
        R2dbcConfig.close()
    }
}
