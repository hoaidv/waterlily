package com.discovery.plugins

import com.discovery.model.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.plugins.statuspages.*
import io.ktor.server.response.*

fun Application.configureStatusPages() {
    install(StatusPages) {
        exception<ProductNotFoundException> { call, cause ->
            call.respond(
                HttpStatusCode.NotFound,
                ProductNotFoundResponse(productId = cause.productId)
            )
        }
        
        exception<InvalidRequestException> { call, cause ->
            call.respond(
                HttpStatusCode.BadRequest,
                ErrorResponse(
                    error = "INVALID_REQUEST",
                    message = cause.message ?: "Invalid request"
                )
            )
        }
        
        exception<BatchLimitExceededException> { call, cause ->
            call.respond(
                HttpStatusCode.BadRequest,
                BatchLimitExceededResponse(requestedCount = cause.requestedCount)
            )
        }
        
        exception<NumberFormatException> { call, _ ->
            call.respond(
                HttpStatusCode.BadRequest,
                ErrorResponse(
                    error = "INVALID_REQUEST",
                    message = "Invalid product ID format"
                )
            )
        }
        
        exception<Throwable> { call, cause ->
            call.application.environment.log.error("Unhandled exception", cause)
            call.respond(
                HttpStatusCode.InternalServerError,
                ErrorResponse(
                    error = "INTERNAL_ERROR",
                    message = "An unexpected error occurred"
                )
            )
        }
    }
}
