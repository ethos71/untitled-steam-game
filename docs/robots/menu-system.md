# Menu System Documentation

## Overview
The game features a comprehensive menu system accessible by pressing the TAB key (simulating the SELECT button on NES controllers).

## Main Menu Structure

### Main Menu
Press **TAB** to open the main menu. Options:
- **Equipment** - Manage hero equipment
- **Options** - Adjust game settings
- **Resume** - Return to game

### Equipment Menu
Manage the hero's equipment across 7 slots:

1. **Head** - Helmets, hats, crowns
2. **Chest** - Armor, shirts, robes
3. **Feet** - Boots, shoes, greaves
4. **Ring 1** - First accessory ring slot
5. **Ring 2** - Second accessory ring slot
6. **Weapon 1** - Primary weapon
7. **Weapon 2** - Secondary weapon or shield

**Controls:**
- UP/DOWN arrows: Navigate slots
- ENTER/SPACE: Select slot to change equipment
- ESC: Return to main menu

### Options Menu
Adjust game settings:

1. **Music Volume** - 0-100% (adjusts in increments of 10)
2. **SFX Volume** - 0-100% (adjusts in increments of 10)
3. **Screen Shake** - ON/OFF toggle
4. **Particles** - ON/OFF toggle
5. **Difficulty** - Easy, Normal, Hard, Nightmare

**Controls:**
- UP/DOWN arrows: Navigate options
- ENTER/SPACE: Adjust selected option
- ESC: Return to main menu

## Menu Navigation
- **UP/DOWN** - Move selection cursor
- **ENTER/SPACE** - Confirm selection
- **ESC** - Go back/close menu
- **TAB** - Open menu (when closed)

## Technical Details

### File Structure
- `src/engine/menu.py` - Main menu system implementation
- `src/characters/hero/equipment.py` - Equipment data structures

### Key Classes
- `MenuSystem` - Manages all menu states and rendering
- `MenuItem` - Individual menu item with action callback
- `EquipSlot` - Enum defining the 7 equipment slots
- `EquipmentManager` - Manages equipped items (in hero module)

### Integration
The menu system is integrated into the main game loop:
1. Game checks if menu is open
2. If open, all input is routed to menu
3. Menu handles navigation and actions
4. Menu renders on top of game screen

## NES-Style Design
The menu follows authentic NES design principles:
- Solid black background with border
- Limited color palette (white, gold highlights)
- Simple text-based layout
- Arrow indicators for selection
- Instant state changes (no fancy transitions)

## Future Enhancements
- Inventory browsing
- Item comparison tooltips
- Status screen with detailed stats
- Save/Load menu
- Key binding configuration
