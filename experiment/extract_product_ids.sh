#!/bin/bash
# Script to extract product IDs from the database for benchmarking
# This runs the Kotlin ExtractProductIds tool

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default values
COUNT=${1:-10000}
OUTPUT_FILE=${2:-"$SCRIPT_DIR/product_ids.txt"}

echo "========================================"
echo "  Product ID Extractor"
echo "========================================"
echo ""
echo "Count: $COUNT"
echo "Output: $OUTPUT_FILE"
echo ""

# Change to project root
cd "$PROJECT_ROOT"

# Run the Kotlin tool
./gradlew extractProductIds -PidCount="$COUNT" -PoutputFile="$OUTPUT_FILE" --quiet

echo ""
echo "Done! Product IDs saved to: $OUTPUT_FILE"

