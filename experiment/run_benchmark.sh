#!/bin/bash
# Script to run wrk benchmark against localhost:8080
# Make sure your server is running before executing this script

echo "Starting benchmark against http://localhost:8080"
echo "Make sure your server is running on port 8080!"
echo ""

# Default parameters:
# -t12: 12 threads
# -c400: 400 connections
# -d30s: 30 seconds duration
# -s: Lua script for custom request handling
wrk -t12 -c400 -d30s -s benchmark.lua http://localhost:8080

