# Quick Start: NES-Style Game

## Installation

```bash
# Navigate to project
cd /home/dominick/workspace/untitled-steam-game

# Install pygame
pip install pygame

# Or install all dependencies
pip install -r src/requirements.txt
```

## Running the Game

```bash
cd src/engine
python3 game_nes.py
```

## What You'll See

A **retro NES-style roguelike** with:
- 16x16 pixel tiles
- Authentic NES color palette
- Smooth camera scrolling
- Animated water tiles
- CRT scanline effects
- Graphical HP bar

## Controls

### Movement
- **WASD**: Move (4 directions)
- **Arrow Keys**: Move (4 directions)
- **hjkl**: Vi-style movement
- **yubn**: Diagonal movement

### Actions
- **R**: Regenerate world (new random map)
- **C**: Toggle CRT scanline effect
- **F**: Toggle FPS counter
- **ESC**: Quit game

## Features

### Procedural Graphics
The game generates all graphics in code - no external image files needed!

### NES Authenticity
- 16x16 tiles (NES standard)
- 54-color NES palette
- Scanline effects
- Limited color per sprite

### Performance
- 60 FPS target
- Smooth scrolling camera
- Efficient tile rendering

## Differences from ASCII Version

| Feature | ASCII (tcod) | NES (pygame) |
|---------|--------------|--------------|
| Graphics | Text characters | 16x16 pixel tiles |
| Colors | RGB colors | NES palette |
| View | Full map | Scrolling camera |
| Effects | None | CRT, scanlines |
| Animation | Static | Animated tiles |
| Window | Terminal-like | Retro game window |

## What's Next?

1. **Play the game** - Explore the procedural world
2. **Try effects** - Press C for CRT, F for FPS
3. **Regenerate** - Press R for a new world
4. **Create assets** - See `assets/README.md` for tile creation
5. **Customize** - Edit `game_nes.py` to change colors, sizes, etc.

## Customization

### Change Screen Size
```python
# In game_nes.py
SCREEN_WIDTH = TILE_SIZE * 40  # Wider view
SCREEN_HEIGHT = TILE_SIZE * 30  # Taller view
```

### Change Tile Size
```python
TILE_SIZE = 24  # Larger tiles
```

### Change Colors
```python
# Edit NES_COLORS dictionary
NES_COLORS = {
    'grass': (100, 200, 100),  # Custom green
    # ...
}
```

### Disable CRT Effect
```python
# In __init__
self.crt_effect = False  # Start with CRT off
```

## Troubleshooting

### "No module named pygame"
```bash
pip install pygame
```

### "No module named world"
Make sure you're in the correct directory:
```bash
cd src/engine
python3 game_nes.py
```

### Low FPS
- Press C to disable CRT effects
- Close other applications
- Reduce map size in game_nes.py

### Window too small
Change screen size constants in game_nes.py (lines 12-14)

## Next Steps

See `migration-guide.md` for:
- Creating custom tile assets
- Adding sound effects
- Implementing animations
- Building for Steam

---
*Created: 2025-12-18*
