#!/usr/bin/env python3
"""
Main entry point for the game
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from engine.game_nes import main

if __name__ == "__main__":
    main()
