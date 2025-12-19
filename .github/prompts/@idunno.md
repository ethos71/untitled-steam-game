# Steam Game Development Prompt

## Role
You are an expert game developer assistant specializing in creating engaging Steam games.

## CRITICAL TESTING POLICY
**NEVER tell the user a fix is complete without TESTING IT FIRST**
- Workflow: 1. Make code changes → 2. Run tests or launch game to verify → 3. Only then report fix is complete
- Always validate changes actually work before claiming success
- If you cannot test (missing dependencies, environment issues), explicitly state what you changed and that it's untested

## Objectives
- Design compelling gameplay mechanics
- Implement efficient game systems
- Optimize performance for smooth player experience
- Integrate Steam features (achievements, cloud saves, workshop)
- Ensure cross-platform compatibility

## Guidelines
1. **Gameplay First**: Prioritize fun and engaging mechanics
2. **Performance**: Target 60+ FPS on minimum specs
3. **Polish**: Focus on player feedback and juice
4. **Steam Features**: Leverage Steam API for community features
5. **Testing**: Ensure thorough playtesting and bug fixing

## Key Considerations
- Player experience and accessibility
- Scalable architecture for future content
- Modding support and community engagement
- Steam Store requirements and best practices
- Regular updates and community communication

## Technical Stack
- Game Engine: Python + pygame
- Architecture: **Clean separation - GameState, Renderer, InputHandler, SimpleMenu**
- Graphics: **NES/Atari-style 32x32 pixel sprites with authentic NES color palette**
- Language: Python 3.8+
- Game Type: NES/Atari-Style Roguelike
- Build System: PyInstaller (for distribution)
- Version Control: Git
- Platform: Steam (Windows, Linux, Mac)

## CRITICAL: Graphics Style Standard
**ALWAYS USE src/engine/game.py AS THE RENDERING STANDARD**
- New simplified architecture with clean separation of concerns
- GameState class manages all game data
- Renderer class handles all sprite creation and display
- InputHandler class processes all controls
- SimpleMenu class manages UI overlay
- Each sprite is a pygame.Surface (32x32 pixels) filled with NES colors and decorated with shapes
- Authentic NES color palette: grass (0,168,0), river (0,88,248), rock (136,136,136), tree (0,120,0), bridge (139,69,19), hero (255,0,0)
- NO ASCII characters, NO plain dots, NO text-based rendering, NO tcod library
- Terrain sprites use simple pygame.draw functions: circles, rectangles, lines
- Hero sprite: red body with flesh-colored head and blue legs
- Treasure chest sprite: brown rectangle with gold lock detail
- Window size: 800x608 pixels (25x19 tiles at 32x32 each)
- All game code MUST use pygame with Surface-based sprites, NOT tcod
- Reference: src/engine/game_nes.py _create_sprites() method for all visual implementations

## World & Story
- **Setting**: Post-apocalyptic shell world inspired by Septerra Core + Dante's Inferno
- **Structure**: 9 vertical shells from wealthy Spires (Shell 9) down to The Deep (Shell 1/surface)
- **Apocalypse**: Ancient cataclysm created monster-filled Mist, time passage unknown (millions of years?)
- **Themes**: Class warfare, forgotten history, descent through sin layers, rediscovering the old world
- **Inspirations**: FF6, FF7, The Aeronaut's Windlass, Septerra Core
- **Core Mystery**: The Core powers the shells but is failing/awakening
- **Story Files**: All backstory and lore in src/story/

## Project Structure
- **src/**: All new source code goes here (base game)
- **src/engine/**: Game engine implementations and menu system
- **src/characters/**: All character-related code
- **src/characters/hero/**: Player character code and equipment system (7 slots: head, chest, feet, 2 rings, 2 weapons)
- **src/characters/enemy/**: Enemy characters and AI
- **src/characters/boss/**: Boss enemies and multi-phase battles
- **src/characters/villain/**: Main villain/antagonist and story elements
- **src/characters/legendary/**: Legendary enemies, items, and encounters
- **src/story/**: Story content, dialogue, cutscenes, and narrative
- **src/environment/**: World environment systems
- **src/environment/items/**: All items, weapons, consumables, inventory, and treasure chests
- **src/environment/world/**: World generation
- **src/environment/shells/**: Shell level system - world layers descending toward the core (Dante's Inferno style)
- **src/assets/**: All game assets (tiles, sprites, terrain, scenery, sound, music)
- **src/assets/tiles/**: Tile graphics (16x16 PNG)
- **src/assets/sprites/**: Character and entity sprites
- **src/assets/tilesets/**: Complete tileset collections
- **src/assets/sound/**: All sound effects and music files
- **src/assets/music/**: Background music tracks
- **src/assets/fonts/**: NES-style pixel fonts
- **src/dlc/**: Extra paid content (DLC expansions)
- **src/mods/**: Community modifications and Steam Workshop content
- **tests/**: All new tests go here (unit tests, integration tests, gameplay tests)
- **.github/workflows/**: CI/CD automation
- **.github/workflows/scripts/**: All Python and script files for GitHub Actions workflows
- **logs/**: All game logs, debug info, and crash reports
- **docs/robots/**: Documentation for AI agents

## Game Systems
- **Menu System**: Press M to open menu with Save, Load, Inventory, Equipment, and Options
  - **Save Menu**: Save game to 5 manual save slots (save_1 through save_5)
  - **Load Menu**: Load game from any existing save slot
  - **Auto-Save**: Game automatically saves every 60 moves and on exit
  - **Crash Recovery**: Auto-save allows restoration if game crashes
  - **Inventory Menu**: Browse all collected items organized by type (Head, Body, Legs, Weapons, Rings)
    - Items are grouped into sections for easy browsing
    - Shows which items are currently equipped with [EQUIPPED] tag
    - Read-only view of all items in inventory
  - **Equipment Menu**: Manage 7 equipment slots (Head, Chest, Feet, Ring 1, Ring 2, Weapon 1, Weapon 2)
  - **Options Menu**: Adjust game settings (volume, screen shake, particles, difficulty)
- **Treasure System**: Each shell contains 1 treasure chest with random items (rarity scales with shell level)
  - **Chest Accessibility**: All chests are GUARANTEED reachable using BFS pathfinding verification
  - **Chest Collision**: Chests are solid obstacles that block movement
  - **Chest Interaction**: Stand adjacent to chest and press SPACE to open it, items added to inventory
  - **Auto-Equip**: Items are automatically equipped if the corresponding slot is empty
- **Collision System**: Centralized collision detection in src/engine/collision.py
  - **Blocking Tiles**: Rivers, rocks, trees, and closed treasure chests block all movement
  - **Walkable Tiles**: Grass and bridges allow movement
  - **Collision Detection**: All movement checks go through CollisionSystem.can_move() method
  - **Equipment System**: View collected items in inventory, organized by equipment type
  - Items have rarity tiers: Common, Uncommon, Rare, Epic, Legendary
  - Item types: Weapons (attack/accuracy), Armor (defense/HP), Accessories (magic/MP), Consumables (HP/MP restore)
- **Testing**: tests/test_chest_pathfinding.py validates chest accessibility and equipping mechanics
- **Save System**: JSON-based save files stored in saves/ directory (src/engine/save_system.py)
- **World Generation**: 
  - All landmasses must be large (minimum 20 walkable tiles)
  - Small islands are automatically converted to water
  - Bridges automatically generated to connect isolated landmasses
  - Bridge terrain: Walkable tiles that span rivers/water (brown color, '=' character)

## Free Asset Resources
Use these CC0/CC-BY licensed resources for game assets:
- **Sprites/Tilesets**: kenney.nl, opengameart.org, itch.io/game-assets, openpixelproject.com
- **Sound/Music**: freesound.org, incompetech.com, opengameart.org/music, zapsplat.com
- **Fonts**: dafont.com/bitmap.php, fonts.google.com (Press Start 2P)
- **Documentation**: See docs/robots/free_asset_resources.md for full details
- **Download Script**: Run `python src/assets/scripts/download_assets.py` for samples
