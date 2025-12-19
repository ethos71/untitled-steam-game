# Mods System

This folder contains community-created modifications and extensions for the game.

## Purpose
- Enable community contributions
- Support custom content creation
- Allow gameplay modifications
- Integrate with Steam Workshop

## Mod Structure

### Types of Mods
- **Content Mods**: New items, enemies, levels
- **Gameplay Mods**: Modified mechanics, balance changes
- **Visual Mods**: Custom sprites, tiles, animations
- **Audio Mods**: New music and sound effects
- **Total Conversions**: Complete game overhauls

### Mod Format
Each mod should be in its own directory with the following structure:
```
src/mods/
├── example_mod/
│   ├── mod.json         # Mod metadata and configuration
│   ├── assets/          # Custom graphics, sounds
│   ├── scripts/         # Python scripts for mod logic
│   └── README.md        # Mod documentation
```

## Mod Configuration (mod.json)
```json
{
  "name": "Example Mod",
  "version": "1.0.0",
  "author": "ModAuthor",
  "description": "Description of what the mod does",
  "dependencies": [],
  "load_order": 100,
  "compatibility": "1.0.0",
  "enabled": true,
  "files": {
    "scripts": ["scripts/main.py"],
    "assets": ["assets/"]
  }
}
```

## Mod API
Mods can hook into:
- **Game Events**: `on_game_start`, `on_level_load`, `on_player_action`
- **Entity System**: Add new enemies, items, NPCs
- **World Generation**: Modify terrain, structures
- **UI/HUD**: Custom overlays and interfaces
- **Combat System**: New abilities, damage types

## Steam Workshop Integration
- Automatic mod discovery
- One-click install/uninstall
- Version management
- Community ratings and feedback
- Automatic updates

## Mod Loading System
1. Scan `src/mods/` directory for mod folders
2. Read `mod.json` configuration files
3. Validate dependencies and compatibility
4. Load mods in specified order
5. Initialize mod hooks and callbacks
6. Merge mod assets with base game

## Guidelines for Mod Creators
- Follow Python coding standards (PEP 8)
- Include clear documentation
- Test thoroughly before publishing
- Respect base game balance
- Credit original assets
- Use version control (Git)

## Security
- Mods run in sandboxed environment
- File system access restricted to mod directory
- No network access without permission
- Code review for Workshop featured mods

## Example Mods
- **Hard Mode**: Increased difficulty, tougher enemies
- **New Biomes**: Additional terrain types and generation
- **Quality of Life**: UI improvements, hotkeys
- **Cosmetic Pack**: Character skins, visual effects
