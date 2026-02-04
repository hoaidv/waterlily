-- Benchmark script for single product API with Zipfian access pattern
-- Usage: WRK_CCU=1000 WRK_OUTPUT_FILE=result.json wrk -t12 -c1000 -d60s -s benchmark_single.lua http://localhost:8080
--
-- Access pattern: Zipfian distribution with exponent s=4
-- Some products are accessed much more frequently than others (realistic e-commerce pattern)

local product_ids = {}
local zipf_cdf = {}  -- Cumulative distribution function for Zipfian sampling
local zipf_s = 1.1     -- Zipfian exponent (higher = more skewed toward popular items)
local errors_3xx = 0
local errors_4xx = 0
local errors_5xx = 0

local counter = 1
local threads = {}

-- Precompute Zipfian CDF for efficient sampling
-- For Zipfian distribution: P(rank=i) ∝ 1/i^s
local function build_zipf_cdf(n, s)
    local cdf = {}
    local sum = 0
    
    -- Calculate normalization constant (harmonic number)
    for i = 1, n do
        sum = sum + (1.0 / math.pow(i, s))
    end
    
    -- Build CDF
    local cumulative = 0
    for i = 1, n do
        cumulative = cumulative + (1.0 / math.pow(i, s)) / sum
        cdf[i] = cumulative
    end
    
    return cdf
end

-- Sample from Zipfian distribution using binary search on CDF
local function zipf_sample(cdf, n)
    local u = math.random()
    
    -- Binary search for the rank
    local lo, hi = 1, n
    while lo < hi do
        local mid = math.floor((lo + hi) / 2)
        if cdf[mid] < u then
            lo = mid + 1
        else
            hi = mid
        end
    end
    
    return lo
end

-- use of setup() to pass
-- data to and from the threads
function setup(thread)
    thread:set("id", counter)
    table.insert(threads, thread)
    counter = counter + 1
end

-- Initialize: load product IDs from file and build Zipfian CDF
function init(args)
    requests  = 0
    responses = 0
    local file = io.open("experiment/product_ids.txt", "r")
    if not file then
        io.stderr:write("Error: Could not open experiment/product_ids.txt\n")
        os.exit(1)
    end
    
    for line in file:lines() do
        local id = line:match("^%s*(.-)%s*$")  -- trim whitespace
        if id and id ~= "" then
            table.insert(product_ids, id)
        end
    end
    file:close()
    
    if #product_ids == 0 then
        io.stderr:write("Error: No product IDs loaded from file\n")
        os.exit(1)
    end
    
    io.stderr:write("Loaded " .. #product_ids .. " product IDs\n")
    
    -- Build Zipfian CDF for access pattern simulation
    io.stderr:write("Building Zipfian CDF (s=" .. zipf_s .. ", N=" .. #product_ids .. ")...\n")
    zipf_cdf = build_zipf_cdf(#product_ids, zipf_s)
    io.stderr:write("Zipfian CDF ready. Top product expected ~" .. string.format("%.1f%%", 100 / math.pow(1, zipf_s) / (function()
        local sum = 0
        for i = 1, math.min(1000, #product_ids) do sum = sum + 1/math.pow(i, zipf_s) end
        return sum * (#product_ids / math.min(1000, #product_ids))
    end)()) .. " of requests\n")
    
    -- Seed random number generator
    math.randomseed(os.time())
end

-- Generate request for each iteration using Zipfian distribution
function request()
    requests = requests + 1

    -- Build headers
    local headers = {}
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"

    -- Sample product ID using Zipfian distribution
    local rank = zipf_sample(zipf_cdf, #product_ids)
    local id = product_ids[rank]
    
    local path = "/api/v1/products/" .. id
    return wrk.format("GET", path, headers)
end

-- Track response status codes
function response(status, headers, body)
    if 200 <= status and status < 300 then
        responses = responses + 1
    elseif 300 <= status and status < 400 then
        errors_3xx = errors_3xx + 1
    elseif 400 <= status and status < 500 then
        errors_4xx = errors_4xx + 1
    elseif 500 <= status then
        errors_5xx = errors_5xx + 1
    end
end

-- Output results as JSON when benchmark completes
function done(summary, latency, requests)
    -- Get config from environment variables
    local ccu = tonumber(os.getenv("WRK_CCU")) or 0
    local output_file = os.getenv("WRK_OUTPUT_FILE") or ""
    
    local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    local duration_seconds = summary.duration / 1000000  -- microseconds to seconds
    local requests_total = summary.requests
    local rps = requests_total / duration_seconds

    -- Count responses
    -- We can access each thread initialized in `init` function via `thread` var
    local total_responses = 0

    for index, thread in ipairs(threads) do
        local responses = thread:get("responses")
        total_responses = total_responses + responses
    end

    local response_per_second = total_responses / duration_seconds
    
    -- Calculate transfer in MB
    local total_bytes = summary.bytes
    local total_mb = total_bytes / (1024 * 1024)
    local rate_mbps = total_mb / duration_seconds
    
    -- Latency values (wrk provides in microseconds)
    local min_ms = latency.min / 1000
    local avg_ms = latency.mean / 1000
    local max_ms = latency.max / 1000
    local stdev_ms = latency.stdev / 1000
    
    -- Percentiles
    local p50_ms = latency:percentile(50) / 1000
    local p95_ms = latency:percentile(95) / 1000
    local p99_ms = latency:percentile(99) / 1000
    
    -- Socket errors
    local socket_connect = summary.errors.connect or 0
    local socket_read = summary.errors.read or 0
    local socket_write = summary.errors.write or 0
    local socket_timeout = summary.errors.timeout or 0
    
    local json_result = string.format([[{
  "benchmark_context": {
    "platform": "localhost",
    "database_type": "MySQL",
    "database_instances": 1,
    "access_pattern": {
      "request_type": "READ",
      "throughput": "HEAVY",
      "complexity": "MEDIUM",
      "distribution": "zipfian",
      "zipfian_exponent": %d,
      "product_count": %d
    }
  },
  "benchmark_target": {
    "api": "single_product",
    "endpoint": "GET /api/v1/products/{id}",
    "ccu": %d
  },
  "timestamp": "%s",
  "duration_seconds": %.2f,
  "metrics": {
    "requests_total": %d,
    "rps": %.2f,
    "latency": {
      "min_ms": %.3f,
      "avg_ms": %.3f,
      "max_ms": %.3f,
      "stdev_ms": %.3f,
      "p50_ms": %.3f,
      "p95_ms": %.3f,
      "p99_ms": %.3f
    },
    "transfer": {
      "total_mb": %.2f,
      "rate_mbps": %.2f
    },
    "errors": {
      "socket.connect": %d,
      "socket.read": %d,
      "socket.write": %d,
      "socket.timeout": %d,
      "4xx": %d,
      "5xx": %d
    }
  },
  "cache_metrics_note": "Query GET /monitor/cache before and after benchmark to calculate cache hit rates"
}]],
        zipf_s,
        #product_ids,
        ccu,
        timestamp,
        duration_seconds,
        total_responses,
        response_per_second,
        min_ms, avg_ms, max_ms, stdev_ms,
        p50_ms, p95_ms, p99_ms,
        total_mb, rate_mbps,
        socket_connect, socket_read, socket_write, socket_timeout,
        errors_4xx, errors_5xx
    )
    
    -- Write to output file if specified via environment variable
    if output_file ~= "" then
        local file = io.open(output_file, "w")
        if file then
            file:write(json_result)
            file:write("\n")
            file:close()
            io.stderr:write("Results written to: " .. output_file .. "\n")
        else
            io.stderr:write("Error: Could not write to " .. output_file .. "\n")
        end
    end
    
    -- Print summary to stderr
    io.stderr:write("\n--- Benchmark Results ---\n")
    io.stderr:write(string.format("Duration: %.2f seconds\n", duration_seconds))
    io.stderr:write(string.format("Successes: %d (%.2f RPS)\n", total_responses, response_per_second))
    io.stderr:write(string.format("Latency: avg=%.2fms, p50=%.2fms, p95=%.2fms, p99=%.2fms\n", avg_ms, p50_ms, p95_ms, p99_ms))
    io.stderr:write(string.format("Errors: 3xx=%d, 4xx=%d, 5xx=%d, socket=%d\n", errors_3xx, errors_4xx, errors_5xx, socket_connect + socket_read + socket_write + socket_timeout))
    io.stderr:write(string.format("Access pattern: Zipfian (s=%f, N=%d)\n", zipf_s, #product_ids))
    io.stderr:write("\nTo get cache metrics, query: curl http://localhost:8080/monitor/cache\n")
end
