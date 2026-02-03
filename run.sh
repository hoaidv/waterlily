#!/bin/bash

# Run the Waterlily application with optimized JVM settings
# Usage: ./run.sh [build]
#   - ./run.sh        : Run the application (assumes JAR is already built)
#   - ./run.sh build  : Build the JAR first, then run

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JAR_FILE="$SCRIPT_DIR/build/libs/waterlily.jar"

# JVM Memory Settings
# - Xms: Initial heap size
# - Xmx: Maximum heap size  
# - XX:+UseG1GC: Use G1 garbage collector (good for large heaps)
# - XX:MaxGCPauseMillis: Target max GC pause time
JVM_OPTS="${JVM_OPTS:--Xms512m -Xmx16g -XX:+UseG1GC -XX:MaxGCPauseMillis=200}"

# Build if requested or JAR doesn't exist
if [[ "$1" == "build" ]] || [[ ! -f "$JAR_FILE" ]]; then
    echo "Building fat JAR..."
    cd "$SCRIPT_DIR"
    ./gradlew buildFatJar --no-daemon -q
    echo "Build complete: $JAR_FILE"
fi

# Check JAR exists
if [[ ! -f "$JAR_FILE" ]]; then
    echo "Error: JAR file not found at $JAR_FILE"
    echo "Run './run.sh build' to build the application first"
    exit 1
fi

echo "Starting Waterlily with JVM options: $JVM_OPTS"
echo "JAR: $JAR_FILE"
echo ""

# Run the application
exec java $JVM_OPTS -jar "$JAR_FILE"
