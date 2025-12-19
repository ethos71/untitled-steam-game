# Python Roguelike Setup Guide

## Project Structure

```
src/
├── hero/
│   └── hero.py           # Hero character class
├── enemy/
│   └── enemy.py          # Enemy types and AI
├── boss/
│   └── boss.py           # Boss enemies with phases
├── villain/
│   └── villain.py        # Main villain and story
├── legendary/
│   └── legendary.py      # Legendary encounters
├── story/
│   ├── story.py          # Story progression
│   ├── dialogue.py       # Dialogue system
│   └── cutscenes.py      # Cutscenes
├── scenery/
│   └── terrain.py        # Terrain elements (trees, rocks, rivers)
├── world/
│   └── world_generator.py # World generation script
├── assets/
│   ├── tiles/            # Tile graphics
│   └── sprites/          # Character sprites
├── sound/                # Sound effects and music
├── steam/
│   └── steam_config.json # Steam configuration
└── requirements.txt      # Python dependencies
```

## Installation

### 1. Create Virtual Environment (Recommended)
```bash
cd src
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the World Generator

### Test World Generation
```bash
cd src/world
python world_generator.py
```

This will generate and display a random ASCII world with:
- Hero (@) at the center
- Trees (♣, ♠, T, ↑)
- Rocks (○, ●, *, ◘)
- Rivers (~, ≈, ∼)
- Grass (., ,, ", ')

## Game Components

### Hero (`src/hero/hero.py`)
- Character: `@`
- Position: Center of the map
- Stats: HP, max_hp
- Methods: move, get_position, render_char

### Terrain Types (`src/scenery/terrain.py`)

#### Tree
- Characters: ♣, ♠, T, ↑
- Color: Forest green
- Blocks: Movement and sight
- Spawns: In forest patches

#### Rock
- Characters: ○, ●, *, ◘
- Color: Gray
- Blocks: Movement only
- Spawns: Scattered randomly

#### River
- Characters: ~, ≈, ∼
- Color: Blue
- Blocks: Movement only
- Spawns: 1-3 winding rivers

#### Grass
- Characters: ., ,, ", '
- Color: Lime green
- Blocks: Nothing (walkable)
- Spawns: Everywhere as base layer

### World Generator (`src/world/world_generator.py`)
Generates procedural worlds with:
- Default size: 80x40 tiles
- Layered generation (grass → rivers → trees → rocks)
- Hero spawns at center on walkable terrain
- Terrain collision detection

## Next Steps

### 1. Add TCOD Integration
Create a proper game window with tcod:
```python
import tcod

# Initialize console
console = tcod.Console(width=80, height=50)
context = tcod.context.new(columns=80, rows=50, title="ASCII Roguelike")
```

### 2. Add Player Input
```python
# Handle keyboard events
for event in tcod.event.wait():
    if event.type == "KEYDOWN":
        if event.sym == tcod.event.K_UP:
            hero.move(0, -1)
```

### 3. Add Game Loop
- Render world each frame
- Handle input
- Update game state
- Collision detection

### 4. Add Features
- Field of view (FOV) system
- Monster AI
- Combat system
- Inventory
- Procedural dungeons

## Development Tips

### Testing World Generation
Run the generator multiple times to see different layouts:
```bash
for i in {1..5}; do python world_generator.py; done
```

### Adjusting World Size
Modify in `world_generator.py`:
```python
generator = WorldGenerator(width=120, height=60)
```

### Adjusting Density
Change terrain density parameters:
```python
self._generate_trees(density=0.20)  # More trees
self._generate_rocks(density=0.10)  # More rocks
```

## Resources

- [python-tcod documentation](https://python-tcod.readthedocs.io/)
- [Roguelike Tutorial](http://rogueliketutorials.com/tutorials/tcod/v2/)
- [RogueBasin](http://roguebasin.com/)

---
*Created: 2025-12-18*
