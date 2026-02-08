package com.discovery.config

import io.asyncer.r2dbc.mysql.MySqlConnectionConfiguration
import io.asyncer.r2dbc.mysql.MySqlConnectionFactory
import io.r2dbc.pool.ConnectionPool
import io.r2dbc.pool.ConnectionPoolConfiguration
import io.r2dbc.spi.ConnectionFactory
import io.r2dbc.spi.ValidationDepth
import io.ktor.server.application.*
import kotlinx.coroutines.reactive.awaitFirstOrNull
import org.slf4j.LoggerFactory
import reactor.core.publisher.Mono
import java.time.Duration

/**
 * R2DBC (Reactive Relational Database Connectivity) configuration.
 * 
 * R2DBC provides true non-blocking database access:
 * - No thread blocking while waiting for database responses
 * - Uses reactive streams (Flux/Mono) under the hood
 * - Integrates with Kotlin coroutines via kotlinx-coroutines-reactor
 * 
 * This allows handling thousands of concurrent database operations
 * with a small number of threads.
 */
object R2dbcConfig {
    private val logger = LoggerFactory.getLogger(R2dbcConfig::class.java)
    
    private lateinit var connectionPool: ConnectionPool
    
    fun init(environment: ApplicationEnvironment) {
        val jdbcUrl = environment.config.property("database.jdbcUrl").getString()
        val username = environment.config.property("database.username").getString()
        val password = environment.config.property("database.password").getString()
        val maxPoolSize = environment.config.propertyOrNull("database.maximumPoolSize")?.getString()?.toInt() ?: 50
        val minIdle = environment.config.propertyOrNull("database.minimumIdle")?.getString()?.toInt() ?: 10
        val maxAcquireTimeMs = environment.config.propertyOrNull("database.maxAcquireTimeMs")?.getString()?.toLongOrNull() ?: 3000L
        val maxCreateConnectionTimeMs = environment.config.propertyOrNull("database.maxCreateConnectionTimeMs")?.getString()?.toLongOrNull() ?: 30000L
        
        // Parse JDBC URL to extract host, port, database
        // Format: jdbc:mysql://host:port/database?params
        val regex = Regex("""jdbc:mysql://([^:]+):(\d+)/([^?]+)""")
        val match = regex.find(jdbcUrl)
            ?: throw IllegalArgumentException("Invalid JDBC URL format: $jdbcUrl")
        
        val (host, port, database) = match.destructured
        
        logger.info("Initializing R2DBC connection pool - host: {}, port: {}, database: {}, maxSize: {}", 
            host, port, database, maxPoolSize)
        
        // Create MySQL connection factory
        val connectionFactory: ConnectionFactory = MySqlConnectionFactory.from(
            MySqlConnectionConfiguration.builder()
                .host(host)
                .port(port.toInt())
                .user(username)
                .password(password)
                .database(database)
                // Performance tuning
                .tcpKeepAlive(true)
                .tcpNoDelay(true)
                .build()
        )
        
        // Create connection pool.
        // When the pool is exhausted, new acquire() callers wait in a queue until a connection
        // is returned or maxAcquireTime elapses. This avoids "Too many connections" by not
        // creating more connections than maxSize; ensure maxSize <= MySQL max_connections.
        val poolConfig = ConnectionPoolConfiguration.builder(connectionFactory)
            .name("r2dbc-mysql-pool")
            .maxSize(maxPoolSize)
            .minIdle(minIdle)
            .maxIdleTime(Duration.ofMinutes(10))
            .maxLifeTime(Duration.ofMinutes(30))
            .maxAcquireTime(Duration.ofMillis(maxAcquireTimeMs))
            .maxCreateConnectionTime(Duration.ofMillis(maxCreateConnectionTimeMs))
            .acquireRetry(3)
            .build()
        
        connectionPool = ConnectionPool(poolConfig)
        
        // Warm up the pool
        connectionPool.warmup().block()
        
        logger.info("R2DBC connection pool initialized successfully")
    }
    
    /**
     * Get the connection pool for executing queries.
     */
    fun getConnectionPool(): ConnectionPool = connectionPool
    
    /**
     * Check if the database connection is healthy.
     * Executes a simple query to verify connectivity.
     * 
     * @return true if DB is reachable, false otherwise
     */
    suspend fun isHealthy(): Boolean {
        if (!::connectionPool.isInitialized) {
            return false
        }
        
        return try {
            // Use a simple validation query
            val result = Mono.from(connectionPool.create())
                .flatMap { connection ->
                    Mono.from(connection.validate(ValidationDepth.REMOTE))
                        .doFinally { connection.close() }
                }
                .awaitFirstOrNull()
            result == true
        } catch (e: Exception) {
            logger.warn("Database health check failed: ${e.message}")
            false
        }
    }
    
    /**
     * Close the connection pool gracefully.
     */
    fun close() {
        if (::connectionPool.isInitialized) {
            logger.info("Closing R2DBC connection pool")
            connectionPool.dispose()
        }
    }
}
