# NES/Atari-Style Roguelike Game

## Game Style
**THIS IS A NES/ATARI-STYLE PIXEL ART GAME - NOT ASCII**

- **Graphics**: 16x16 pixel tiles with NES color palette
- **Engine**: Python + pygame
- **Style**: Authentic retro NES/Atari aesthetics
- **Resolution**: 800x600 with scrolling camera
- **Framerate**: 60 FPS

## Key Features
- Pixel art tiles for terrain (grass, trees, rocks, water)
- Sprite-based hero character
- NES authentic color palette
- Smooth scrolling camera system
- Retro UI with pixel fonts

## NES Color Palette
```python
NES_PALETTE = {
    'black': (0, 0, 0),
    'grass': (0, 168, 0),
    'tree': (0, 88, 0),
    'rock': (124, 124, 124),
    'water': (0, 120, 248),
    'hero': (252, 160, 68),
    'ui_bg': (24, 24, 24),
    'ui_text': (248, 248, 248),
}
```

## Current Implementation
- **Main Game**: `src/engine/game_simple.py`
- **Tile Size**: 16x16 pixels
- **Map Size**: 50x38 tiles
- **Controls**: WASD/Arrow keys for movement

## No ASCII
This game uses pixel graphics, NOT text characters. All terrain and sprites are rendered as colored rectangles/circles using pygame's drawing functions, or will use actual pixel art sprites from free asset packs.

## Next Steps
1. Replace colored shapes with actual 16x16 PNG sprite tiles
2. Add character animations
3. Implement proper tileset system
4. Add sound effects and music
5. Create NES-style UI elements
