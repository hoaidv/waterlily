package com.discovery.repository

import com.discovery.config.DatabaseConfig
import com.discovery.config.DatabaseDispatcher
import com.discovery.model.*
import kotlinx.coroutines.withContext
import java.sql.ResultSet

class ProductRepository {

    /**
     * Find a product by ID with all related details.
     * 
     * This is a suspend function that offloads blocking JDBC operations
     * to the DatabaseDispatcher, keeping Netty worker threads free.
     */
    suspend fun findById(id: Long): ProductDetail? = withContext(DatabaseDispatcher.get()) {
        val product = findProductById(id) ?: return@withContext null
        val category = product.categoryId?.let { findCategoryById(it) }
        val variants = findVariantsByProductId(id)
        val media = findMediaByProductId(id)
        
        ProductDetail.fromProduct(product, category, variants, media)
    }

    /**
     * Find multiple products by IDs with all related details.
     * 
     * This is a suspend function that offloads blocking JDBC operations
     * to the DatabaseDispatcher, keeping Netty worker threads free.
     */
    suspend fun findByIds(ids: List<Long>): List<ProductDetail> = withContext(DatabaseDispatcher.get()) {
        if (ids.isEmpty()) return@withContext emptyList()
        
        val products = findProductsByIds(ids)
        if (products.isEmpty()) return@withContext emptyList()
        
        val productIds = products.map { it.id }
        val categoryIds = products.mapNotNull { it.categoryId }.distinct()
        
        val categories = if (categoryIds.isNotEmpty()) {
            findCategoriesByIds(categoryIds).associateBy { it.id }
        } else {
            emptyMap()
        }
        
        val variantsByProductId = findVariantsByProductIds(productIds).groupBy { it.productId }
        val mediaByProductId = findMediaByProductIds(productIds).groupBy { it.productId }
        
        products.map { product ->
            ProductDetail.fromProduct(
                product = product,
                category = product.categoryId?.let { categories[it] },
                variants = variantsByProductId[product.id] ?: emptyList(),
                media = mediaByProductId[product.id] ?: emptyList()
            )
        }
    }

    private fun findProductById(id: Long): Product? {
        val sql = """
            SELECT id, base_sku, name, description, features, status, 
                   source, source_sku, source_url, category_id, attributes
            FROM products WHERE id = ?
        """.trimIndent()
        
        return DatabaseConfig.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                stmt.setLong(1, id)
                stmt.executeQuery().use { rs ->
                    if (rs.next()) mapToProduct(rs) else null
                }
            }
        }
    }

    private fun findProductsByIds(ids: List<Long>): List<Product> {
        if (ids.isEmpty()) return emptyList()
        
        val placeholders = ids.joinToString(",") { "?" }
        val sql = """
            SELECT id, base_sku, name, description, features, status, 
                   source, source_sku, source_url, category_id, attributes
            FROM products WHERE id IN ($placeholders)
        """.trimIndent()
        
        return DatabaseConfig.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                ids.forEachIndexed { index, id ->
                    stmt.setLong(index + 1, id)
                }
                stmt.executeQuery().use { rs ->
                    val products = mutableListOf<Product>()
                    while (rs.next()) {
                        products.add(mapToProduct(rs))
                    }
                    products
                }
            }
        }
    }

    private fun findCategoryById(id: Long): Category? {
        val sql = "SELECT id, name, description FROM categories WHERE id = ?"
        
        return DatabaseConfig.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                stmt.setLong(1, id)
                stmt.executeQuery().use { rs ->
                    if (rs.next()) mapToCategory(rs) else null
                }
            }
        }
    }

    private fun findCategoriesByIds(ids: List<Long>): List<Category> {
        if (ids.isEmpty()) return emptyList()
        
        val placeholders = ids.joinToString(",") { "?" }
        val sql = "SELECT id, name, description FROM categories WHERE id IN ($placeholders)"
        
        return DatabaseConfig.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                ids.forEachIndexed { index, id ->
                    stmt.setLong(index + 1, id)
                }
                stmt.executeQuery().use { rs ->
                    val categories = mutableListOf<Category>()
                    while (rs.next()) {
                        categories.add(mapToCategory(rs))
                    }
                    categories
                }
            }
        }
    }

    private fun findVariantsByProductId(productId: Long): List<ProductVariant> {
        val sql = """
            SELECT id, product_id, variant_sku, quantity, price, currency, attributes
            FROM product_variants WHERE product_id = ?
        """.trimIndent()
        
        return DatabaseConfig.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                stmt.setLong(1, productId)
                stmt.executeQuery().use { rs ->
                    val variants = mutableListOf<ProductVariant>()
                    while (rs.next()) {
                        variants.add(mapToProductVariant(rs))
                    }
                    variants
                }
            }
        }
    }

    private fun findVariantsByProductIds(productIds: List<Long>): List<ProductVariant> {
        if (productIds.isEmpty()) return emptyList()
        
        val placeholders = productIds.joinToString(",") { "?" }
        val sql = """
            SELECT id, product_id, variant_sku, quantity, price, currency, attributes
            FROM product_variants WHERE product_id IN ($placeholders)
        """.trimIndent()
        
        return DatabaseConfig.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                productIds.forEachIndexed { index, id ->
                    stmt.setLong(index + 1, id)
                }
                stmt.executeQuery().use { rs ->
                    val variants = mutableListOf<ProductVariant>()
                    while (rs.next()) {
                        variants.add(mapToProductVariant(rs))
                    }
                    variants
                }
            }
        }
    }

    private fun findMediaByProductId(productId: Long): List<ProductMedia> {
        val sql = """
            SELECT id, product_id, variant_id, type, resolution, url
            FROM product_media WHERE product_id = ?
        """.trimIndent()
        
        return DatabaseConfig.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                stmt.setLong(1, productId)
                stmt.executeQuery().use { rs ->
                    val media = mutableListOf<ProductMedia>()
                    while (rs.next()) {
                        media.add(mapToProductMedia(rs))
                    }
                    media
                }
            }
        }
    }

    private fun findMediaByProductIds(productIds: List<Long>): List<ProductMedia> {
        if (productIds.isEmpty()) return emptyList()
        
        val placeholders = productIds.joinToString(",") { "?" }
        val sql = """
            SELECT id, product_id, variant_id, type, resolution, url
            FROM product_media WHERE product_id IN ($placeholders)
        """.trimIndent()
        
        return DatabaseConfig.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                productIds.forEachIndexed { index, id ->
                    stmt.setLong(index + 1, id)
                }
                stmt.executeQuery().use { rs ->
                    val media = mutableListOf<ProductMedia>()
                    while (rs.next()) {
                        media.add(mapToProductMedia(rs))
                    }
                    media
                }
            }
        }
    }

    fun getRandomProductIds(count: Int): List<Long> {
        val sql = "SELECT id FROM products ORDER BY RAND() LIMIT ?"
        
        return DatabaseConfig.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                stmt.setInt(1, count)
                stmt.executeQuery().use { rs ->
                    val ids = mutableListOf<Long>()
                    while (rs.next()) {
                        ids.add(rs.getLong("id"))
                    }
                    ids
                }
            }
        }
    }

    private fun mapToProduct(rs: ResultSet): Product {
        return Product(
            id = rs.getLong("id"),
            baseSku = rs.getString("base_sku"),
            name = rs.getString("name"),
            description = rs.getString("description"),
            features = rs.getString("features"),
            status = rs.getString("status"),
            source = rs.getString("source"),
            sourceSku = rs.getString("source_sku"),
            sourceUrl = rs.getString("source_url"),
            categoryId = rs.getLong("category_id").takeIf { !rs.wasNull() },
            attributes = rs.getString("attributes")
        )
    }

    private fun mapToCategory(rs: ResultSet): Category {
        return Category(
            id = rs.getLong("id"),
            name = rs.getString("name"),
            description = rs.getString("description")
        )
    }

    private fun mapToProductVariant(rs: ResultSet): ProductVariant {
        return ProductVariant(
            id = rs.getLong("id"),
            productId = rs.getLong("product_id"),
            variantSku = rs.getString("variant_sku"),
            quantity = rs.getInt("quantity"),
            price = rs.getDouble("price"),
            currency = rs.getString("currency") ?: "USD",
            attributes = rs.getString("attributes")
        )
    }

    private fun mapToProductMedia(rs: ResultSet): ProductMedia {
        return ProductMedia(
            id = rs.getLong("id"),
            productId = rs.getLong("product_id"),
            variantId = rs.getLong("variant_id").takeIf { !rs.wasNull() },
            type = rs.getString("type"),
            resolution = rs.getString("resolution"),
            url = rs.getString("url")
        )
    }
}
