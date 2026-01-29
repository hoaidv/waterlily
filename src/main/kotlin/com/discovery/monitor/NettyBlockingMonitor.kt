package com.discovery.monitor

import org.slf4j.LoggerFactory
import java.lang.management.ManagementFactory
import java.lang.management.ThreadInfo
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledExecutorService
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean
import java.util.concurrent.atomic.AtomicLong

/**
 * Monitors Netty event loop threads for blocking operations.
 * 
 * Netty's event loop threads should never block. When they do, it can cause:
 * - Degraded throughput
 * - Increased latency
 * - Connection timeouts
 * - Thread starvation
 * 
 * This monitor detects blocking by:
 * 1. Periodically sampling thread states
 * 2. Tracking how long threads remain in BLOCKED/WAITING states
 * 3. Capturing stack traces when thresholds are exceeded
 */
class NettyBlockingMonitor private constructor(
    private val config: Config
) {
    private val logger = LoggerFactory.getLogger(NettyBlockingMonitor::class.java)
    private val threadMXBean = ManagementFactory.getThreadMXBean()
    private val scheduler: ScheduledExecutorService = Executors.newSingleThreadScheduledExecutor { r ->
        Thread(r, "netty-blocking-monitor").apply { isDaemon = true }
    }
    
    private val running = AtomicBoolean(false)
    
    // Track blocking state per thread
    private val threadBlockingState = ConcurrentHashMap<Long, BlockingState>()
    
    // Statistics
    private val totalBlockingEvents = AtomicLong(0)
    private val totalBlockingTimeMs = AtomicLong(0)
    private val startTime = AtomicLong(0)
    
    data class Config(
        val checkIntervalMs: Long = 100,              // How often to check thread states
        val warningThresholdMs: Long = 50,            // Warn if blocked longer than this
        val criticalThresholdMs: Long = 200,          // Critical alert threshold
        val stackTraceOnWarning: Boolean = true,      // Capture stack trace on warning
        val nettyThreadPatterns: List<String> = listOf(
            "ktor-cio",
            "eventLoopGroup",
            "nioEventLoopGroup",
            "epollEventLoopGroup",
            "kqueueEventLoopGroup",
            "ktor-netty"
        )
    )
    
    private data class BlockingState(
        val threadId: Long,
        val threadName: String,
        var blockingStartTime: Long = 0,
        var lastState: Thread.State = Thread.State.RUNNABLE,
        var warningLogged: Boolean = false,
        var criticalLogged: Boolean = false,
        var lastStackTrace: Array<StackTraceElement>? = null
    )
    
    fun start() {
        if (running.compareAndSet(false, true)) {
            startTime.set(System.currentTimeMillis())
            logger.info("Starting Netty blocking monitor with check interval: {}ms, warning threshold: {}ms, critical threshold: {}ms",
                config.checkIntervalMs, config.warningThresholdMs, config.criticalThresholdMs)
            
            scheduler.scheduleAtFixedRate(
                { checkThreadStates() },
                config.checkIntervalMs,
                config.checkIntervalMs,
                TimeUnit.MILLISECONDS
            )
        }
    }
    
    fun stop() {
        if (running.compareAndSet(true, false)) {
            scheduler.shutdown()
            try {
                if (!scheduler.awaitTermination(5, TimeUnit.SECONDS)) {
                    scheduler.shutdownNow()
                }
            } catch (e: InterruptedException) {
                scheduler.shutdownNow()
                Thread.currentThread().interrupt()
            }
            logStatistics()
            logger.info("Netty blocking monitor stopped")
        }
    }
    
    private fun checkThreadStates() {
        try {
            val currentTime = System.currentTimeMillis()
            val threadInfos = threadMXBean.dumpAllThreads(config.stackTraceOnWarning, false)
            
            for (threadInfo in threadInfos) {
                if (!isNettyThread(threadInfo.threadName)) continue
                
                val state = threadBlockingState.computeIfAbsent(threadInfo.threadId) {
                    BlockingState(threadInfo.threadId, threadInfo.threadName)
                }
                
                processThreadState(threadInfo, state, currentTime)
            }
            
            // Clean up old entries for terminated threads
            val activeThreadIds = threadInfos.map { it.threadId }.toSet()
            threadBlockingState.keys.removeIf { it !in activeThreadIds }
            
        } catch (e: Exception) {
            logger.error("Error checking thread states", e)
        }
    }
    
    private fun processThreadState(threadInfo: ThreadInfo, state: BlockingState, currentTime: Long) {
        val isBlocking = isBlockingState(threadInfo.threadState)
        
        when {
            isBlocking && state.lastState == Thread.State.RUNNABLE -> {
                // Thread just started blocking
                state.blockingStartTime = currentTime
                state.warningLogged = false
                state.criticalLogged = false
                state.lastStackTrace = threadInfo.stackTrace
            }
            
            isBlocking && state.blockingStartTime > 0 -> {
                // Thread is still blocking
                val blockingDuration = currentTime - state.blockingStartTime
                state.lastStackTrace = threadInfo.stackTrace
                
                when {
                    blockingDuration >= config.criticalThresholdMs && !state.criticalLogged -> {
                        logCriticalBlocking(state, threadInfo, blockingDuration)
                        state.criticalLogged = true
                        totalBlockingEvents.incrementAndGet()
                    }
                    
                    blockingDuration >= config.warningThresholdMs && !state.warningLogged -> {
                        logWarningBlocking(state, threadInfo, blockingDuration)
                        state.warningLogged = true
                        totalBlockingEvents.incrementAndGet()
                    }
                }
            }
            
            !isBlocking && state.blockingStartTime > 0 -> {
                // Thread resumed from blocking
                val blockingDuration = currentTime - state.blockingStartTime
                totalBlockingTimeMs.addAndGet(blockingDuration)
                
                if (blockingDuration >= config.warningThresholdMs) {
                    logger.debug("Thread '{}' resumed after blocking for {}ms", 
                        state.threadName, blockingDuration)
                }
                
                state.blockingStartTime = 0
                state.warningLogged = false
                state.criticalLogged = false
            }
        }
        
        state.lastState = threadInfo.threadState
    }
    
    private fun isNettyThread(threadName: String): Boolean {
        return config.nettyThreadPatterns.any { pattern ->
            threadName.contains(pattern, ignoreCase = true)
        }
    }
    
    private fun isBlockingState(state: Thread.State): Boolean {
        return state == Thread.State.BLOCKED ||
               state == Thread.State.WAITING ||
               state == Thread.State.TIMED_WAITING
    }
    
    private fun logWarningBlocking(state: BlockingState, threadInfo: ThreadInfo, durationMs: Long) {
        val stackTrace = formatStackTrace(state.lastStackTrace)
        val lockInfo = formatLockInfo(threadInfo)
        
        logger.warn("""
            |
            |========== NETTY THREAD BLOCKING WARNING ==========
            |Thread: {} (id={})
            |State: {}
            |Blocked for: {}ms (threshold: {}ms)
            |{}
            |Stack trace:
            |{}
            |===================================================
        """.trimMargin(),
            state.threadName,
            state.threadId,
            threadInfo.threadState,
            durationMs,
            config.warningThresholdMs,
            lockInfo,
            stackTrace
        )
    }
    
    private fun logCriticalBlocking(state: BlockingState, threadInfo: ThreadInfo, durationMs: Long) {
        val stackTrace = formatStackTrace(state.lastStackTrace)
        val lockInfo = formatLockInfo(threadInfo)
        
        logger.error("""
            |
            |!!!!!!!!!! NETTY THREAD BLOCKING CRITICAL !!!!!!!!!!
            |Thread: {} (id={})
            |State: {}
            |Blocked for: {}ms (threshold: {}ms)
            |{}
            |
            |This is a CRITICAL performance issue!
            |Blocking Netty event loop threads causes:
            |- Request timeouts
            |- Degraded throughput
            |- Connection failures
            |
            |Consider using:
            |- Dispatchers.IO for blocking operations
            |- Async database drivers (R2DBC)
            |- Non-blocking HTTP clients
            |
            |Stack trace:
            |{}
            |!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """.trimMargin(),
            state.threadName,
            state.threadId,
            threadInfo.threadState,
            durationMs,
            config.criticalThresholdMs,
            lockInfo,
            stackTrace
        )
    }
    
    private fun formatStackTrace(stackTrace: Array<StackTraceElement>?): String {
        if (stackTrace.isNullOrEmpty()) return "  <no stack trace available>"
        
        return stackTrace.take(20).joinToString("\n") { "  at $it" } +
            if (stackTrace.size > 20) "\n  ... ${stackTrace.size - 20} more" else ""
    }
    
    private fun formatLockInfo(threadInfo: ThreadInfo): String {
        val sb = StringBuilder()
        
        threadInfo.lockInfo?.let { lock ->
            sb.append("Waiting for lock: ${lock.className}@${lock.identityHashCode}\n")
        }
        
        threadInfo.lockOwnerName?.let { owner ->
            sb.append("Lock owner: $owner (id=${threadInfo.lockOwnerId})")
        }
        
        return if (sb.isNotEmpty()) sb.toString() else "No lock information available"
    }
    
    fun getStatistics(): Statistics {
        val uptimeMs = System.currentTimeMillis() - startTime.get()
        return Statistics(
            uptimeMs = uptimeMs,
            totalBlockingEvents = totalBlockingEvents.get(),
            totalBlockingTimeMs = totalBlockingTimeMs.get(),
            monitoredThreads = threadBlockingState.size,
            currentlyBlockedThreads = threadBlockingState.values.count { it.blockingStartTime > 0 }
        )
    }
    
    private fun logStatistics() {
        val stats = getStatistics()
        logger.info("""
            |
            |Netty Blocking Monitor Statistics:
            |  Uptime: ${stats.uptimeMs}ms
            |  Total blocking events: ${stats.totalBlockingEvents}
            |  Total blocking time: ${stats.totalBlockingTimeMs}ms
            |  Monitored threads: ${stats.monitoredThreads}
        """.trimMargin())
    }
    
    data class Statistics(
        val uptimeMs: Long,
        val totalBlockingEvents: Long,
        val totalBlockingTimeMs: Long,
        val monitoredThreads: Int,
        val currentlyBlockedThreads: Int
    )
    
    companion object {
        @Volatile
        private var instance: NettyBlockingMonitor? = null
        
        fun getInstance(config: Config = Config()): NettyBlockingMonitor {
            return instance ?: synchronized(this) {
                instance ?: NettyBlockingMonitor(config).also { instance = it }
            }
        }
        
        fun configure(
            checkIntervalMs: Long = 100,
            warningThresholdMs: Long = 50,
            criticalThresholdMs: Long = 200,
            stackTraceOnWarning: Boolean = true
        ): NettyBlockingMonitor {
            return getInstance(Config(
                checkIntervalMs = checkIntervalMs,
                warningThresholdMs = warningThresholdMs,
                criticalThresholdMs = criticalThresholdMs,
                stackTraceOnWarning = stackTraceOnWarning
            ))
        }
    }
}
