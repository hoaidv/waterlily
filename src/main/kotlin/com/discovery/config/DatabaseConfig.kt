package com.discovery.config

import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import io.ktor.server.application.*
import java.sql.Connection

object DatabaseConfig {
    private lateinit var dataSource: HikariDataSource

    fun init(environment: ApplicationEnvironment) {
        val config = HikariConfig().apply {
            jdbcUrl = environment.config.property("database.jdbcUrl").getString()
            username = environment.config.property("database.username").getString()
            password = environment.config.property("database.password").getString()
            maximumPoolSize = environment.config.propertyOrNull("database.maximumPoolSize")?.getString()?.toInt() ?: 100
            minimumIdle = environment.config.propertyOrNull("database.minimumIdle")?.getString()?.toInt() ?: 50
            connectionTimeout = environment.config.propertyOrNull("database.connectionTimeout")?.getString()?.toLong() ?: 30000
            idleTimeout = environment.config.propertyOrNull("database.idleTimeout")?.getString()?.toLong() ?: 600000
            maxLifetime = environment.config.propertyOrNull("database.maxLifetime")?.getString()?.toLong() ?: 1800000
            
            // MySQL specific optimizations
            addDataSourceProperty("cachePrepStmts", "true")
            addDataSourceProperty("prepStmtCacheSize", "250")
            addDataSourceProperty("prepStmtCacheSqlLimit", "2048")
            addDataSourceProperty("useServerPrepStmts", "true")
            addDataSourceProperty("useLocalSessionState", "true")
            addDataSourceProperty("rewriteBatchedStatements", "true")
            addDataSourceProperty("cacheResultSetMetadata", "true")
            addDataSourceProperty("cacheServerConfiguration", "true")
            addDataSourceProperty("elideSetAutoCommits", "true")
            addDataSourceProperty("maintainTimeStats", "false")
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
