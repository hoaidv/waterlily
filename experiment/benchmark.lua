-- Wrk Lua script for benchmarking the server at localhost:8080
-- Usage: wrk -t12 -c400 -d30s -s benchmark.lua http://localhost:8080

-- Initialize request counter
request_counter = 0

-- Customize each request
request = function()
    request_counter = request_counter + 1
    
    -- You can customize headers here
    headers = {}
    headers["Content-Type"] = "application/json"
    
    -- You can customize the request path and method
    -- For example, if you want to hit a specific endpoint:
    -- return wrk.format("GET", "/api/endpoint", headers)
    
    -- Default: simple GET request to root
    return wrk.format("GET", "/", headers)
end

-- Handle response (optional - for logging or custom metrics)
response = function(status, headers, body)
    -- Log every 1000th response
    if request_counter % 1000 == 0 then
        print(string.format("Request #%d: Status %d", request_counter, status))
    end
end

-- Summary function called when benchmark completes
done = function(summary, latency, requests)
    io.write("------------------------------\n")
    io.write(string.format("Total Requests: %d\n", summary.requests))
    io.write(string.format("Duration: %.2f seconds\n", summary.duration / 1000000))
    io.write(string.format("Requests/sec: %.2f\n", summary.requests / (summary.duration / 1000000)))
    io.write(string.format("Transfer/sec: %.2f MB\n", summary.bytes / (summary.duration / 1000000) / 1024 / 1024))
    
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
    io.write("------------------------------\n")
end

