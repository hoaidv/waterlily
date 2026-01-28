-- Benchmark script for batch product API
-- Usage: WRK_CCU=1000 WRK_OUTPUT_FILE=result.json wrk -t12 -c1000 -d60s -s benchmark_batch.lua http://localhost:8080

local product_ids = {}
local counter = 0
local errors_4xx = 0
local errors_5xx = 0

-- Batch size range
local MIN_BATCH_SIZE = 10
local MAX_BATCH_SIZE = 50

-- Initialize: load product IDs from file
function init(args)
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
    
    -- Seed random number generator
    math.randomseed(os.time())
end

-- Generate a random batch of product IDs
function generate_batch()
    local batch_size = math.random(MIN_BATCH_SIZE, MAX_BATCH_SIZE)
    local ids = {}
    
    for i = 1, batch_size do
        local idx = math.random(1, #product_ids)
        table.insert(ids, product_ids[idx])
    end
    
    return ids
end

-- Generate request for each iteration
function request()
    counter = counter + 1
    local ids = generate_batch()
    
    -- Build JSON body
    local ids_json = table.concat(ids, ",")
    local body = '{"ids":[' .. ids_json .. ']}'
    
    local headers = {
        ["Content-Type"] = "application/json"
    }
    
    return wrk.format("POST", "/api/v1/products/batch", headers, body)
end

-- Track response status codes
function response(status, headers, body)
    if status >= 400 and status < 500 then
        errors_4xx = errors_4xx + 1
    elseif status >= 500 then
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
      "complexity": "HIGH"
    }
  },
  "benchmark_target": {
    "api": "batch_products",
    "endpoint": "POST /api/v1/products/batch",
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
  }
}]],
        ccu,
        timestamp,
        duration_seconds,
        requests_total,
        rps,
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
    io.stderr:write(string.format("Requests: %d (%.2f RPS)\n", requests_total, rps))
    io.stderr:write(string.format("Latency: avg=%.2fms, p50=%.2fms, p95=%.2fms, p99=%.2fms\n", avg_ms, p50_ms, p95_ms, p99_ms))
    io.stderr:write(string.format("Errors: 4xx=%d, 5xx=%d, socket=%d\n", errors_4xx, errors_5xx, socket_connect + socket_read + socket_write + socket_timeout))
end
