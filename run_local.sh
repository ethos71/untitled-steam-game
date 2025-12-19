#!/bin/bash
# Run the game locally

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Run './build_local.sh' first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the game
echo "Starting game..."
python3 main.py
