package com.discovery.repository

import com.discovery.config.DatabaseConfig
import com.discovery.model.*
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject
import java.math.BigDecimal
import java.sql.ResultSet

class ProductRepository {
    
    private val json = Json { ignoreUnknownKeys = true }
    
    fun findById(id: Long): Product? {
        DatabaseConfig.getConnection().use { conn ->
            val sql = """
                SELECT id, base_sku, name, description, features, status, 
                       source, source_sku, source_url, category_id, attributes
                FROM products 
                WHERE id = ?
            """.trimIndent()
            
            conn.prepareStatement(sql).use { stmt ->
                stmt.setLong(1, id)
                stmt.executeQuery().use { rs ->
                    return if (rs.next()) rs.toProduct() else null
                }
            }
        }
    }
    
    fun findByIds(ids: List<Long>): List<Product> {
        if (ids.isEmpty()) return emptyList()
        
        DatabaseConfig.getConnection().use { conn ->
            val placeholders = ids.joinToString(",") { "?" }
            val sql = """
                SELECT id, base_sku, name, description, features, status, 
                       source, source_sku, source_url, category_id, attributes
                FROM products 
                WHERE id IN ($placeholders)
            """.trimIndent()
            
            conn.prepareStatement(sql).use { stmt ->
                ids.forEachIndexed { index, id ->
                    stmt.setLong(index + 1, id)
                }
                stmt.executeQuery().use { rs ->
                    val products = mutableListOf<Product>()
                    while (rs.next()) {
                        products.add(rs.toProduct())
                    }
                    // Maintain order consistent with input IDs
                    val productMap = products.associateBy { it.id }
                    return ids.mapNotNull { productMap[it] }
                }
            }
        }
    }
    
    fun findCategoryById(id: Long): Category? {
        DatabaseConfig.getConnection().use { conn ->
            val sql = "SELECT id, name, description FROM categories WHERE id = ?"
            
            conn.prepareStatement(sql).use { stmt ->
                stmt.setLong(1, id)
                stmt.executeQuery().use { rs ->
                    return if (rs.next()) rs.toCategory() else null
                }
            }
        }
    }
    
    fun findCategoriesByIds(ids: Set<Long>): Map<Long, Category> {
        if (ids.isEmpty()) return emptyMap()
        
        DatabaseConfig.getConnection().use { conn ->
            val placeholders = ids.joinToString(",") { "?" }
            val sql = "SELECT id, name, description FROM categories WHERE id IN ($placeholders)"
            
            conn.prepareStatement(sql).use { stmt ->
                ids.forEachIndexed { index, id ->
                    stmt.setLong(index + 1, id)
                }
                stmt.executeQuery().use { rs ->
                    val categories = mutableMapOf<Long, Category>()
                    while (rs.next()) {
                        val category = rs.toCategory()
                        categories[category.id] = category
                    }
                    return categories
                }
            }
        }
    }
    
    fun findVariantsByProductId(productId: Long): List<ProductVariant> {
        DatabaseConfig.getConnection().use { conn ->
            val sql = """
                SELECT id, product_id, variant_sku, quantity, price, currency, attributes
                FROM product_variants 
                WHERE product_id = ?
            """.trimIndent()
            
            conn.prepareStatement(sql).use { stmt ->
                stmt.setLong(1, productId)
                stmt.executeQuery().use { rs ->
                    val variants = mutableListOf<ProductVariant>()
                    while (rs.next()) {
                        variants.add(rs.toProductVariant())
                    }
                    return variants
                }
            }
        }
    }
    
    fun findVariantsByProductIds(productIds: List<Long>): Map<Long, List<ProductVariant>> {
        if (productIds.isEmpty()) return emptyMap()
        
        DatabaseConfig.getConnection().use { conn ->
            val placeholders = productIds.joinToString(",") { "?" }
            val sql = """
                SELECT id, product_id, variant_sku, quantity, price, currency, attributes
                FROM product_variants 
                WHERE product_id IN ($placeholders)
            """.trimIndent()
            
            conn.prepareStatement(sql).use { stmt ->
                productIds.forEachIndexed { index, id ->
                    stmt.setLong(index + 1, id)
                }
                stmt.executeQuery().use { rs ->
                    val variantsByProduct = mutableMapOf<Long, MutableList<ProductVariant>>()
                    while (rs.next()) {
                        val variant = rs.toProductVariant()
                        variantsByProduct.getOrPut(variant.productId) { mutableListOf() }.add(variant)
                    }
                    return variantsByProduct
                }
            }
        }
    }
    
    fun findMediaByProductId(productId: Long): List<ProductMedia> {
        DatabaseConfig.getConnection().use { conn ->
            val sql = """
                SELECT id, product_id, variant_id, type, resolution, url
                FROM product_media 
                WHERE product_id = ?
            """.trimIndent()
            
            conn.prepareStatement(sql).use { stmt ->
                stmt.setLong(1, productId)
                stmt.executeQuery().use { rs ->
                    val media = mutableListOf<ProductMedia>()
                    while (rs.next()) {
                        media.add(rs.toProductMedia())
                    }
                    return media
                }
            }
        }
    }
    
    fun findMediaByProductIds(productIds: List<Long>): Map<Long, List<ProductMedia>> {
        if (productIds.isEmpty()) return emptyMap()
        
        DatabaseConfig.getConnection().use { conn ->
            val placeholders = productIds.joinToString(",") { "?" }
            val sql = """
                SELECT id, product_id, variant_id, type, resolution, url
                FROM product_media 
                WHERE product_id IN ($placeholders)
            """.trimIndent()
            
            conn.prepareStatement(sql).use { stmt ->
                productIds.forEachIndexed { index, id ->
                    stmt.setLong(index + 1, id)
                }
                stmt.executeQuery().use { rs ->
                    val mediaByProduct = mutableMapOf<Long, MutableList<ProductMedia>>()
                    while (rs.next()) {
                        val media = rs.toProductMedia()
                        mediaByProduct.getOrPut(media.productId) { mutableListOf() }.add(media)
                    }
                    return mediaByProduct
                }
            }
        }
    }
    
    fun getRandomProductIds(count: Int): List<Long> {
        DatabaseConfig.getConnection().use { conn ->
            val sql = "SELECT id FROM products ORDER BY RAND() LIMIT ?"
            
            conn.prepareStatement(sql).use { stmt ->
                stmt.setInt(1, count)
                stmt.executeQuery().use { rs ->
                    val ids = mutableListOf<Long>()
                    while (rs.next()) {
                        ids.add(rs.getLong("id"))
                    }
                    return ids
                }
            }
        }
    }
    
    // Extension functions for ResultSet mapping
    
    private fun ResultSet.toProduct(): Product {
        return Product(
            id = getLong("id"),
            baseSku = getString("base_sku"),
            name = getString("name"),
            description = getString("description"),
            features = getString("features")?.let { parseJsonArray(it) },
            status = getString("status"),
            source = getString("source"),
            sourceSku = getString("source_sku"),
            sourceUrl = getString("source_url"),
            categoryId = getLong("category_id"),
            attributes = getString("attributes")?.let { parseJsonObject(it) }
        )
    }
    
    private fun ResultSet.toCategory(): Category {
        return Category(
            id = getLong("id"),
            name = getString("name"),
            description = getString("description")
        )
    }
    
    private fun ResultSet.toProductVariant(): ProductVariant {
        return ProductVariant(
            id = getLong("id"),
            productId = getLong("product_id"),
            variantSku = getString("variant_sku"),
            quantity = getInt("quantity"),
            price = getBigDecimal("price") ?: BigDecimal.ZERO,
            currency = getString("currency") ?: "USD",
            attributes = getString("attributes")?.let { parseJsonObject(it) }
        )
    }
    
    private fun ResultSet.toProductMedia(): ProductMedia {
        return ProductMedia(
            id = getLong("id"),
            productId = getLong("product_id"),
            variantId = getLong("variant_id").takeIf { !wasNull() },
            type = getString("type"),
            resolution = getString("resolution"),
            url = getString("url")
        )
    }
    
    private fun parseJsonArray(jsonString: String): JsonArray? {
        return try {
            json.decodeFromString<JsonArray>(jsonString)
        } catch (e: Exception) {
            null
        }
    }
    
    private fun parseJsonObject(jsonString: String): JsonObject? {
        return try {
            json.decodeFromString<JsonObject>(jsonString)
        } catch (e: Exception) {
            null
        }
    }
}
