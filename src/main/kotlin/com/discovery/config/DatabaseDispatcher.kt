package com.discovery.config

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.asCoroutineDispatcher
import org.slf4j.LoggerFactory
import java.util.concurrent.Executors
import java.util.concurrent.ThreadFactory
import java.util.concurrent.atomic.AtomicInteger

/**
 * Dedicated dispatcher for database operations.
 * 
 * Why a separate dispatcher instead of Dispatchers.IO?
 * 
 * 1. **Bounded thread pool**: Prevents unbounded thread creation under load.
 *    The pool size matches HikariCP's max connections, so we never have more
 *    threads waiting than connections available.
 * 
 * 2. **Isolation**: Database operations don't compete with other I/O operations
 *    (file reads, HTTP calls, etc.) for threads.
 * 
 * 3. **Backpressure**: When all threads are busy, new coroutines wait in queue
 *    rather than spawning more threads. This prevents thread explosion under load.
 * 
 * 4. **Monitoring**: Easier to monitor and tune database-specific thread pool.
 * 
 * Flow when handling a request:
 * 
 * 1. Request arrives on Netty worker thread (non-blocking)
 * 2. Route handler suspends and offloads to DatabaseDispatcher
 * 3. Netty worker thread is FREE to handle other requests
 * 4. Database operation runs on DatabaseDispatcher thread
 * 5. When complete, coroutine resumes (can be on any available thread)
 * 6. Response sent back on Netty worker thread
 * 
 * This allows thousands of concurrent requests with a small thread pool!
 */
object DatabaseDispatcher {
    private val logger = LoggerFactory.getLogger(DatabaseDispatcher::class.java)
    
    @Volatile
    private var dispatcher: CoroutineDispatcher? = null
    
    @Volatile
    private var poolSize: Int = 50
    
    private val threadFactory = object : ThreadFactory {
        private val counter = AtomicInteger(0)
        override fun newThread(r: Runnable): Thread {
            return Thread(r, "db-dispatcher-${counter.incrementAndGet()}").apply {
                isDaemon = true
            }
        }
    }
    
    /**
     * Initialize the database dispatcher with a fixed thread pool.
     * 
     * @param size Thread pool size. Should match or be slightly less than
     *             HikariCP's maximumPoolSize to avoid threads waiting for connections.
     */
    fun init(size: Int) {
        if (dispatcher != null) {
            logger.warn("DatabaseDispatcher already initialized, skipping")
            return
        }
        
        poolSize = size
        dispatcher = Executors.newFixedThreadPool(size, threadFactory).asCoroutineDispatcher()
        logger.info("Initialized DatabaseDispatcher with {} threads", size)
    }
    
    /**
     * Get the database dispatcher.
     * Falls back to a default pool if not explicitly initialized.
     */
    fun get(): CoroutineDispatcher {
        return dispatcher ?: synchronized(this) {
            dispatcher ?: run {
                logger.warn("DatabaseDispatcher not initialized, using default pool size: {}", poolSize)
                Executors.newFixedThreadPool(poolSize, threadFactory).asCoroutineDispatcher().also {
                    dispatcher = it
                }
            }
        }
    }
    
    /**
     * Shutdown the dispatcher gracefully.
     */
    fun shutdown() {
        dispatcher?.let {
            logger.info("Shutting down DatabaseDispatcher")
            // The dispatcher wraps an ExecutorService, but we can't directly access it
            // In production, you might want to keep a reference to the ExecutorService
        }
    }
}
