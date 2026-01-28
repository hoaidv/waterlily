package com.discovery

import com.discovery.config.DatabaseConfig
import com.discovery.plugins.configureSerialization
import com.discovery.plugins.configureStatusPages
import com.discovery.routes.healthRoutes
import com.discovery.routes.productRoutes
import com.discovery.service.ProductService
import io.ktor.server.application.*
import io.ktor.server.routing.*

fun main(args: Array<String>) {
    io.ktor.server.netty.EngineMain.main(args)
}

fun Application.module() {
    // Initialize database connection pool
    DatabaseConfig.init(environment)

    // Configure plugins
    configureSerialization()
    configureStatusPages()

    // Initialize services
    val productService = ProductService()

    // Configure routes
    routing {
        healthRoutes()
        productRoutes(productService)
    }

    // Shutdown hook
    environment.monitor.subscribe(ApplicationStopped) {
        DatabaseConfig.close()
    }
}
