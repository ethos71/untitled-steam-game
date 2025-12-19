# Steam Game Development Prompt

## Role
You are an expert game developer assistant specializing in creating engaging Steam games.

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
- Graphics: **NES/Atari-style PIXEL ART (16x16 tiles, authentic NES palette) - NO ASCII**
- Language: Python 3.8+
- Game Type: NES/Atari-Style Roguelike
- Build System: PyInstaller (for distribution)
- Version Control: Git
- Platform: Steam (Windows, Linux, Mac)

## IMPORTANT: Graphics Style
**THIS IS NOT AN ASCII GAME**
- Use 16x16 pixel tiles for all terrain and objects
- Use NES authentic color palette
- Render using pygame sprite/surface system
- Create or download pixel art assets (NOT text characters)
- Reference: docs/robots/nes-atari-style-game.md

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
- **src/engine/**: Game engine implementations
- **src/characters/**: All character-related code
- **src/characters/hero/**: Player character code and equipment system
- **src/characters/enemy/**: Enemy characters and AI
- **src/characters/boss/**: Boss enemies and multi-phase battles
- **src/characters/villain/**: Main villain/antagonist and story elements
- **src/characters/legendary/**: Legendary enemies, items, and encounters
- **src/story/**: Story content, dialogue, cutscenes, and narrative
- **src/environment/**: World environment systems
- **src/environment/items/**: All items, weapons, consumables, and inventory
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
- **.github/workflows/**: CI/CD automation
- **docs/robots/**: Documentation for AI agents

## Free Asset Resources
Use these CC0/CC-BY licensed resources for game assets:
- **Sprites/Tilesets**: kenney.nl, opengameart.org, itch.io/game-assets, openpixelproject.com
- **Sound/Music**: freesound.org, incompetech.com, opengameart.org/music, zapsplat.com
- **Fonts**: dafont.com/bitmap.php, fonts.google.com (Press Start 2P)
- **Documentation**: See docs/robots/free_asset_resources.md for full details
- **Download Script**: Run `python src/assets/scripts/download_assets.py` for samples
