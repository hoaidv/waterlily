-- Waterlily Benchmark Script for wrk
-- Usage: wrk -t12 -c1000 -d60s --timeout 30s -s benchmark.lua http://localhost:8080 -- <api_type> <batch_size> <ccu> <timeout>
--
-- Arguments (passed after --):
--   api_type   : "single" or "batch" (default: "single")
--   batch_size : Number of IDs per batch request, only for batch API (default: 10)
--   ccu        : Concurrent connections, passed explicitly for result tracking (default: 0)
--   timeout    : Request timeout in seconds (default: 30)

-- Configuration
local product_ids = {}
local api_type = "single"
local batch_size = 10
local ccu = 0
local timeout_sec = 30
local start_time = nil

-- Benchmark context
local benchmark_context = {
    platform = "localhost",
    database_type = "MySQL",
    database_instances = 1,
    access_pattern = {
        request_type = "READ",
        throughput = "HEAVY",
        complexity = "MEDIUM"
    }
}

-- Error tracking
local http_errors = {
    ["4xx"] = 0,
    ["5xx"] = 0
}

-- Thread-local request counter
local request_counter = 0

-- Load product IDs from file
function load_product_ids(filename)
    local file = io.open(filename, "r")
    if not file then
        io.stderr:write("ERROR: Could not open " .. filename .. "\n")
        io.stderr:write("Please run the product ID extractor first:\n")
        io.stderr:write("  ./gradlew extractProductIds --args=\"--count 1000000 --output experiment/product_ids.txt\"\n")
        os.exit(1)
    end

    for line in file:lines() do
        local id = line:match("^%s*(.-)%s*$")  -- Trim whitespace
        if id and id ~= "" then
            table.insert(product_ids, id)
        end
    end
    file:close()

    if #product_ids == 0 then
        io.stderr:write("ERROR: No product IDs found in " .. filename .. "\n")
        os.exit(1)
    end

    io.write(string.format("Loaded %d product IDs\n", #product_ids))
end

-- Parse command line arguments
function parse_args()
    if wrk.args then
        if wrk.args[1] then
            api_type = wrk.args[1]
        end
        if wrk.args[2] then
            batch_size = tonumber(wrk.args[2]) or 10
        end
        if wrk.args[3] then
            ccu = tonumber(wrk.args[3]) or 0
        end
        if wrk.args[4] then
            timeout_sec = tonumber(wrk.args[4]) or 30
        end
    end

    -- Validate api_type
    if api_type ~= "single" and api_type ~= "batch" then
        io.stderr:write("ERROR: Invalid api_type. Must be 'single' or 'batch'\n")
        os.exit(1)
    end

    io.write(string.format("Configuration:\n"))
    io.write(string.format("  API type: %s\n", api_type))
    if api_type == "batch" then
        io.write(string.format("  Batch size: %d\n", batch_size))
    end
    io.write(string.format("  CCU: %d\n", ccu))
    io.write(string.format("  Timeout: %ds\n", timeout_sec))
end

-- Init function called once per thread
function init(args)
    -- Determine script directory
    local script_path = debug.getinfo(1, "S").source:match("^@(.*/)")
    local ids_file

    if script_path then
        ids_file = script_path .. "product_ids.txt"
    else
        ids_file = "experiment/product_ids.txt"
    end

    load_product_ids(ids_file)
    parse_args()

    -- Record start time (only once)
    if not start_time then
        start_time = os.date("%Y-%m-%d-%H-%M-%S")
    end
end

-- Generate request based on API type
function request()
    request_counter = request_counter + 1

    if api_type == "batch" then
        return generate_batch_request()
    else
        return generate_single_request()
    end
end

-- Generate single product request: GET /api/v1/products/{id}
function generate_single_request()
    local idx = ((request_counter - 1) % #product_ids) + 1
    local path = "/api/v1/products/" .. product_ids[idx]

    return wrk.format("GET", path, {
        ["Accept"] = "application/json"
    })
end

-- Generate batch request: POST /api/v1/products/batch
function generate_batch_request()
    local ids = {}
    for i = 1, batch_size do
        local idx = ((request_counter + i - 2) % #product_ids) + 1
        table.insert(ids, product_ids[idx])
    end

    -- Build JSON body
    local json_ids = {}
    for _, id in ipairs(ids) do
        table.insert(json_ids, id)
    end
    local body = '{"ids":[' .. table.concat(json_ids, ',') .. ']}'

    return wrk.format("POST", "/api/v1/products/batch", {
        ["Content-Type"] = "application/json",
        ["Accept"] = "application/json"
    }, body)
end

-- Handle response and track errors
function response(status, headers, body)
    if status >= 400 and status < 500 then
        http_errors["4xx"] = http_errors["4xx"] + 1
    elseif status >= 500 then
        http_errors["5xx"] = http_errors["5xx"] + 1
    end
end

-- Generate timestamp for filename
function get_timestamp()
    return start_time or os.date("%Y-%m-%d-%H-%M-%S")
end

-- Summary function called when benchmark completes
function done(summary, latency, requests)
    local duration_sec = summary.duration / 1000000
    local rps = summary.requests / duration_sec
    local transfer_mb = summary.bytes / 1024 / 1024
    local transfer_rate_mbps = transfer_mb / duration_sec

    -- Print results to console
    io.write("\n")
    io.write("================================================================================\n")
    io.write("                           BENCHMARK RESULTS\n")
    io.write("================================================================================\n")
    io.write(string.format("API Type:        %s\n", api_type))
    if api_type == "batch" then
        io.write(string.format("Batch Size:      %d\n", batch_size))
    end
    io.write(string.format("CCU:             %d\n", ccu))
    io.write(string.format("Duration:        %.2f seconds\n", duration_sec))
    io.write("--------------------------------------------------------------------------------\n")
    io.write("THROUGHPUT\n")
    io.write(string.format("  Total Requests: %d\n", summary.requests))
    io.write(string.format("  Requests/sec:   %.2f\n", rps))
    io.write("--------------------------------------------------------------------------------\n")
    io.write("LATENCY (ms)\n")
    io.write(string.format("  Min:    %.4f\n", latency.min / 1000))
    io.write(string.format("  Avg:    %.4f\n", latency.mean / 1000))
    io.write(string.format("  Max:    %.4f\n", latency.max / 1000))
    io.write(string.format("  Stdev:  %.4f\n", latency.stdev / 1000))
    io.write("--------------------------------------------------------------------------------\n")
    io.write("PERCENTILES (ms)\n")
    io.write(string.format("  p50:    %.4f\n", latency:percentile(50) / 1000))
    io.write(string.format("  p75:    %.4f\n", latency:percentile(75) / 1000))
    io.write(string.format("  p90:    %.4f\n", latency:percentile(90) / 1000))
    io.write(string.format("  p95:    %.4f\n", latency:percentile(95) / 1000))
    io.write(string.format("  p99:    %.4f\n", latency:percentile(99) / 1000))
    io.write("--------------------------------------------------------------------------------\n")
    io.write("TRANSFER\n")
    io.write(string.format("  Total:  %.2f MB\n", transfer_mb))
    io.write(string.format("  Rate:   %.2f MB/s\n", transfer_rate_mbps))
    io.write("--------------------------------------------------------------------------------\n")
    io.write("ERRORS\n")
    io.write(string.format("  Socket Connect: %d\n", summary.errors.connect))
    io.write(string.format("  Socket Read:    %d\n", summary.errors.read))
    io.write(string.format("  Socket Write:   %d\n", summary.errors.write))
    io.write(string.format("  Socket Timeout: %d\n", summary.errors.timeout))
    io.write(string.format("  HTTP 4xx:       %d\n", http_errors["4xx"]))
    io.write(string.format("  HTTP 5xx:       %d\n", http_errors["5xx"]))
    io.write("================================================================================\n")

    -- Export to JSON
    export_json_results(summary, latency, duration_sec, rps, transfer_mb, transfer_rate_mbps)
end

-- Export results to JSON file
function export_json_results(summary, latency, duration_sec, rps, transfer_mb, transfer_rate_mbps)
    local timestamp = get_timestamp()

    -- Determine output directory
    local script_path = debug.getinfo(1, "S").source:match("^@(.*/)")
    local benchmarks_dir
    if script_path then
        benchmarks_dir = script_path .. "benchmarks/"
    else
        benchmarks_dir = "experiment/benchmarks/"
    end

    -- Create benchmarks directory
    os.execute("mkdir -p " .. benchmarks_dir)

    local filename = benchmarks_dir .. timestamp .. "_" .. api_type .. "_ccu" .. ccu .. ".json"
    local file = io.open(filename, "w")

    if not file then
        io.stderr:write("WARNING: Could not write JSON results to " .. filename .. "\n")
        return
    end

    -- Determine endpoint based on API type
    local endpoint
    if api_type == "single" then
        endpoint = "GET /api/v1/products/{id}"
    else
        endpoint = "POST /api/v1/products/batch"
    end

    local json_output = string.format([[{
  "benchmark_context": {
    "platform": "%s",
    "database_type": "%s",
    "database_instances": %d,
    "access_pattern": {
      "request_type": "%s",
      "throughput": "%s",
      "complexity": "%s"
    }
  },
  "timestamp": "%s",
  "duration_seconds": %.2f,
  "results": [
    {
      "api": "%s",
      "endpoint": "%s",
      "ccu": %d,
      "batch_size": %s,
      "metrics": {
        "requests_total": %d,
        "rps": %.2f,
        "latency": {
          "min_ms": %.4f,
          "avg_ms": %.4f,
          "max_ms": %.4f,
          "stdev_ms": %.4f,
          "p50_ms": %.4f,
          "p95_ms": %.4f,
          "p99_ms": %.4f
        },
        "transfer": {
          "total_mb": %.2f,
          "rate_mbps": %.2f
        },
        "errors": {
          "socket_connect": %d,
          "socket_read": %d,
          "socket_write": %d,
          "socket_timeout": %d,
          "http_4xx": %d,
          "http_5xx": %d
        }
      }
    }
  ]
}
]],
        benchmark_context.platform,
        benchmark_context.database_type,
        benchmark_context.database_instances,
        benchmark_context.access_pattern.request_type,
        benchmark_context.access_pattern.throughput,
        benchmark_context.access_pattern.complexity,
        timestamp,
        duration_sec,
        api_type == "single" and "single_product" or "batch_products",
        endpoint,
        ccu,
        api_type == "batch" and tostring(batch_size) or "null",
        summary.requests,
        rps,
        latency.min / 1000,
        latency.mean / 1000,
        latency.max / 1000,
        latency.stdev / 1000,
        latency:percentile(50) / 1000,
        latency:percentile(95) / 1000,
        latency:percentile(99) / 1000,
        transfer_mb,
        transfer_rate_mbps,
        summary.errors.connect,
        summary.errors.read,
        summary.errors.write,
        summary.errors.timeout,
        http_errors["4xx"],
        http_errors["5xx"]
    )

    file:write(json_output)
    file:close()

    io.write(string.format("\nResults exported to: %s\n", filename))
end
