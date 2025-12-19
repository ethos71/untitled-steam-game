#!/bin/bash
# Quick script to run the NES-style game

echo "========================================="
echo "  NES ROGUELIKE ADVENTURE"
echo "========================================="
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q pygame 2>/dev/null

echo ""
echo "Starting game..."
echo ""
echo "CONTROLS:"
echo "  WASD / Arrows - Move"
echo "  TAB - Menu (Equipment & Options)"
echo "  SPACE - Open treasure chests"
echo "  R - Regenerate world"
echo "  C - Toggle CRT effects"
echo "  ESC - Quit"
echo ""
echo "========================================="
echo ""

python src/engine/game_nes.py
