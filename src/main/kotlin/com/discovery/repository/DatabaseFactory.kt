package com.discovery.repository

import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import io.ktor.server.application.*
import java.sql.Connection

object DatabaseFactory {
    private lateinit var dataSource: HikariDataSource

    fun init(environment: ApplicationEnvironment) {
        val config = HikariConfig().apply {
            jdbcUrl = environment.config.property("database.jdbcUrl").getString()
            driverClassName = environment.config.property("database.driverClassName").getString()
            username = environment.config.property("database.username").getString()
            password = environment.config.property("database.password").getString()
            
            // Tuned for high throughput
            maximumPoolSize = environment.config.propertyOrNull("database.maximumPoolSize")?.getString()?.toInt() ?: 50
            minimumIdle = environment.config.propertyOrNull("database.minimumIdle")?.getString()?.toInt() ?: 10
            connectionTimeout = environment.config.propertyOrNull("database.connectionTimeout")?.getString()?.toLong() ?: 30000
            idleTimeout = environment.config.propertyOrNull("database.idleTimeout")?.getString()?.toLong() ?: 600000
            maxLifetime = environment.config.propertyOrNull("database.maxLifetime")?.getString()?.toLong() ?: 1800000
            
            // Performance optimizations
            addDataSourceProperty("cachePrepStmts", "true")
            addDataSourceProperty("prepStmtCacheSize", "250")
            addDataSourceProperty("prepStmtCacheSqlLimit", "2048")
            addDataSourceProperty("useServerPrepStmts", "true")
        }
        
        dataSource = HikariDataSource(config)
    }

    fun getConnection(): Connection = dataSource.connection

    fun close() {
        if (::dataSource.isInitialized) {
            dataSource.close()
        }
    }
}

