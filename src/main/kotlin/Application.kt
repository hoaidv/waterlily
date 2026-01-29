package com.discovery

import com.discovery.config.R2dbcConfig
import com.discovery.plugins.BlockingMonitorPlugin
import com.discovery.plugins.configureSerialization
import com.discovery.plugins.configureStatusPages
import com.discovery.routes.healthRoutes
import com.discovery.routes.monitorRoutes
import com.discovery.routes.productRoutes
import com.discovery.service.ProductService
import io.ktor.server.application.*
import io.ktor.server.routing.*

fun main(args: Array<String>) {
    io.ktor.server.netty.EngineMain.main(args)
}

fun Application.module() {
    // Initialize R2DBC connection pool (non-blocking reactive database)
    R2dbcConfig.init(environment)

    // Configure plugins
    configureSerialization()
    configureStatusPages()
    
    // Configure Netty blocking monitor
    install(BlockingMonitorPlugin) {
        enabled = environment.config.propertyOrNull("monitor.blocking.enabled")?.getString()?.toBoolean() ?: true
        checkIntervalMs = environment.config.propertyOrNull("monitor.blocking.checkIntervalMs")?.getString()?.toLong() ?: 100
        warningThresholdMs = environment.config.propertyOrNull("monitor.blocking.warningThresholdMs")?.getString()?.toLong() ?: 50
        criticalThresholdMs = environment.config.propertyOrNull("monitor.blocking.criticalThresholdMs")?.getString()?.toLong() ?: 200
        stackTraceOnWarning = environment.config.propertyOrNull("monitor.blocking.stackTraceOnWarning")?.getString()?.toBoolean() ?: true
    }

    // Initialize services
    val productService = ProductService()

    // Configure routes
    routing {
        healthRoutes()
        productRoutes(productService)
        monitorRoutes()
    }

    // Shutdown hook
    monitor.subscribe(ApplicationStopped) {
        R2dbcConfig.close()
    }
}
