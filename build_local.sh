#!/bin/bash
# Local build script for testing

echo "Building Untitled Steam Game locally..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Build complete! Run './run_local.sh' to play the game."
