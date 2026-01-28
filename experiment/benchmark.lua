-- Wrk Lua script for benchmarking the Waterlily product service
-- Usage: wrk -t12 -c400 -d30s -s benchmark.lua http://localhost:8080 -- <api_type> <batch_size>
-- api_type: "single" or "batch"
-- batch_size: number of IDs per batch request (only for batch API)

-- Configuration
local product_ids = {}
local api_type = "single"  -- "single" or "batch"
local batch_size = 10      -- Number of IDs per batch request
local current_index = 0
local start_time = nil

-- Benchmark context
local benchmark_context = {
    platform = "localhost",
    database_type = "MySQL",
    instance_count = 1,
    access_pattern = {
        request = "READ",
        throughput = "HEAVY",
        processing_complexity = "Medium"
    }
}

-- Load product IDs from file
function load_product_ids(filename)
    local file = io.open(filename, "r")
    if not file then
        print("Warning: Could not open " .. filename .. ", using test IDs")
        -- Fallback to some test IDs
        for i = 1, 100 do
            table.insert(product_ids, "test-product-" .. i)
        end
        return
    end
    
    for line in file:lines() do
        local id = line:match("^%s*(.-)%s*$")  -- Trim whitespace
        if id and id ~= "" then
            table.insert(product_ids, id)
        end
    end
    file:close()
    
    print("Loaded " .. #product_ids .. " product IDs")
end

-- Parse command line arguments
function parse_args()
    -- wrk passes extra arguments after "--"
    if wrk.args then
        if wrk.args[1] then
            api_type = wrk.args[1]
        end
        if wrk.args[2] then
            batch_size = tonumber(wrk.args[2]) or 10
        end
    end
    print("API type: " .. api_type)
    print("Batch size: " .. batch_size)
end

-- Setup function called once per thread
function setup(thread)
    thread:set("id", current_index)
    current_index = current_index + 1
end

-- Init function called once per thread
function init(args)
    -- Load product IDs
    local script_dir = debug.getinfo(1, "S").source:match("^@(.*/)")
    if script_dir then
        load_product_ids(script_dir .. "product_ids.txt")
    else
        load_product_ids("experiment/product_ids.txt")
    end
    
    parse_args()
    
    -- Record start time
    if not start_time then
        start_time = os.date("%Y-%m-%d-%H-%M-%S")
    end
end

-- Request counter for round-robin through product IDs
local request_counter = 0

-- Generate request based on API type
function request()
    local headers = {}
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    
    local path
    
    if api_type == "batch" then
        -- Batch API: /v1/products?ids=id1,id2,id3
        local ids = {}
        for i = 1, batch_size do
            request_counter = request_counter + 1
            local idx = ((request_counter - 1) % #product_ids) + 1
            table.insert(ids, product_ids[idx])
        end
        path = "/v1/products?ids=" .. table.concat(ids, ",")
    else
        -- Single API: /v1/products/{id}
        request_counter = request_counter + 1
        local idx = ((request_counter - 1) % #product_ids) + 1
        path = "/v1/products/" .. product_ids[idx]
    end
    
    return wrk.format("GET", path, headers)
end

-- Response counter for statistics
local response_count = 0
local error_count = 0
local status_codes = {}

-- Handle response
function response(status, headers, body)
    response_count = response_count + 1
    status_codes[status] = (status_codes[status] or 0) + 1
    
    if status >= 400 then
        error_count = error_count + 1
    end
end

-- Generate timestamp for filename
function get_timestamp()
    return start_time or os.date("%Y-%m-%d-%H-%M-%S")
end

-- Escape string for JSON
function json_escape(str)
    if type(str) ~= "string" then
        return tostring(str)
    end
    str = str:gsub("\\", "\\\\")
    str = str:gsub('"', '\\"')
    str = str:gsub("\n", "\\n")
    str = str:gsub("\r", "\\r")
    str = str:gsub("\t", "\\t")
    return str
end

-- Summary function called when benchmark completes
function done(summary, latency, requests)
    local duration_sec = summary.duration / 1000000
    local rps = summary.requests / duration_sec
    local transfer_mb = summary.bytes / duration_sec / 1024 / 1024
    
    io.write("------------------------------\n")
    io.write("Benchmark Results\n")
    io.write("------------------------------\n")
    io.write(string.format("API Type: %s\n", api_type))
    if api_type == "batch" then
        io.write(string.format("Batch Size: %d\n", batch_size))
    end
    io.write(string.format("Total Requests: %d\n", summary.requests))
    io.write(string.format("Duration: %.2f seconds\n", duration_sec))
    io.write(string.format("Requests/sec: %.2f\n", rps))
    io.write(string.format("Transfer/sec: %.2f MB\n", transfer_mb))
    
    io.write("\nLatency Statistics:\n")
    io.write(string.format("  Min: %.2f ms\n", latency.min / 1000))
    io.write(string.format("  Max: %.2f ms\n", latency.max / 1000))
    io.write(string.format("  Mean: %.2f ms\n", latency.mean / 1000))
    io.write(string.format("  Stdev: %.2f ms\n", latency.stdev / 1000))
    
    io.write("\nPercentiles:\n")
    io.write(string.format("  50%%: %.2f ms\n", latency:percentile(50) / 1000))
    io.write(string.format("  75%%: %.2f ms\n", latency:percentile(75) / 1000))
    io.write(string.format("  90%%: %.2f ms\n", latency:percentile(90) / 1000))
    io.write(string.format("  99%%: %.2f ms\n", latency:percentile(99) / 1000))
    
    io.write("\nStatus Codes:\n")
    for code, count in pairs(status_codes) do
        io.write(string.format("  %d: %d\n", code, count))
    end
    io.write("------------------------------\n")
    
    -- Export to JSON
    local timestamp = get_timestamp()
    local script_dir = debug.getinfo(1, "S").source:match("^@(.*/)")
    local benchmarks_dir
    if script_dir then
        benchmarks_dir = script_dir .. "benchmarks/"
    else
        benchmarks_dir = "experiment/benchmarks/"
    end
    
    -- Create benchmarks directory (using os.execute)
    os.execute("mkdir -p " .. benchmarks_dir)
    
    -- Determine CCU from connections (approximate - wrk doesn't expose this directly)
    local ccu = wrk.connections or "unknown"
    
    local json_filename = benchmarks_dir .. timestamp .. "_benchmark_result.json"
    local json_file = io.open(json_filename, "a")
    
    if json_file then
        local json_result = string.format([[{
  "timestamp": "%s",
  "context": {
    "platform": "%s",
    "database_type": "%s",
    "instance_count": %d,
    "access_pattern": {
      "request": "%s",
      "throughput": "%s",
      "processing_complexity": "%s"
    }
  },
  "benchmark": {
    "api_type": "%s",
    "batch_size": %s,
    "ccu": "%s",
    "duration_seconds": %.2f
  },
  "results": {
    "total_requests": %d,
    "requests_per_second": %.2f,
    "transfer_mb_per_second": %.2f,
    "latency": {
      "min_ms": %.4f,
      "max_ms": %.4f,
      "mean_ms": %.4f,
      "stdev_ms": %.4f,
      "p50_ms": %.4f,
      "p75_ms": %.4f,
      "p90_ms": %.4f,
      "p99_ms": %.4f
    },
    "errors": %d
  }
}
]],
            timestamp,
            benchmark_context.platform,
            benchmark_context.database_type,
            benchmark_context.instance_count,
            benchmark_context.access_pattern.request,
            benchmark_context.access_pattern.throughput,
            benchmark_context.access_pattern.processing_complexity,
            api_type,
            api_type == "batch" and tostring(batch_size) or "null",
            tostring(ccu),
            duration_sec,
            summary.requests,
            rps,
            transfer_mb,
            latency.min / 1000,
            latency.max / 1000,
            latency.mean / 1000,
            latency.stdev / 1000,
            latency:percentile(50) / 1000,
            latency:percentile(75) / 1000,
            latency:percentile(90) / 1000,
            latency:percentile(99) / 1000,
            error_count
        )
        
        json_file:write(json_result)
        json_file:close()
        
        io.write(string.format("\nResults exported to: %s\n", json_filename))
    else
        io.write("\nWarning: Could not write JSON results to file\n")
    end
end
