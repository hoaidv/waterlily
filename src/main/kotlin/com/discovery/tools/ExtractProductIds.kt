package com.discovery.tools

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import java.io.File
import java.sql.DriverManager

/**
 * Standalone utility to extract product IDs from the database
 * for use in benchmark scripts.
 * 
 * Usage: Run with gradle or IDE
 *   ./gradlew run --args="extract-ids [count] [output-file]"
 * 
 * Or run this main function directly from IDE.
 */
object ExtractProductIds {
    
    private const val DEFAULT_COUNT = 10000
    private const val DEFAULT_OUTPUT = "experiment/product_ids.txt"
    
    @JvmStatic
    fun main(args: Array<String>) {
        val count = args.getOrNull(0)?.toIntOrNull() ?: DEFAULT_COUNT
        val outputFile = args.getOrNull(1) ?: DEFAULT_OUTPUT
        
        println("Extracting $count product IDs to $outputFile")
        
        // Load database config
        val configFile = File("experiment/mysql-config.json")
        if (!configFile.exists()) {
            println("Error: mysql-config.json not found at experiment/mysql-config.json")
            return
        }
        
        val config = Json.parseToJsonElement(configFile.readText()).jsonObject
        val host = config["host"]?.jsonPrimitive?.content ?: "localhost"
        val port = config["port"]?.jsonPrimitive?.content ?: "3306"
        val database = config["database"]?.jsonPrimitive?.content ?: "ecommerce"
        val user = config["user"]?.jsonPrimitive?.content ?: "root"
        val password = config["password"]?.jsonPrimitive?.content ?: ""
        
        val jdbcUrl = "jdbc:mysql://$host:$port/$database?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true"
        
        println("Connecting to database: $jdbcUrl")
        
        try {
            // Load MySQL driver
            Class.forName("com.mysql.cj.jdbc.Driver")
            
            DriverManager.getConnection(jdbcUrl, user, password).use { conn ->
                // Get total count first
                val countSql = "SELECT COUNT(*) FROM products"
                val totalCount = conn.createStatement().use { stmt ->
                    stmt.executeQuery(countSql).use { rs ->
                        if (rs.next()) rs.getInt(1) else 0
                    }
                }
                println("Total products in database: $totalCount")
                
                // Extract IDs with random sampling for better distribution
                val sql = if (totalCount > count * 2) {
                    // Use random sampling for large datasets
                    """
                        SELECT id FROM products 
                        ORDER BY RAND() 
                        LIMIT ?
                    """.trimIndent()
                } else {
                    // Simple selection for smaller datasets
                    "SELECT id FROM products LIMIT ?"
                }
                
                val ids = mutableListOf<String>()
                
                conn.prepareStatement(sql).use { stmt ->
                    stmt.setInt(1, count)
                    stmt.executeQuery().use { rs ->
                        while (rs.next()) {
                            ids.add(rs.getString("id"))
                        }
                    }
                }
                
                println("Extracted ${ids.size} product IDs")
                
                // Write to file
                val file = File(outputFile)
                file.parentFile?.mkdirs()
                file.writeText(ids.joinToString("\n"))
                
                println("Product IDs saved to: ${file.absolutePath}")
            }
        } catch (e: Exception) {
            println("Error: ${e.message}")
            e.printStackTrace()
        }
    }
}

