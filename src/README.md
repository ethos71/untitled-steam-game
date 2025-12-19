# ASCII Roguelike Game

A procedurally generated ASCII roguelike game built with Python and tcod.

## Installation

1. **Create virtual environment** (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Game

### Option 1: NES-Style Version (Recommended)
Modern pygame version with retro graphics:
```bash
cd engine
python3 game_nes.py
```

### Option 2: ASCII Simple Version
Uses default tcod font, no additional files needed:
```bash
cd engine
python3 game_simple.py
```

### Option 3: ASCII Full Version
Requires font file (dejavu10x10_gs_tc.png):
```bash
cd engine
python3 main.py
```

## Controls

### Movement
- **Arrow Keys** or **hjkl** (vi-style): Move in 4 directions
- **yubn** (vi-style diagonals):
  - `y` = up-left
  - `u` = up-right
  - `b` = down-left
  - `n` = down-right

### Actions
- **r**: Regenerate world (new random map)
- **ESC**: Quit game

## Game Features

### World Elements
- **@ (Hero)**: Your character (white)
- **♣♠T↑ (Trees)**: Block movement and sight (green)
- **○●*◘ (Rocks)**: Block movement (gray)
- **~≈∼ (Rivers)**: Block movement (blue)
- **.,'" (Grass)**: Walkable ground (light green)

### Procedural Generation
- Random winding rivers (1-3 per map)
- Forest patches with clustered trees
- Scattered rocks
- Grass base layer
- Hero always spawns at center on walkable terrain

### UI
- HP display (bottom left)
- Position coordinates (bottom center)
- Control hints (bottom right)

## Project Structure

```
src/
├── engine/
│   ├── game_nes.py      # NES-style pygame game
│   ├── game_simple.py   # ASCII game with default font
│   └── main.py          # ASCII game with custom font
├── hero/
│   └── hero.py          # Hero character class
├── enemy/
│   └── enemy.py         # Enemy types and AI
├── boss/
│   └── boss.py          # Boss enemies with phases
├── villain/
│   └── villain.py       # Main villain and story
├── legendary/
│   └── legendary.py     # Legendary encounters
├── story/
│   ├── story.py         # Story progression
│   └── dialogue.py      # Dialogue system
├── items/
│   ├── item.py          # Base item class
│   ├── weapon.py        # Weapons
│   └── inventory.py     # Inventory
├── scenery/
│   └── terrain.py       # Terrain elements
├── world/
│   └── world_generator.py  # Procedural generation
└── requirements.txt     # Python dependencies
```

## Development

### Test World Generation Only
```bash
cd world
python3 world_generator.py
```

### Adjust World Parameters
Edit `engine/game_simple.py`, `engine/main.py`, or `engine/game_nes.py`:
```python
# Change world size (in game files)
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 60

# Change terrain density (in world_generator.py)
self._generate_trees(density=0.20)  # More trees
self._generate_rocks(density=0.10)  # More rocks
```

## Next Features to Add

- [ ] Field of View (FOV) system
- [ ] Monsters/enemies
- [ ] Combat system
- [ ] Items and inventory
- [ ] Multiple dungeon levels
- [ ] Save/load system
- [ ] Sound effects
- [ ] Steam achievements

## Troubleshooting

### Import Errors
Make sure you're in the `src/engine/` directory when running:
```bash
cd src/engine
python3 game_nes.py
# or
python3 game_simple.py
```

### tcod Not Found
Install dependencies:
```bash
pip install -r requirements.txt
```

### Font File Missing (main.py)
Use `game_simple.py` instead, or download the font from:
https://github.com/libtcod/python-tcod/tree/main/fonts

## Credits

Built with:
- [python-tcod](https://github.com/libtcod/python-tcod) - Roguelike library
- Python 3.8+

---
*Game created: 2025-12-18*
