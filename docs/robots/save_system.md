# Save/Load System

## Overview
The game features a robust save/load system with automatic crash recovery.

## Features

### Manual Save Slots
- **5 Save Slots**: Players can manually save to 5 different slots (save_1 through save_5)
- **Save Metadata**: Each save includes timestamp and game state snapshot
- **Overwrite Protection**: Players can see existing save timestamps before overwriting

### Auto-Save
- **Frequency**: Auto-saves every 60 player moves
- **Exit Save**: Game automatically saves when closing (ESC key or window close)
- **Crash Recovery**: Auto-save file can be loaded if game crashes
- **Silent Operation**: Auto-saves don't interrupt gameplay

## Usage

### Opening the Menu
Press **M** to open the game menu.

### Saving
1. Press **M** to open menu
2. Press **1** to select "Save Game"
3. Press **1-5** to select save slot
4. Game is saved and menu closes

### Loading
1. Press **M** to open menu
2. Press **2** to select "Load Game"
3. View available saves with timestamps
4. Press **1-5** to select save slot to load
5. Game state is restored and menu closes

### Auto-Save Recovery
- On game startup, if an autosave exists, it indicates crash recovery available
- Future enhancement: Prompt player to load autosave or start fresh

## Technical Details

### Save File Location
- Directory: `saves/`
- Manual saves: `saves/save_1.json` through `saves/save_5.json`
- Auto-save: `saves/autosave.json`

### Saved Data
Each save file contains:
- **Hero State**: Position (x, y), HP, Max HP
- **Inventory**: All items in player's inventory with full stats
- **Equipment**: All equipped items in 7 slots
- **World State**: Terrain data, map dimensions
- **Chests**: Chest locations and opened status
- **Metadata**: Save timestamp, world seed (if applicable)

### Save File Format
JSON format with structure:
```json
{
  "timestamp": "2025-12-19T15:59:44.737Z",
  "hero": {
    "x": 25,
    "y": 19,
    "hp": 100,
    "max_hp": 100,
    "inventory": [...],
    "equipment": {...}
  },
  "terrain": {...},
  "chests": [...],
  "map_size": {
    "width": 50,
    "height": 38
  }
}
```

## Implementation Files
- **Save System**: `src/engine/save_system.py`
- **Game Integration**: `src/engine/game_simple.py`
- **Menu UI**: Rendered in `Game._render_menu()`

## Future Enhancements
- Cloud saves (Steam Cloud integration)
- Save file backup/restore
- Save screenshots/thumbnails
- Playtime tracking
- Character portraits in save list
- Quick save/load hotkeys (F5/F9)
- Multiple save profiles
