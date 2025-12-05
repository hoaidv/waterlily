#!/bin/bash
# Runner script for the product scraper

cd "$(dirname "$0")/scrapers"

# Check if sample mode
if [ "$1" == "--sample" ] || [ "$1" == "-s" ]; then
    echo "Running in SAMPLE mode..."
    python3 orchestrator.py --sample
elif [ "$1" == "--resume" ] || [ "$1" == "-r" ]; then
    echo "Resuming from checkpoint..."
    python3 orchestrator.py --resume
elif [ "$1" == "--full" ] || [ "$1" == "-f" ]; then
    echo "Running FULL scrape..."
    python3 orchestrator.py
else
    echo "Usage: $0 [--sample|-s] [--resume|-r] [--full|-f]"
    echo "  --sample, -s : Run sample scrape (5 products per website)"
    echo "  --resume, -r : Resume from checkpoint"
    echo "  --full, -f   : Run full scrape (10 products per website)"
    exit 1
fi

