package com.discovery.plugins

import com.discovery.monitor.NettyBlockingMonitor
import io.ktor.events.*
import io.ktor.server.application.*
import org.slf4j.LoggerFactory

/**
 * Ktor plugin configuration for Netty blocking monitor.
 */
class BlockingMonitorConfig {
    /** How often to check thread states (in milliseconds) */
    var checkIntervalMs: Long = 100
    
    /** Warn if a thread is blocked longer than this (in milliseconds) */
    var warningThresholdMs: Long = 50
    
    /** Critical alert if a thread is blocked longer than this (in milliseconds) */
    var criticalThresholdMs: Long = 200
    
    /** Whether to capture stack traces when warnings occur */
    var stackTraceOnWarning: Boolean = true
    
    /** Whether monitoring is enabled */
    var enabled: Boolean = true
}

/**
 * Ktor plugin for monitoring Netty thread blocking.
 * 
 * Usage:
 * ```kotlin
 * install(BlockingMonitorPlugin) {
 *     checkIntervalMs = 100
 *     warningThresholdMs = 50
 *     criticalThresholdMs = 200
 *     enabled = true
 * }
 * ```
 */
val BlockingMonitorPlugin = createApplicationPlugin(
    name = "BlockingMonitorPlugin",
    createConfiguration = ::BlockingMonitorConfig
) {
    val logger = LoggerFactory.getLogger("BlockingMonitorPlugin")
    val config = pluginConfig
    
    if (!config.enabled) {
        logger.info("Netty blocking monitor is disabled")
        return@createApplicationPlugin
    }
    
    val monitor = NettyBlockingMonitor.configure(
        checkIntervalMs = config.checkIntervalMs,
        warningThresholdMs = config.warningThresholdMs,
        criticalThresholdMs = config.criticalThresholdMs,
        stackTraceOnWarning = config.stackTraceOnWarning
    )
    
    // Start monitoring immediately when plugin is installed
    logger.info("Starting Netty blocking monitor")
    monitor.start()
    
    // Register shutdown hook via application environment
    application.monitor.subscribe(ApplicationStopped) {
        logger.info("Stopping Netty blocking monitor")
        monitor.stop()
    }
}

/**
 * Extension function to easily install the blocking monitor with default settings.
 */
fun Application.configureBlockingMonitor(
    enabled: Boolean = true,
    warningThresholdMs: Long = 50,
    criticalThresholdMs: Long = 200
) {
    install(BlockingMonitorPlugin) {
        this.enabled = enabled
        this.warningThresholdMs = warningThresholdMs
        this.criticalThresholdMs = criticalThresholdMs
    }
}
