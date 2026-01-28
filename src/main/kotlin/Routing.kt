package com.discovery

import com.discovery.service.ProductService
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.serialization.Serializable

@Serializable
data class ErrorResponse(val error: String, val message: String)

@Serializable
data class ProductsResponse<T>(val products: List<T>, val count: Int)

fun Application.configureRouting() {
    val productService = ProductService()
    
    routing {
        get("/") {
            call.respondText("Waterlily Product Service")
        }
        
        // Health check endpoint
        get("/health") {
            call.respondText("OK")
        }
        
        route("/v1/products") {
            // GET /v1/products?ids=id1,id2,id3 - Get multiple products
            get {
                val idsParam = call.request.queryParameters["ids"]
                
                if (idsParam.isNullOrBlank()) {
                    call.respond(
                        HttpStatusCode.BadRequest,
                        ErrorResponse("bad_request", "Query parameter 'ids' is required")
                    )
                    return@get
                }
                
                val ids = idsParam.split(",").map { it.trim() }.filter { it.isNotBlank() }
                
                if (ids.isEmpty()) {
                    call.respond(
                        HttpStatusCode.BadRequest,
                        ErrorResponse("bad_request", "At least one valid ID is required")
                    )
                    return@get
                }
                
                if (ids.size > ProductService.MAX_BATCH_SIZE) {
                    call.respond(
                        HttpStatusCode.BadRequest,
                        ErrorResponse("bad_request", "Maximum ${ProductService.MAX_BATCH_SIZE} IDs allowed per request")
                    )
                    return@get
                }
                
                val products = productService.getProductsByIds(ids)
                call.respond(ProductsResponse(products, products.size))
            }
            
            // GET /v1/products/{id} - Get single product
            get("/{id}") {
                val id = call.parameters["id"]
                
                if (id.isNullOrBlank()) {
                    call.respond(
                        HttpStatusCode.BadRequest,
                        ErrorResponse("bad_request", "Product ID is required")
                    )
                    return@get
                }
                
                val product = productService.getProductById(id)
                
                if (product == null) {
                    call.respond(
                        HttpStatusCode.NotFound,
                        ErrorResponse("not_found", "Product with ID '$id' not found")
                    )
                    return@get
                }
                
                call.respond(product)
            }
        }
    }
}
