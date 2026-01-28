#!/bin/bash

# Benchmark runner script for Waterlily
# Usage: ./experiment/run_benchmark.sh --api single --ccu 1000 --duration 30 --timeout 2

set -e

# Default values
API=""
CCU=""
DURATION=30
TIMEOUT=10
BASE_URL="http://localhost:8080"
THREADS=12

# All CCU levels as defined in the spec
ALL_CCU_LEVELS=(100 200 500 1000 2000 5000 10000 20000 50000 100000)

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --api)
            API="$2"
            shift 2
            ;;
        --ccu)
            CCU="$2"
            shift 2
            ;;
        --duration)
            DURATION="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --url)
            BASE_URL="$2"
            shift 2
            ;;
        --threads)
            THREADS="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 --api <single|batch> [options]"
            echo ""
            echo "Options:"
            echo "  --api <single|batch>  API to benchmark (required)"
            echo "  --ccu <number>        Concurrent connections (default: all levels)"
            echo "  --duration <seconds>  Test duration (default: 30)"
            echo "  --timeout <seconds>   Request timeout (default: 2)"
            echo "  --url <url>           Base URL (default: http://localhost:8080)"
            echo "  --threads <number>    Number of threads (default: 12)"
            echo ""
            echo "CCU levels when --ccu is omitted: ${ALL_CCU_LEVELS[*]}"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$API" ]]; then
    echo "Error: --api is required (single or batch)"
    exit 1
fi

if [[ "$API" != "single" && "$API" != "batch" ]]; then
    echo "Error: --api must be 'single' or 'batch'"
    exit 1
fi

# Determine which Lua script to use
if [[ "$API" == "single" ]]; then
    LUA_SCRIPT="experiment/benchmark_single.lua"
    API_NAME="single_product"
else
    LUA_SCRIPT="experiment/benchmark_batch.lua"
    API_NAME="batch_products"
fi

# Check if Lua script exists
if [[ ! -f "$LUA_SCRIPT" ]]; then
    echo "Error: Lua script not found: $LUA_SCRIPT"
    exit 1
fi

# Check if product_ids.txt exists
if [[ ! -f "experiment/product_ids.txt" ]]; then
    echo "Error: experiment/product_ids.txt not found"
    echo "Run: ./gradlew extractProductIds -PproductCount=1000000"
    exit 1
fi

# Create output directory
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="experiment/benchmarks"
mkdir -p "$OUTPUT_DIR"

# Log file for stdout/stderr
LOG_FILE="${OUTPUT_DIR}/result_${TIMESTAMP}__stdout_stderr.log"

# Determine CCU levels to run
if [[ -n "$CCU" ]]; then
    CCU_LEVELS=($CCU)
else
    CCU_LEVELS=("${ALL_CCU_LEVELS[@]}")
fi

echo "=== Waterlily Benchmark ===" | tee "$LOG_FILE"
echo "API: $API" | tee -a "$LOG_FILE"
echo "CCU Levels: ${CCU_LEVELS[*]}" | tee -a "$LOG_FILE"
echo "Duration: ${DURATION}s" | tee -a "$LOG_FILE"
echo "Timeout: ${TIMEOUT}s" | tee -a "$LOG_FILE"
echo "Threads: $THREADS" | tee -a "$LOG_FILE"
echo "Base URL: $BASE_URL" | tee -a "$LOG_FILE"
echo "Timestamp: $TIMESTAMP" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Health check
echo "Checking health endpoint..." | tee -a "$LOG_FILE"
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/health" 2>&1 || true)
if [[ "$HEALTH_RESPONSE" != "200" ]]; then
    echo "Error: Health check failed (HTTP $HEALTH_RESPONSE)" | tee -a "$LOG_FILE"
    echo "Make sure the application is running at $BASE_URL" | tee -a "$LOG_FILE"
    exit 1
fi
echo "Health check passed" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Run benchmarks for each CCU level
for ccu in "${CCU_LEVELS[@]}"; do
    OUTPUT_FILE="${OUTPUT_DIR}/result_${TIMESTAMP}_${API_NAME}_${ccu}.json"
    
    echo "----------------------------------------" | tee -a "$LOG_FILE"
    echo "Running benchmark: API=$API, CCU=$ccu" | tee -a "$LOG_FILE"
    echo "Output: $OUTPUT_FILE" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
    
    # Calculate actual threads (should not exceed CCU)
    ACTUAL_THREADS=$THREADS
    if [[ $ccu -lt $THREADS ]]; then
        ACTUAL_THREADS=$ccu
    fi
    
    # Run wrk benchmark with environment variables for CCU and output file
    # Export as environment variables so Lua's os.getenv() can read them
    export WRK_CCU="$ccu"
    export WRK_OUTPUT_FILE="$OUTPUT_FILE"
    
    wrk -t"$ACTUAL_THREADS" -c"$ccu" -d"${DURATION}s" --timeout "${TIMEOUT}s" \
        -s "$LUA_SCRIPT" "$BASE_URL" 2>&1 | tee -a "$LOG_FILE"
    
    # Check if JSON file was created
    if [[ -s "$OUTPUT_FILE" ]]; then
        echo "JSON file created successfully: $OUTPUT_FILE" | tee -a "$LOG_FILE"
    else
        echo "Warning: JSON file is empty or not created" | tee -a "$LOG_FILE"
    fi
    
    echo "" | tee -a "$LOG_FILE"
    
    # Small delay between runs
    if [[ ${#CCU_LEVELS[@]} -gt 1 ]]; then
        echo "Cooling down for 5 seconds..." | tee -a "$LOG_FILE"
        sleep 5
    fi
done

echo "========================================" | tee -a "$LOG_FILE"
echo "Benchmark complete!" | tee -a "$LOG_FILE"
echo "Results saved to: $OUTPUT_DIR" | tee -a "$LOG_FILE"
echo "Log file: $LOG_FILE" | tee -a "$LOG_FILE"

# List generated JSON files
echo "" | tee -a "$LOG_FILE"
echo "Generated JSON files:" | tee -a "$LOG_FILE"
ls -la "${OUTPUT_DIR}/result_${TIMESTAMP}_${API_NAME}_"*.json 2>/dev/null | tee -a "$LOG_FILE" || echo "No JSON files found" | tee -a "$LOG_FILE"
