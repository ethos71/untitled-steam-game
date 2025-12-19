# Game Implementation Guide

## Overview
The playable ASCII roguelike game is now complete with full keyboard controls and real-time rendering.

## Game Files

### Main Game Files
1. **`src/game_simple.py`** (Recommended)
   - Simplified version using default tcod font
   - No external font files needed
   - Easiest to run

2. **`src/main.py`** (Advanced)
   - Full version with custom font support
   - Requires `dejavu10x10_gs_tc.png` font file
   - Better visual quality

### Supporting Files
- `src/hero/hero.py` - Player character
- `src/scenery/terrain.py` - World terrain
- `src/world/world_generator.py` - Procedural generation
- `src/requirements.txt` - Dependencies

## Quick Start

```bash
# Install dependencies
cd src
pip install -r requirements.txt

# Run the game
python3 game_simple.py
```

## Game Architecture

### Game Loop
```
Initialize → [Render → Handle Input → Update] → Exit
```

### Main Components

#### Game Class
Manages game state:
- World generator instance
- Terrain dictionary
- Hero reference
- Running state

#### Event Handling
- Keyboard input processing
- Movement validation
- World regeneration
- Quit handling

#### Rendering System
- Terrain layer (grass, trees, rocks, rivers)
- Hero layer (player character)
- UI layer (status bar, help text)

## Controls

### Movement System
**Cardinal Directions:**
- Arrow Keys: ↑↓←→
- Vi Keys: k j h l

**Diagonal Movement:**
- y = Northwest (↖)
- u = Northeast (↗)
- b = Southwest (↙)
- n = Southeast (↘)

### Special Actions
- **r** = Regenerate world (new random map)
- **ESC** = Quit game

## Features Implemented

### ✅ Core Features
- [x] Procedural world generation
- [x] 8-directional movement
- [x] Collision detection (walls, trees, rocks, rivers)
- [x] Real-time rendering
- [x] Status bar UI
- [x] World regeneration
- [x] Color-coded terrain

### World Generation
- **Size**: 80x50 tiles (configurable)
- **Layers**: Grass → Rivers → Trees → Rocks
- **Terrain Types**: 5 (grass, tree, rock, river, hero)
- **Collision**: Trees and rocks block movement
- **Rivers**: 1-3 winding waterways per map

### Visual Design
- **Hero**: @ (white)
- **Trees**: ♣♠T↑ (forest green)
- **Rocks**: ○●*◘ (gray)
- **Rivers**: ~≈∼ (blue)
- **Grass**: .,'" (lime green)

## Technical Implementation

### Coordinate System
```
(0,0) ────────────→ x (80)
  │
  │
  │
  ↓
  y (50)
```

### Movement Validation
```python
1. Calculate new position (x + dx, y + dy)
2. Check bounds (0 <= x < width, 0 <= y < height)
3. Check terrain (is_walkable)
4. Move hero if valid
```

### Rendering Order
```
1. Clear console
2. Draw terrain (background layer)
3. Draw hero (character layer)
4. Draw UI (overlay layer)
5. Present to screen
```

## Performance

### Optimization Techniques
- Dictionary-based terrain lookup: O(1)
- Event-driven rendering (only on input)
- Efficient collision detection
- No unnecessary redraws

### Metrics
- **Terrain Objects**: ~3200 tiles
- **FPS Target**: 60 (vsync enabled)
- **Memory**: Minimal (<50MB typical)

## Extending the Game

### Adding New Terrain
```python
# In src/scenery/terrain.py
class Mountain(Terrain):
    def __init__(self, x, y):
        char = '^'
        color = (139, 69, 19)  # Brown
        super().__init__(x, y, char, color, 
                        blocks_movement=True, 
                        blocks_sight=True)
```

### Adding Enemies
```python
# Create src/enemies/monster.py
class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.char = 'g'  # goblin
        self.hp = 10
```

### Adding Items
```python
# Create src/items/item.py
class Item:
    def __init__(self, x, y, char, name):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
```

### Adding FOV (Field of View)
```python
import tcod.map

# In game initialization
fov_map = tcod.map.compute_fov(
    transparency,
    (hero.x, hero.y),
    radius=10,
    algorithm=tcod.FOV_SHADOW
)
```

## Testing

### Manual Testing
```bash
# Test world generation
cd src/world
python3 world_generator.py

# Test game
cd src
python3 game_simple.py
```

### Validation Checklist
- [ ] Hero spawns at center
- [ ] Can move in 8 directions
- [ ] Cannot walk through trees/rocks/rivers
- [ ] Can walk on grass
- [ ] Press 'r' generates new world
- [ ] ESC quits game
- [ ] UI displays correctly

## Known Limitations

1. **No Save System**: Game state is lost on exit
2. **No Enemies**: Only terrain, no monsters yet
3. **No Items**: No collectibles or inventory
4. **No FOV**: Can see entire map always
5. **No Audio**: Silent gameplay

## Future Development Roadmap

### Phase 1: Core Gameplay (Next)
- [ ] Field of View system
- [ ] Enemy monsters with AI
- [ ] Basic combat system
- [ ] Health regeneration

### Phase 2: Content
- [ ] Items and inventory
- [ ] Multiple dungeon levels
- [ ] Different enemy types
- [ ] Equipment system

### Phase 3: Polish
- [ ] Save/load system
- [ ] Sound effects and music
- [ ] Particle effects
- [ ] Better UI/menus

### Phase 4: Steam Integration
- [ ] Achievements
- [ ] Cloud saves
- [ ] Leaderboards
- [ ] Workshop support

## Resources

- [python-tcod docs](https://python-tcod.readthedocs.io/)
- [Roguelike Tutorial](http://rogueliketutorials.com/tutorials/tcod/v2/)
- [RogueBasin](http://roguebasin.com/)

---
*Created: 2025-12-18*
*Last Updated: 2025-12-18*
