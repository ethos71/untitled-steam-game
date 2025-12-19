# Game Architecture

## Overview
The game uses a clean, modular architecture with clear separation of concerns to prevent bugs and make maintenance easier.

## Core Systems

### GameState (`src/engine/game_state.py`)
**Purpose**: Central data management
- Manages all game data (world, hero, inventory, chests)
- Provides clean APIs for state queries and modifications
- Handles collision detection and movement validation
- Manages inventory and auto-equip logic
- **No rendering or input logic**

### Renderer (`src/engine/renderer.py`)
**Purpose**: All visual display
- Creates and stores all sprite surfaces
- Renders world tiles based on camera position
- Draws chests and hero
- **Only responsible for drawing - no game logic**

### InputHandler (`src/engine/input_handler.py`)
**Purpose**: User input processing
- Processes keyboard events
- Routes input to appropriate handlers (game vs menu)
- Coordinates between player input and game state changes
- **No direct rendering**

### SimpleMenu (`src/engine/simple_menu.py`)
**Purpose**: UI overlay system
- Displays menu with inventory and options
- Shows equipped items by slot
- **Reads from GameState, doesn't modify it directly**

### Game (`src/engine/game.py`)
**Purpose**: Main coordinator
- Initializes all systems
- Runs the game loop
- Coordinates between systems
- **Keeps systems decoupled**

## Benefits of This Architecture

### 1. Easier to Debug
- Each system has ONE clear responsibility
- Bugs are isolated to specific modules
- Logs clearly show which system has issues

### 2. Prevents Crashes
- No circular dependencies
- State changes go through controlled APIs
- Rendering can't accidentally modify game state

### 3. Easier to Test
- Each system can be tested independently
- Mock objects are simple to create
- Game logic separate from display logic

### 4. Easier to Extend
- Want new item type? Modify GameState only
- Want new sprite? Modify Renderer only
- Want new control? Modify InputHandler only

## Data Flow

```
User Input → InputHandler → GameState → Renderer → Screen
                ↓
            SimpleMenu (displays state)
```

## Adding New Features

### New Item Type
1. Update `GameState.inventory` structure
2. Update `GameState.add_item()` logic
3. Update `SimpleMenu.render()` to display it
4. No changes needed to Renderer or InputHandler

### New Sprite
1. Add sprite creation in `Renderer._create_sprites()`
2. Update terrain generation to use it
3. No changes to GameState, Input, or Menu

### New Control
1. Add key handling in `InputHandler.handle_keydown()`
2. Call appropriate GameState method
3. No changes to Renderer or Menu

## Best Practices

1. **GameState owns all data** - other systems read from it
2. **Renderer only draws** - never modifies game state
3. **InputHandler routes commands** - doesn't implement game logic
4. **Systems communicate through clear APIs** - no direct access to internal state
5. **Logging at system boundaries** - makes debugging easy

## Migration from Old Code

Old monolithic `game_nes.py` has been replaced with:
- `game.py` - coordinator
- `game_state.py` - data management
- `renderer.py` - display
- `input_handler.py` - controls
- `simple_menu.py` - UI

This makes the codebase **simpler, safer, and more maintainable**.
