#!/bin/bash

# Script to run the Amazon scraper

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}   Amazon Product Scraper${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run the scraper
echo ""
echo -e "${GREEN}Starting scraper...${NC}"
echo ""

cd scrapers

# Check if arguments provided
if [ $# -eq 0 ]; then
    # No arguments - run with sample categories
    echo -e "${YELLOW}No categories specified, running with sample categories...${NC}"
    python3 orchestrator.py --sample
else
    # Run with provided categories
    echo -e "${YELLOW}Running with categories: $@${NC}"
    python3 orchestrator.py --categories "$@"
fi

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Scraping completed successfully${NC}"
else
    echo ""
    echo -e "${RED}✗ Scraping failed${NC}"
    exit 1
fi

# Deactivate virtual environment
deactivate

echo ""
echo -e "${GREEN}Check ./output/ for results${NC}"

