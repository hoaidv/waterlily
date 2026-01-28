package com.discovery.tools

import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import java.io.File

/**
 * Extracts random product IDs from the database for benchmark testing.
 * 
 * Usage: ./gradlew extractProductIds -PproductCount=1000000 -PresultFile=experiment/product_ids.txt
 */
object ExtractProductIds {
    
    @JvmStatic
    fun main(args: Array<String>) {
        val productCount = args.getOrNull(0)?.toIntOrNull() ?: 1_000_000
        val resultFile = args.getOrNull(1) ?: "experiment/product_ids.txt"
        
        println("Extracting $productCount product IDs to $resultFile")
        
        // Load database config
        val configFile = File("experiment/mysql-config.json")
        if (!configFile.exists()) {
            System.err.println("Error: experiment/mysql-config.json not found")
            System.exit(1)
        }
        
        val configJson = Json.parseToJsonElement(configFile.readText()).jsonObject
        val host = configJson["host"]?.jsonPrimitive?.content ?: "localhost"
        val port = configJson["port"]?.jsonPrimitive?.content?.toIntOrNull() ?: 3306
        val database = configJson["database"]?.jsonPrimitive?.content ?: "ecommerce"
        val username = configJson["user"]?.jsonPrimitive?.content ?: "root"
        val password = configJson["password"]?.jsonPrimitive?.content ?: ""
        
        val jdbcUrl = "jdbc:mysql://$host:$port/$database"
        
        // Create connection pool
        val hikariConfig = HikariConfig().apply {
            this.jdbcUrl = jdbcUrl
            this.username = username
            this.password = password
            maximumPoolSize = 5
            minimumIdle = 1
        }
        
        val dataSource = HikariDataSource(hikariConfig)
        
        try {
            dataSource.connection.use { conn ->
                println("Connected to database: $jdbcUrl")
                
                // For large datasets, ORDER BY RAND() is slow
                // Use a more efficient approach: get max ID and sample
                val countSql = "SELECT COUNT(*) as cnt FROM products"
                val totalProducts = conn.prepareStatement(countSql).use { stmt ->
                    stmt.executeQuery().use { rs ->
                        if (rs.next()) rs.getLong("cnt") else 0L
                    }
                }
                
                println("Total products in database: $totalProducts")
                
                if (totalProducts == 0L) {
                    System.err.println("Error: No products found in database")
                    System.exit(1)
                }
                
                val actualCount = minOf(productCount, totalProducts.toInt())
                println("Extracting $actualCount product IDs...")
                
                // Use LIMIT with random offset or just get all IDs and sample
                // For best randomness with large datasets, we'll fetch IDs in batches
                val ids = mutableSetOf<Long>()
                val batchSize = 100_000
                
                if (actualCount <= totalProducts / 2) {
                    // Sample using ORDER BY RAND() with LIMIT - acceptable for smaller samples
                    val sql = "SELECT id FROM products ORDER BY RAND() LIMIT ?"
                    conn.prepareStatement(sql).use { stmt ->
                        stmt.setInt(1, actualCount)
                        stmt.executeQuery().use { rs ->
                            while (rs.next()) {
                                ids.add(rs.getLong("id"))
                            }
                        }
                    }
                } else {
                    // Get all IDs and shuffle locally (more efficient for large samples)
                    val sql = "SELECT id FROM products"
                    val allIds = mutableListOf<Long>()
                    conn.prepareStatement(sql).use { stmt ->
                        stmt.executeQuery().use { rs ->
                            while (rs.next()) {
                                allIds.add(rs.getLong("id"))
                            }
                        }
                    }
                    allIds.shuffle()
                    ids.addAll(allIds.take(actualCount))
                }
                
                println("Extracted ${ids.size} product IDs")
                
                // Write to file
                val outputFile = File(resultFile)
                outputFile.parentFile?.mkdirs()
                outputFile.bufferedWriter().use { writer ->
                    ids.forEach { id ->
                        writer.write(id.toString())
                        writer.newLine()
                    }
                }
                
                println("Wrote ${ids.size} IDs to $resultFile")
            }
        } finally {
            dataSource.close()
        }
    }
}
