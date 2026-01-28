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
    // Ktor server
    implementation(libs.ktor.server.core)
    implementation(libs.ktor.server.netty)
    implementation(libs.ktor.server.config.yaml)
    implementation(libs.ktor.server.content.negotiation)
    implementation(libs.ktor.server.status.pages)
    implementation(libs.ktor.serialization.kotlinx.json)

    // Database
    implementation(libs.hikaricp)
    implementation(libs.mysql.connector)

    // Logging
    implementation(libs.logback.classic)

    // Testing
    testImplementation(libs.ktor.server.test.host)
    testImplementation(libs.kotlin.test.junit)
}

// Task to extract product IDs for benchmarking
// Usage: ./gradlew extractProductIds -PproductCount=1000000 -PresultFile=experiment/product_ids.txt
tasks.register<JavaExec>("extractProductIds") {
    group = "benchmark"
    description = "Extract random product IDs from database for benchmark testing"
    mainClass.set("com.discovery.tools.ExtractProductIds")
    classpath = sourceSets["main"].runtimeClasspath
    
    // Pass Gradle properties as command-line arguments
    val productCount = project.findProperty("productCount")?.toString() ?: "1000000"
    val resultFile = project.findProperty("resultFile")?.toString() ?: "experiment/product_ids.txt"
    args = listOf(productCount, resultFile)
}
