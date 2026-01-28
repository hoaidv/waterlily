plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.ktor)
}

group = "com.discovery"
version = "0.0.1"

application {
    mainClass = "io.ktor.server.netty.EngineMain"
}

dependencies {
    // Ktor
    implementation(libs.ktor.server.core)
    implementation(libs.ktor.server.netty)
    implementation(libs.ktor.server.config.yaml)
    implementation(libs.ktor.server.content.negotiation)
    implementation(libs.ktor.serialization.kotlinx.json)
    
    // Database
    implementation(libs.hikaricp)
    implementation(libs.mysql.connector)
    
    // Serialization
    implementation(libs.kotlinx.serialization.json)
    
    // Logging
    implementation(libs.logback.classic)
    
    // Testing
    testImplementation(libs.ktor.server.test.host)
    testImplementation(libs.kotlin.test.junit)
}

// Task to extract product IDs for benchmarking
tasks.register<JavaExec>("extractProductIds") {
    group = "benchmark"
    description = "Extract product IDs from the database for benchmarking"
    mainClass.set("com.discovery.tools.ExtractProductIds")
    classpath = sourceSets["main"].runtimeClasspath
    
    val idCount = project.findProperty("idCount")?.toString() ?: "10000"
    val outputFile = project.findProperty("outputFile")?.toString() ?: "experiment/product_ids.txt"
    
    args = listOf(idCount, outputFile)
}
