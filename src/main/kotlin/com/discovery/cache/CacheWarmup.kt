package com.discovery.cache

import org.slf4j.LoggerFactory
import java.io.File

/**
 * Utility for reading product IDs from a file for cache warmup.
 */
object CacheWarmup {
    private val log = LoggerFactory.getLogger(CacheWarmup::class.java)

    /**
     * Read product IDs from a file, one ID per line.
     * 
     * @param filePath Path to the file containing product IDs
     * @param limit Maximum number of IDs to read (usually cache maxSize)
     * @return List of product IDs, or empty list if file not found or error
     */
    fun readProductIds(filePath: String, limit: Long): List<Long> {
        val file = File(filePath)
        
        if (!file.exists()) {
            log.warn("Product IDs file not found: $filePath")
            return emptyList()
        }
        
        if (!file.isFile) {
            log.warn("Product IDs path is not a file: $filePath")
            return emptyList()
        }

        return try {
            val ids = mutableListOf<Long>()
            var lineNumber = 0
            var invalidLines = 0
            
            file.bufferedReader().useLines { lines ->
                for (line in lines) {
                    if (ids.size >= limit) break
                    lineNumber++
                    
                    val trimmed = line.trim()
                    if (trimmed.isEmpty()) continue
                    
                    val id = trimmed.toLongOrNull()
                    if (id != null) {
                        ids.add(id)
                    } else {
                        invalidLines++
                        if (invalidLines <= 5) {
                            log.warn("Invalid product ID at line $lineNumber: '$trimmed'")
                        }
                    }
                }
            }
            
            if (invalidLines > 5) {
                log.warn("... and ${invalidLines - 5} more invalid lines")
            }
            
            log.info("Read ${ids.size} product IDs from $filePath (limit: $limit)")
            ids
        } catch (e: Exception) {
            log.error("Error reading product IDs from $filePath: ${e.message}", e)
            emptyList()
        }
    }
}
