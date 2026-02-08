package com.discovery.plugins

import com.discovery.model.ErrorResponse
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.request.*
import io.micrometer.core.instrument.Counter
import io.micrometer.core.instrument.Gauge
import io.micrometer.core.instrument.MeterRegistry
import kotlinx.coroutines.*
import org.slf4j.LoggerFactory
import java.util.concurrent.atomic.AtomicBoolean
import java.util.concurrent.atomic.AtomicInteger

/**
 * Data for one second bucket in the sliding window.
 * Thread-safe: use synchronized on the bucket when resetting and incrementing.
 */
private class Bucket {
    @Volatile
    var lastWrittenSecond: Long = -1L

    @Volatile
    var totalCount: Long = 0L

    @Volatile
    var overThresholdCount: Long = 0L

    @Synchronized
    fun ensureAndAdd(second: Long, overThreshold: Boolean) {
        if (lastWrittenSecond != second) {
            lastWrittenSecond = second
            totalCount = 0L
            overThresholdCount = 0L
        }
        totalCount++
        if (overThreshold) overThresholdCount++
    }

    @Synchronized
    fun readIfMatch(second: Long): Pair<Long, Long>? {
        return if (lastWrittenSecond == second) totalCount to overThresholdCount else null
    }
}

/**
 * Sliding window of RTW seconds: one bucket per second (ring).
 * On completion: add to bucket for current second.
 * On check: sum buckets for seconds in [now - RTW, now).
 */
private class SlidingWindow(
    private val rtwSeconds: Int,
    private val responseTimeThresholdMs: Long
) {
    private val buckets = Array(rtwSeconds) { Bucket() }

    fun recordCompletion(durationMs: Long) {
        val nowMs = System.currentTimeMillis()
        val second = nowMs / 1000
        val index = (second % rtwSeconds).toInt()
        val overThreshold = durationMs >= responseTimeThresholdMs
        buckets[index].ensureAndAdd(second, overThreshold)
    }

    /**
     * Returns (totalRequests, overThresholdRequests) for the last RTW seconds.
     * Only includes buckets whose lastWrittenSecond matches the second we're summing.
     */
    fun sumLastRtwSeconds(): Pair<Long, Long> {
        val nowSecond = System.currentTimeMillis() / 1000
        var total = 0L
        var overThreshold = 0L
        for (i in 0 until rtwSeconds) {
            val second = nowSecond - 1 - i
            if (second < 0) break
            val index = (second % rtwSeconds).toInt()
            buckets[index].readIfMatch(second)?.let { (t, o) ->
                total += t
                overThreshold += o
            }
        }
        return total to overThreshold
    }
}

/**
 * Check result: (rps, timeoutPercent). Check is satisfied when rps >= HTT and timeoutPercent >= TOR.
 */
private data class CheckResult(val rps: Double, val timeoutPercent: Double)

/**
 * Configuration for the High Load Shedder plugin.
 * RTW = Recent Time Window, HTT = High Traffic Threshold, TOR = Timeout Rate, CI = Check Interval,
 * TC = Trigger Condition (consecutive checks), CC = Cooldown Condition (consecutive checks).
 */
class HighLoadShedderConfig {
    var enabled: Boolean = false
    var recentTimeWindowSeconds: Int = 12
    var highTrafficThresholdRps: Int = 500
    var timeoutRatePercent: Double = 1.0
    var responseTimeThresholdMs: Long = 3000L
    var checkIntervalSeconds: Long = 1L
    var triggerConsecutiveChecks: Int = 3
    var cooldownConsecutiveChecks: Int = 3
    var excludedPaths: Set<String> = setOf("/health", "/ready", "/metrics")
    var meterRegistry: MeterRegistry? = null
}

/**
 * High Load Shedder plugin: latency-based load shedding.
 * Check = Traffic reaches HTT RPS and Timeout reaches TOR % in last RTW seconds.
 * Warning on first satisfied check; trigger 503 after TC consecutive satisfied checks;
 * cooldown (exit shedding) after CC consecutive unsatisfied checks.
 */
val HighLoadShedderPlugin = createApplicationPlugin(
    name = "HighLoadShedderPlugin",
    createConfiguration = ::HighLoadShedderConfig
) {
    val logger = LoggerFactory.getLogger("HighLoadShedderPlugin")
    logger.info("High load shedder: Installing...")
    val config = pluginConfig

    if (!config.enabled) {
        logger.info("High load shedder is disabled")
        return@createApplicationPlugin
    }

    val slidingWindow = SlidingWindow(config.recentTimeWindowSeconds, config.responseTimeThresholdMs)
    val shedding = AtomicBoolean(false)
    val consecutiveSatisfied = AtomicInteger(0)
    val consecutiveUnsatisfied = AtomicInteger(0)

    /** Check: satisfied iff RPS >= HTT and timeout % >= TOR (in last RTW seconds). */
    fun check(): CheckResult {
        val (total, overThreshold) = slidingWindow.sumLastRtwSeconds()
        val rtw = config.recentTimeWindowSeconds.toDouble()
        val rps = if (rtw > 0) total / rtw else 0.0
        val timeoutPercent = if (total > 0) 100.0 * overThreshold / total else 0.0
        return CheckResult(rps, timeoutPercent)
    }

    fun isCheckSatisfied(result: CheckResult): Boolean =
        result.rps >= config.highTrafficThresholdRps &&
            result.timeoutPercent >= config.timeoutRatePercent

    val rejectionCounter: Counter? = config.meterRegistry?.let { registry ->
        Counter.builder("high_load_shedder_rejections_total")
            .description("Total requests rejected with 503 due to high load shedding")
            .register(registry)
    }

    config.meterRegistry?.let { registry ->
        Gauge.builder("high_load_shedder_shedding") { if (shedding.get()) 1.0 else 0.0 }
            .description("1 when shedding (returning 503), 0 otherwise")
            .register(registry)
        Gauge.builder("high_load_shedder_consecutive_satisfied") { consecutiveSatisfied.get().toDouble() }
            .description("Consecutive checks that satisfied the condition")
            .register(registry)
        Gauge.builder("high_load_shedder_consecutive_unsatisfied") { consecutiveUnsatisfied.get().toDouble() }
            .description("Consecutive unsatisfied checks while shedding (for cooldown)")
            .register(registry)
    }

    logger.info(
        "High load shedder enabled: RTW=${config.recentTimeWindowSeconds}, HTT=${config.highTrafficThresholdRps}, " +
            "TOR=${config.timeoutRatePercent}%, responseTimeThresholdMs=${config.responseTimeThresholdMs}, " +
            "CI=${config.checkIntervalSeconds}s, TC=${config.triggerConsecutiveChecks}, CC=${config.cooldownConsecutiveChecks}, " +
            "excludedPaths=${config.excludedPaths}"
    )

    val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    val checkJob = scope.launch {
        while (isActive) {
            delay(config.checkIntervalSeconds * 1000L)
            val result = check()
            if (isCheckSatisfied(result)) {
                val prev = consecutiveSatisfied.getAndIncrement()
                consecutiveUnsatisfied.set(0)
                if (prev == 0) {
                    logger.warn(
                        "High load check satisfied: rps=${result.rps}, timeoutPercent=${result.timeoutPercent}% " +
                            "(HTT=${config.highTrafficThresholdRps}, TOR=${config.timeoutRatePercent}%)"
                    )
                }
                if (consecutiveSatisfied.get() >= config.triggerConsecutiveChecks) {
                    shedding.set(true)
                    logger.warn("High load shedder: entering shedding (503)")
                }
            } else {
                consecutiveSatisfied.set(0)
                if (shedding.get()) {
                    val unsat = consecutiveUnsatisfied.incrementAndGet()
                    if (unsat >= config.cooldownConsecutiveChecks) {
                        shedding.set(false)
                        consecutiveUnsatisfied.set(0)
                        logger.info("High load shedder: exiting shedding (cooldown)")
                    }
                }
            }
        }
    }

    application.monitor.subscribe(ApplicationStopped) {
        checkJob.cancel()
        scope.cancel()
    }


    application.intercept(ApplicationCallPipeline.Call) {
        val path = call.request.path().substringBefore('?')
        if (path in config.excludedPaths) {
            proceed()
            return@intercept
        }

        if (shedding.get()) {
            rejectionCounter?.increment()
            call.respond(
                HttpStatusCode.ServiceUnavailable,
                ErrorResponse(
                    error = "SERVICE_OVERLOADED",
                    message = "Server is at capacity; try again later"
                )
            )
            return@intercept
        }

        val startTime = System.currentTimeMillis()
        val recordCompletion = true

        try {
            proceed()
        } finally {
            if (recordCompletion) {
                val durationMs = System.currentTimeMillis() - startTime
                slidingWindow.recordCompletion(durationMs)
            }
        }
    }
}
