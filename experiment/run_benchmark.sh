#!/bin/bash
# Script to run wrk benchmarks with different CCUs and API types
# Make sure your server is running before executing this script

set -e

# Configuration
BASE_URL="http://localhost:8080"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BENCHMARK_SCRIPT="$SCRIPT_DIR/benchmark.lua"
BENCHMARKS_DIR="$SCRIPT_DIR/benchmarks"

# Threads (adjust based on your CPU cores)
THREADS=12

# Duration for each test
DURATION="30s"

# CCU levels to test
CCUS=(100 200 500 1000 2000 5000 10000 20000 50000 100000)

# API types to test
API_TYPES=("single" "batch")

# Batch sizes for batch API
BATCH_SIZES=(10 50)

# Generate timestamp for this benchmark run
TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Waterlily Benchmark Suite${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Base URL: ${YELLOW}$BASE_URL${NC}"
echo -e "Timestamp: ${YELLOW}$TIMESTAMP${NC}"
echo -e "Duration per test: ${YELLOW}$DURATION${NC}"
echo -e "Threads: ${YELLOW}$THREADS${NC}"
echo ""

# Create benchmarks directory
mkdir -p "$BENCHMARKS_DIR"

# Check if server is running
echo -e "${YELLOW}Checking if server is running...${NC}"
if ! curl -s "$BASE_URL/health" > /dev/null 2>&1; then
    echo -e "${RED}Error: Server is not running at $BASE_URL${NC}"
    echo "Please start the server first with: ./gradlew run"
    exit 1
fi
echo -e "${GREEN}Server is running!${NC}"
echo ""

# Check if product_ids.txt exists
if [ ! -f "$SCRIPT_DIR/product_ids.txt" ]; then
    echo -e "${YELLOW}Warning: product_ids.txt not found. Run extract_product_ids first.${NC}"
    echo "Creating sample product_ids.txt with test IDs..."
    for i in $(seq 1 1000); do
        echo "test-product-$i"
    done > "$SCRIPT_DIR/product_ids.txt"
fi

# Initialize results file with JSON array start
RESULTS_FILE="$BENCHMARKS_DIR/${TIMESTAMP}_benchmark_results.json"
echo "[" > "$RESULTS_FILE"
FIRST_RESULT=true

# Function to run a single benchmark
run_benchmark() {
    local api_type=$1
    local ccu=$2
    local batch_size=$3
    
    echo -e "${YELLOW}----------------------------------------${NC}"
    if [ "$api_type" == "batch" ]; then
        echo -e "Running: API=${GREEN}$api_type${NC}, CCU=${GREEN}$ccu${NC}, BatchSize=${GREEN}$batch_size${NC}"
    else
        echo -e "Running: API=${GREEN}$api_type${NC}, CCU=${GREEN}$ccu${NC}"
    fi
    echo -e "${YELLOW}----------------------------------------${NC}"
    
    # Run wrk benchmark
    if [ "$api_type" == "batch" ]; then
        wrk -t$THREADS -c$ccu -d$DURATION -s "$BENCHMARK_SCRIPT" "$BASE_URL" -- "$api_type" "$batch_size"
    else
        wrk -t$THREADS -c$ccu -d$DURATION -s "$BENCHMARK_SCRIPT" "$BASE_URL" -- "$api_type"
    fi
    
    echo ""
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -q, --quick         Quick mode: fewer CCUs (100, 1000, 10000)"
    echo "  -s, --single        Run single API benchmarks only"
    echo "  -b, --batch         Run batch API benchmarks only"
    echo "  -c, --ccu <value>   Run with specific CCU only"
    echo "  -d, --duration <s>  Set duration (default: 30s)"
    echo ""
    echo "Examples:"
    echo "  $0                  # Full benchmark suite"
    echo "  $0 -q               # Quick benchmark"
    echo "  $0 -s -c 1000       # Single API with 1000 CCU"
}

# Parse command line arguments
QUICK_MODE=false
SINGLE_ONLY=false
BATCH_ONLY=false
SPECIFIC_CCU=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -q|--quick)
            QUICK_MODE=true
            CCUS=(100 1000 10000)
            shift
            ;;
        -s|--single)
            SINGLE_ONLY=true
            shift
            ;;
        -b|--batch)
            BATCH_ONLY=true
            shift
            ;;
        -c|--ccu)
            SPECIFIC_CCU="$2"
            CCUS=("$2")
            shift 2
            ;;
        -d|--duration)
            DURATION="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
done

# Determine which API types to run
if [ "$SINGLE_ONLY" = true ]; then
    API_TYPES=("single")
elif [ "$BATCH_ONLY" = true ]; then
    API_TYPES=("batch")
fi

# Count total tests
TOTAL_TESTS=0
for api_type in "${API_TYPES[@]}"; do
    if [ "$api_type" == "batch" ]; then
        TOTAL_TESTS=$((TOTAL_TESTS + ${#CCUS[@]} * ${#BATCH_SIZES[@]}))
    else
        TOTAL_TESTS=$((TOTAL_TESTS + ${#CCUS[@]}))
    fi
done

echo -e "Total tests to run: ${YELLOW}$TOTAL_TESTS${NC}"
echo ""

# Run benchmarks
TEST_COUNT=0
for api_type in "${API_TYPES[@]}"; do
    if [ "$api_type" == "batch" ]; then
        for batch_size in "${BATCH_SIZES[@]}"; do
            for ccu in "${CCUS[@]}"; do
                TEST_COUNT=$((TEST_COUNT + 1))
                echo -e "${GREEN}Test $TEST_COUNT/$TOTAL_TESTS${NC}"
                run_benchmark "$api_type" "$ccu" "$batch_size"
            done
        done
    else
        for ccu in "${CCUS[@]}"; do
            TEST_COUNT=$((TEST_COUNT + 1))
            echo -e "${GREEN}Test $TEST_COUNT/$TOTAL_TESTS${NC}"
            run_benchmark "$api_type" "$ccu" ""
        done
    fi
done

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Benchmark Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Results saved to: ${YELLOW}$BENCHMARKS_DIR/${NC}"
echo -e "Look for files starting with: ${YELLOW}$TIMESTAMP${NC}"
