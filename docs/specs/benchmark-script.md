# Benchmark Script Specification

This document defines the benchmark execution approach for the Waterlily project.

## Overview

For each chosen "benchmark context", the benchmark script measures API performance under varying concurrent loads.

**Related Documents:**
- [API Specification](api-spec.md) - Endpoints to benchmark
- [Non-Functional Requirements](nfr.md) - Performance targets and CCU levels
- [Technical Constraints](constraints.md) - Tool and environment constraints
- [Glossary](glossary.md) - Term definitions (CCU, RPS, TPS, etc.)

---

## Benchmark Tools

| Tool | Purpose |
|------|---------|
| wrk | HTTP load generator |
| Lua | Script for request customization |

---

## Benchmark Aspects

Definitions

- A benchmark aspect is a combination of API x CCU.
- A benchmark run may execute the benchmark on multiple aspects (e.g. fix API, but vary CCU).

### APIs Under Test

| API | Endpoint | Method | Reference |
|-----|----------|--------|-----------|
| Get Single Product | `/api/v1/products/{id}` | GET | [API Spec](api-spec.md#get-product-by-id) |
| Get Products Batch | `/api/v1/products/batch` | POST | [API Spec](api-spec.md#get-products-batch) |

### Concurrency Levels (CCU)

As defined in [NFR-003](nfr.md#nfr-003-concurrency-support):

| Level | CCU | wrk flag |
|-------|-----|----------|
| Low | 100 | `--connections 100` |
| Low | 200 | `--connections 200` |
| Low | 500 | `--connections 500` |
| Medium | 1,000 | `--connections 1000` |
| Medium | 2,000 | `--connections 2000` |
| Medium | 5,000 | `--connections 5000` |
| High | 10,000 | `--connections 10000` |
| High | 20,000 | `--connections 20000` |
| High | 50,000 | `--connections 50000` |
| Extreme | 100,000 | `--connections 100000` |

---

## Benchmark Matrix

Possible combinations from APIs x CCU Levels.

| API | CCU Levels |
|-----|------------|
| Single Product | 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000 |
| Batch Products | 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000 |

**Total runs:** 20 (2 APIs x 10 CCU levels)

---

## Input Data

### Product IDs Extractor

Need to write an `extract_product_ids` to extract product IDs from MySQL to `experiment/product_ids.txt`.
* Unique IDs to extract 1,000,000
* Writen using Kotlin and bash
  - Kotlin for actual extractor logic
  - `./gradlew` to invoke the script
* Arguments as properties
  - `-PproductCount`
  - `-PresultFile`

### Product IDs File

Location: `experiment/product_ids.txt`

Format: One product ID per line

```
446655440000
446655440001
446655440002
...
```

**Requirement:** File should contain sufficient IDs to avoid repetition during benchmark (minimum 10,000 unique IDs recommended).

---

## Bechmark Aspect Output

One benchmark aspect result is saved to one output file, not sharing 
with other benchmark aspects, not sharing with benchmark run stdout, stderr.

```
experiment/benchmarks/result_<timestamp>_<api>_<ccu>.json
```

### JSON Result Structure

```json
{
  "benchmark_context": {
    "platform": "localhost",
    "database_type": "MySQL",
    "database_instances": 1,
    "access_pattern": {
      "request_type": "READ",
      "throughput": "HEAVY",
      "complexity": "MEDIUM"
    }
  },
  "benchmark_target": {
    "api": "single_product",
    "endpoint": "GET /api/v1/products/{id}",
    "ccu": 1000
  },
  "timestamp": "2026-01-28T10:30:00Z",
  "duration_seconds": 60,
  "metrics": {
    "requests_total": 1250000,
    "rps": 20833,
    "latency": {
      "min_ms": 0.5,
      "avg_ms": 48.2,
      "max_ms": 512.0,
      "stdev_ms": 15.3,
      "p50_ms": 45.0,
      "p95_ms": 82.0,
      "p99_ms": 120.0
    },
    "transfer": {
      "total_mb": 6250,
      "rate_mbps": 104.2
    },
    "errors": {
      "socket.connect": 0,
      "socket.read": 0,
      "socket.write": 0,
      "socket.timeout": 0,
      "4xx": 0,
      "5xx": 0
    }
  }
}
```

## Benchmark Run Output

One benchmark run may results in many benchmark aspect output files.
But all its stdout, stderr are saved into one file.

```
experiment/benchmarks/result_<timestamp>__stdout_stderr.log
```

---

## Metrics Collected

### Throughput Metrics

| Metric | Description | Unit |
|--------|-------------|------|
| requests_total | Total requests completed | count |
| rps | Requests per second | req/s |

### Latency Metrics

| Metric | Description | Unit |
|--------|-------------|------|
| min_ms | Minimum latency | ms |
| avg_ms | Average latency | ms |
| max_ms | Maximum latency | ms |
| stdev_ms | Standard deviation | ms |
| p50_ms | 50th percentile (median) | ms |
| p95_ms | 95th percentile | ms |
| p99_ms | 99th percentile | ms |

### Transfer Metrics

| Metric | Description | Unit |
|--------|-------------|------|
| total_mb | Total data transferred | MB |
| rate_mbps | Transfer rate | MB/s |

### Error Metrics

- We collect socket errors from `summary` argument of `wrk` `done` handler.
- We collect http errors by counting at `wrk` `response` handler

| Metric | Description | Unit |
|--------|-------------|------|
| socket.connect | Total socket connect errors | count |
| socket.read | Total socket read errors | count |
| socket.write | Total socket write errors | count |
| socket.timeout | Total socket timeout errors | count |
| 4xx | Total client errors | count |
| 5xx | Total server errors | count |

---

## Execution

### Example wrk Command

```bash
wrk -t12 -c1000 -d60s --timeout 30s -s benchmark.lua http://localhost:8080 -- init_arg1 init_arg2 init_arg3
```

| Flag | Value | Description |
|------|-------|-------------|
| -t | 12 | Number of threads |
| -c | 1000 | Number of connections (CCU) |
| -d | 60s | Duration |
| --timeout | 30s | Request timeout |
| -s | benchmark.lua | Lua script |

### Benchmark Script Runner

```bash
./experiment/run_benchmark.sh --api single --ccu 1000 --duration 30 --timeout 30
```

#### Arguments

| Flag  | Required | Description |
|------ | -------| -------------|
| --api | Required | Type of API to benchmark |
| --ccu | Optional | CCU level to benchmark. Default to all concurrency levels. |
| --duration | Optional | CCU level to benchmark. Default to `30s` (30 seconds). |
| --timeout | Optional | CCU level to benchmark. Default to `2s` (2 seconds). |

#### Important fixes

- Number of connection (CCU) is unavailable at `wrk`'s `done` handler, 
  we have to pass it to `wrk`'s `init` handler by appending at the end of the
  `wrk` invocation (`wrk ... -- init_arg1 init_arg2 init_arg3`)
- If user omits the `--ccu` flag, the script will loop through all concurrency levels 
  as described in section `Concurrency Levels` above.
  
Thus, a single benchmark script run may produce multiple benchmark 
output files of different CCUs.

---

## Result Visualization

Results should support:

1. **RPS Comparison** - Compare RPS across different benchmark contexts, APIs, and CCU levels
2. **Latency Distribution** - Visualize p50/p95/p99 for each API at each CCU level
3. **Scalability Curve** - Plot RPS vs CCU to identify scaling limits
4. **Transfer Analysis** - Monitor data transfer rates for bandwidth planning

---

## Pre-benchmark Checklist

- [ ] MySQL database is running and warmed up
- [ ] Run product IDs extractor
- [ ] Product IDs file is generated (`experiment/product_ids.txt`)
- [ ] Application is running on port 8080
- [ ] Health check passes: `curl http://localhost:8080/health`