package com.discovery.routes

import com.discovery.model.*
import com.discovery.service.ProductService
import io.ktor.http.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Route.productRoutes(productService: ProductService) {
    route("/api/v1/products") {
        
        // GET /api/v1/products/{id} - Get single product by ID
        get("/{id}") {
            val idParam = call.parameters["id"] 
                ?: throw InvalidRequestException("Product ID is required")
            
            val id = idParam.toLongOrNull() 
                ?: throw InvalidRequestException("Invalid product ID format")
            
            val product = productService.getProductById(id)
                ?: throw ProductNotFoundException(id)
            
            call.respond(HttpStatusCode.OK, product)
        }
        
        // POST /api/v1/products/batch - Get multiple products by IDs
        post("/batch") {
            val request = call.receive<BatchRequest>()
            
            // Validate request
            if (request.ids.isEmpty()) {
                throw InvalidRequestException("At least one product ID is required")
            }
            
            if (request.ids.size > BatchRequest.MAX_IDS) {
                throw BatchLimitExceededException(request.ids.size)
            }
            
            val products = productService.getProductsByIds(request.ids)
            
            call.respond(
                HttpStatusCode.OK,
                BatchProductResponse(
                    products = products,
                    count = products.size
                )
            )
        }
    }
}
