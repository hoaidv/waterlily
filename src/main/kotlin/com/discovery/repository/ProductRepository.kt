package com.discovery.repository

import com.discovery.config.R2dbcConfig
import com.discovery.model.*
import io.r2dbc.spi.Row
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.reactive.asFlow
import kotlinx.coroutines.reactive.awaitFirstOrNull
import reactor.core.publisher.Flux

/**
 * Product repository using R2DBC for true non-blocking database access.
 * 
 * R2DBC (Reactive Relational Database Connectivity) provides:
 * - Non-blocking I/O: No thread blocking while waiting for DB responses
 * - Backpressure: Handles flow control between app and database
 * - Coroutine integration: Via kotlinx-coroutines-reactor
 * 
 * This allows handling thousands of concurrent requests without
 * blocking any threads, including Netty event loop threads.
 */
class ProductRepository {

    private val pool get() = R2dbcConfig.getConnectionPool()

    /**
     * Find a product by ID with all related details.
     * Fully non-blocking - no threads are blocked during execution.
     */
    suspend fun findById(id: Long): ProductDetail? {
        val product = findProductById(id) ?: return null
        
        // Fetch related data concurrently (all non-blocking)
        return coroutineScope {
            val categoryDeferred = async { 
                product.categoryId?.let { findCategoryById(it) } 
            }
            val variantsDeferred = async { findVariantsByProductId(id) }
            val mediaDeferred = async { findMediaByProductId(id) }
            
            ProductDetail.fromProduct(
                product = product,
                category = categoryDeferred.await(),
                variants = variantsDeferred.await(),
                media = mediaDeferred.await()
            )
        }
    }

    /**
     * Find multiple products by IDs with all related details.
     * Fully non-blocking with concurrent fetching of related data.
     */
    suspend fun findByIds(ids: List<Long>): List<ProductDetail> {
        if (ids.isEmpty()) return emptyList()
        
        val products = findProductsByIds(ids)
        if (products.isEmpty()) return emptyList()
        
        val productIds = products.map { it.id }
        val categoryIds = products.mapNotNull { it.categoryId }.distinct()
        
        // Fetch all related data concurrently (all non-blocking)
        return coroutineScope {
            val categoriesDeferred = async {
                if (categoryIds.isNotEmpty()) {
                    findCategoriesByIds(categoryIds).associateBy { it.id }
                } else {
                    emptyMap()
                }
            }
            val variantsDeferred = async { 
                findVariantsByProductIds(productIds).groupBy { it.productId } 
            }
            val mediaDeferred = async { 
                findMediaByProductIds(productIds).groupBy { it.productId } 
            }
            
            val categories = categoriesDeferred.await()
            val variantsByProductId = variantsDeferred.await()
            val mediaByProductId = mediaDeferred.await()
            
            products.map { product ->
                ProductDetail.fromProduct(
                    product = product,
                    category = product.categoryId?.let { categories[it] },
                    variants = variantsByProductId[product.id] ?: emptyList(),
                    media = mediaByProductId[product.id] ?: emptyList()
                )
            }
        }
    }

    private suspend fun findProductById(id: Long): Product? {
        val sql = """
            SELECT id, base_sku, name, description, features, status, 
                   source, source_sku, source_url, category_id, attributes
            FROM products WHERE id = ?
        """.trimIndent()
        
        return Flux.usingWhen(
            pool.create(),
            { conn ->
                Flux.from(conn.createStatement(sql)
                    .bind(0, id)
                    .execute())
                    .flatMap { result ->
                        result.map { row, _ -> mapToProduct(row) }
                    }
            },
            { conn -> conn.close() }
        ).awaitFirstOrNull()
    }

    private suspend fun findProductsByIds(ids: List<Long>): List<Product> {
        if (ids.isEmpty()) return emptyList()
        
        val placeholders = ids.indices.joinToString(",") { "?" }
        val sql = """
            SELECT id, base_sku, name, description, features, status, 
                   source, source_sku, source_url, category_id, attributes
            FROM products WHERE id IN ($placeholders)
        """.trimIndent()
        
        return Flux.usingWhen(
            pool.create(),
            { conn ->
                val statement = conn.createStatement(sql)
                ids.forEachIndexed { index, id ->
                    statement.bind(index, id)
                }
                Flux.from(statement.execute())
                    .flatMap { result ->
                        result.map { row, _ -> mapToProduct(row) }
                    }
            },
            { conn -> conn.close() }
        ).asFlow().toList()
    }

    private suspend fun findCategoryById(id: Long): Category? {
        val sql = "SELECT id, name, description FROM categories WHERE id = ?"
        
        return Flux.usingWhen(
            pool.create(),
            { conn ->
                Flux.from(conn.createStatement(sql)
                    .bind(0, id)
                    .execute())
                    .flatMap { result ->
                        result.map { row, _ -> mapToCategory(row) }
                    }
            },
            { conn -> conn.close() }
        ).awaitFirstOrNull()
    }

    private suspend fun findCategoriesByIds(ids: List<Long>): List<Category> {
        if (ids.isEmpty()) return emptyList()
        
        val placeholders = ids.indices.joinToString(",") { "?" }
        val sql = "SELECT id, name, description FROM categories WHERE id IN ($placeholders)"
        
        return Flux.usingWhen(
            pool.create(),
            { conn ->
                val statement = conn.createStatement(sql)
                ids.forEachIndexed { index, id ->
                    statement.bind(index, id)
                }
                Flux.from(statement.execute())
                    .flatMap { result ->
                        result.map { row, _ -> mapToCategory(row) }
                    }
            },
            { conn -> conn.close() }
        ).asFlow().toList()
    }

    private suspend fun findVariantsByProductId(productId: Long): List<ProductVariant> {
        val sql = """
            SELECT id, product_id, variant_sku, quantity, price, currency, attributes
            FROM product_variants WHERE product_id = ?
        """.trimIndent()
        
        return Flux.usingWhen(
            pool.create(),
            { conn ->
                Flux.from(conn.createStatement(sql)
                    .bind(0, productId)
                    .execute())
                    .flatMap { result ->
                        result.map { row, _ -> mapToProductVariant(row) }
                    }
            },
            { conn -> conn.close() }
        ).asFlow().toList()
    }

    private suspend fun findVariantsByProductIds(productIds: List<Long>): List<ProductVariant> {
        if (productIds.isEmpty()) return emptyList()
        
        val placeholders = productIds.indices.joinToString(",") { "?" }
        val sql = """
            SELECT id, product_id, variant_sku, quantity, price, currency, attributes
            FROM product_variants WHERE product_id IN ($placeholders)
        """.trimIndent()
        
        return Flux.usingWhen(
            pool.create(),
            { conn ->
                val statement = conn.createStatement(sql)
                productIds.forEachIndexed { index, id ->
                    statement.bind(index, id)
                }
                Flux.from(statement.execute())
                    .flatMap { result ->
                        result.map { row, _ -> mapToProductVariant(row) }
                    }
            },
            { conn -> conn.close() }
        ).asFlow().toList()
    }

    private suspend fun findMediaByProductId(productId: Long): List<ProductMedia> {
        val sql = """
            SELECT id, product_id, variant_id, type, resolution, url
            FROM product_media WHERE product_id = ?
        """.trimIndent()
        
        return Flux.usingWhen(
            pool.create(),
            { conn ->
                Flux.from(conn.createStatement(sql)
                    .bind(0, productId)
                    .execute())
                    .flatMap { result ->
                        result.map { row, _ -> mapToProductMedia(row) }
                    }
            },
            { conn -> conn.close() }
        ).asFlow().toList()
    }

    private suspend fun findMediaByProductIds(productIds: List<Long>): List<ProductMedia> {
        if (productIds.isEmpty()) return emptyList()
        
        val placeholders = productIds.indices.joinToString(",") { "?" }
        val sql = """
            SELECT id, product_id, variant_id, type, resolution, url
            FROM product_media WHERE product_id IN ($placeholders)
        """.trimIndent()
        
        return Flux.usingWhen(
            pool.create(),
            { conn ->
                val statement = conn.createStatement(sql)
                productIds.forEachIndexed { index, id ->
                    statement.bind(index, id)
                }
                Flux.from(statement.execute())
                    .flatMap { result ->
                        result.map { row, _ -> mapToProductMedia(row) }
                    }
            },
            { conn -> conn.close() }
        ).asFlow().toList()
    }

    // Row mappers for R2DBC
    
    private fun mapToProduct(row: Row): Product {
        return Product(
            id = row.get("id", java.lang.Long::class.java)?.toLong() ?: 0L,
            baseSku = row.get("base_sku", String::class.java),
            name = row.get("name", String::class.java),
            description = row.get("description", String::class.java),
            features = row.get("features", String::class.java),
            status = row.get("status", String::class.java),
            source = row.get("source", String::class.java),
            sourceSku = row.get("source_sku", String::class.java),
            sourceUrl = row.get("source_url", String::class.java),
            categoryId = row.get("category_id", java.lang.Long::class.java)?.toLong(),
            attributes = row.get("attributes", String::class.java)
        )
    }

    private fun mapToCategory(row: Row): Category {
        return Category(
            id = row.get("id", java.lang.Long::class.java)?.toLong() ?: 0L,
            name = row.get("name", String::class.java),
            description = row.get("description", String::class.java)
        )
    }

    private fun mapToProductVariant(row: Row): ProductVariant {
        return ProductVariant(
            id = row.get("id", java.lang.Long::class.java)?.toLong() ?: 0L,
            productId = row.get("product_id", java.lang.Long::class.java)?.toLong() ?: 0L,
            variantSku = row.get("variant_sku", String::class.java),
            quantity = row.get("quantity", java.lang.Integer::class.java)?.toInt() ?: 0,
            price = row.get("price", java.lang.Double::class.java)?.toDouble() ?: 0.0,
            currency = row.get("currency", String::class.java) ?: "USD",
            attributes = row.get("attributes", String::class.java)
        )
    }

    private fun mapToProductMedia(row: Row): ProductMedia {
        return ProductMedia(
            id = row.get("id", java.lang.Long::class.java)?.toLong() ?: 0L,
            productId = row.get("product_id", java.lang.Long::class.java)?.toLong() ?: 0L,
            variantId = row.get("variant_id", java.lang.Long::class.java)?.toLong(),
            type = row.get("type", String::class.java),
            resolution = row.get("resolution", String::class.java),
            url = row.get("url", String::class.java)
        )
    }
}
