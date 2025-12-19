# GAME STYLE: NES/ATARI PIXEL ART

## ⚠️ CRITICAL: NOT AN ASCII GAME

This is a **NES/Atari-style PIXEL ART game**, NOT an ASCII text-based game.

## Graphics Specifications
- **Tile Size**: 16x16 pixels
- **Color Palette**: Authentic NES colors
- **Rendering**: pygame sprite/surface system
- **Style**: Retro pixel art (like classic NES/Atari games)

## Current Implementation
- **Engine**: pygame (NOT tcod)
- **Main File**: `src/engine/game_simple.py`
- **Resolution**: 800x600 pixels
- **Camera**: Smooth scrolling following player
- **FPS**: 60

## What This Means
- ❌ NO text characters (like @, #, ., etc.)
- ❌ NO ASCII art
- ✅ YES 16x16 pixel sprites and tiles
- ✅ YES NES color palette
- ✅ YES retro pixel art style

## Controls
- **WASD/Arrow Keys**: Move player
- **R**: Regenerate world
- **ESC**: Quit

## To Run
```bash
source venv/bin/activate
python src/engine/game_simple.py
```

## References
- See `docs/robots/nes-atari-style-game.md` for full details
- See `.github/agents/@idunno.json` for project structure
- See `.github/prompts/@idunno.md` for development guidelines
