package com.discovery.repository

import com.discovery.models.*
import java.sql.ResultSet

class ProductRepository {

    fun findById(id: String): ProductDetail? {
        val product = findProductById(id) ?: return null
        val category = product.categoryId?.let { findCategoryById(it) }
        val variants = findVariantsByProductId(id)
        val media = findMediaByProductId(id)
        
        return ProductDetail.fromProduct(product, category, variants, media)
    }

    fun findByIds(ids: List<String>): List<ProductDetail> {
        if (ids.isEmpty()) return emptyList()
        
        val products = findProductsByIds(ids)
        if (products.isEmpty()) return emptyList()
        
        val productIds = products.map { it.id }
        val categoryIds = products.mapNotNull { it.categoryId }.distinct()
        
        val categories = if (categoryIds.isNotEmpty()) {
            findCategoriesByIds(categoryIds).associateBy { it.id }
        } else {
            emptyMap()
        }
        
        val variantsByProductId = findVariantsByProductIds(productIds).groupBy { it.productId }
        val mediaByProductId = findMediaByProductIds(productIds).groupBy { it.productId }
        
        return products.map { product ->
            ProductDetail.fromProduct(
                product = product,
                category = product.categoryId?.let { categories[it] },
                variants = variantsByProductId[product.id] ?: emptyList(),
                media = mediaByProductId[product.id] ?: emptyList()
            )
        }
    }

    private fun findProductById(id: String): Product? {
        val sql = """
            SELECT id, base_sku, name, description, features, status, 
                   source, source_sku, source_url, category_id, product_def_id, attributes
            FROM products WHERE id = ?
        """.trimIndent()
        
        return DatabaseFactory.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                stmt.setString(1, id)
                stmt.executeQuery().use { rs ->
                    if (rs.next()) mapToProduct(rs) else null
                }
            }
        }
    }

    private fun findProductsByIds(ids: List<String>): List<Product> {
        if (ids.isEmpty()) return emptyList()
        
        val placeholders = ids.joinToString(",") { "?" }
        val sql = """
            SELECT id, base_sku, name, description, features, status, 
                   source, source_sku, source_url, category_id, product_def_id, attributes
            FROM products WHERE id IN ($placeholders)
        """.trimIndent()
        
        return DatabaseFactory.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                ids.forEachIndexed { index, id ->
                    stmt.setString(index + 1, id)
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

    private fun findCategoryById(id: String): Category? {
        val sql = "SELECT id, name, description, product_def_id FROM categories WHERE id = ?"
        
        return DatabaseFactory.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                stmt.setString(1, id)
                stmt.executeQuery().use { rs ->
                    if (rs.next()) mapToCategory(rs) else null
                }
            }
        }
    }

    private fun findCategoriesByIds(ids: List<String>): List<Category> {
        if (ids.isEmpty()) return emptyList()
        
        val placeholders = ids.joinToString(",") { "?" }
        val sql = "SELECT id, name, description, product_def_id FROM categories WHERE id IN ($placeholders)"
        
        return DatabaseFactory.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                ids.forEachIndexed { index, id ->
                    stmt.setString(index + 1, id)
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

    private fun findVariantsByProductId(productId: String): List<ProductVariant> {
        val sql = """
            SELECT id, product_id, variant_sku, quantity, price, currency, attributes
            FROM product_variants WHERE product_id = ?
        """.trimIndent()
        
        return DatabaseFactory.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                stmt.setString(1, productId)
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

    private fun findVariantsByProductIds(productIds: List<String>): List<ProductVariant> {
        if (productIds.isEmpty()) return emptyList()
        
        val placeholders = productIds.joinToString(",") { "?" }
        val sql = """
            SELECT id, product_id, variant_sku, quantity, price, currency, attributes
            FROM product_variants WHERE product_id IN ($placeholders)
        """.trimIndent()
        
        return DatabaseFactory.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                productIds.forEachIndexed { index, id ->
                    stmt.setString(index + 1, id)
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

    private fun findMediaByProductId(productId: String): List<ProductMedia> {
        val sql = """
            SELECT id, product_id, variant_id, type, resolution, url
            FROM product_media WHERE product_id = ?
        """.trimIndent()
        
        return DatabaseFactory.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                stmt.setString(1, productId)
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

    private fun findMediaByProductIds(productIds: List<String>): List<ProductMedia> {
        if (productIds.isEmpty()) return emptyList()
        
        val placeholders = productIds.joinToString(",") { "?" }
        val sql = """
            SELECT id, product_id, variant_id, type, resolution, url
            FROM product_media WHERE product_id IN ($placeholders)
        """.trimIndent()
        
        return DatabaseFactory.getConnection().use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                productIds.forEachIndexed { index, id ->
                    stmt.setString(index + 1, id)
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

    private fun mapToProduct(rs: ResultSet): Product {
        return Product(
            id = rs.getString("id"),
            baseSku = rs.getString("base_sku"),
            name = rs.getString("name"),
            description = rs.getString("description"),
            features = rs.getString("features"),
            status = rs.getString("status"),
            source = rs.getString("source"),
            sourceSku = rs.getString("source_sku"),
            sourceUrl = rs.getString("source_url"),
            categoryId = rs.getString("category_id"),
            productDefId = rs.getString("product_def_id"),
            attributes = rs.getString("attributes")
        )
    }

    private fun mapToCategory(rs: ResultSet): Category {
        return Category(
            id = rs.getString("id"),
            name = rs.getString("name"),
            description = rs.getString("description"),
            productDefId = rs.getString("product_def_id")
        )
    }

    private fun mapToProductVariant(rs: ResultSet): ProductVariant {
        return ProductVariant(
            id = rs.getString("id"),
            productId = rs.getString("product_id"),
            variantSku = rs.getString("variant_sku"),
            quantity = rs.getInt("quantity"),
            price = rs.getDouble("price"),
            currency = rs.getString("currency"),
            attributes = rs.getString("attributes")
        )
    }

    private fun mapToProductMedia(rs: ResultSet): ProductMedia {
        return ProductMedia(
            id = rs.getString("id"),
            productId = rs.getString("product_id"),
            variantId = rs.getString("variant_id"),
            type = rs.getString("type"),
            resolution = rs.getString("resolution"),
            url = rs.getString("url")
        )
    }
}

