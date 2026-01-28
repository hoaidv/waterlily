package com.discovery

import com.discovery.repository.DatabaseFactory
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import io.ktor.server.plugins.contentnegotiation.*
import kotlinx.serialization.json.Json

fun main(args: Array<String>) {
    io.ktor.server.netty.EngineMain.main(args)
}

fun Application.module() {
    // Initialize database connection pool
    DatabaseFactory.init(environment)
    
    // Configure JSON serialization
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = false
            isLenient = true
            ignoreUnknownKeys = true
        })
    }
    
    // Configure routes
    configureRouting()
    
    // Shutdown hook for cleanup
    environment.monitor.subscribe(ApplicationStopped) {
        DatabaseFactory.close()
    }
}
