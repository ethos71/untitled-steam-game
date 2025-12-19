# Free Asset Resources for Game Development

This document lists free resources for game assets that can be used in our NES-style roguelike.

## Sprite & Tileset Resources

### Kenney.nl
- **URL**: https://kenney.nl/assets
- **License**: CC0 (Public Domain)
- **Content**: Huge collection of game assets including:
  - Roguelike characters and tilesets
  - UI elements
  - Platformer assets
  - 3D models
- **Why It's Great**: Professional quality, completely free, no attribution required

### OpenGameArt.org
- **URL**: https://opengameart.org
- **License**: Various CC licenses (check individual assets)
- **Content**: Community-contributed game art
  - 2D sprites and tilesets
  - Pixel art
  - Character sprites
  - Background art
- **Why It's Great**: Massive variety, active community

### itch.io Game Assets
- **URL**: https://itch.io/game-assets/free
- **License**: Various (check individual packs)
- **Content**: Free and paid asset packs
  - Pixel art packs
  - Character sprites
  - Tilesets
  - Effects
- **Why It's Great**: Modern indie game assets, frequent new additions

### Open Pixel Project
- **URL**: http://openpixelproject.com
- **License**: CC0
- **Content**: Collaborative pixel art project
  - Character sprites
  - Enemies
  - Items
- **Why It's Great**: Consistent pixel art style

## Sound & Music Resources

### Freesound.org
- **URL**: https://freesound.org
- **License**: Various CC licenses
- **Content**: Sound effects library
  - Ambient sounds
  - UI sounds
  - Combat effects
  - Environmental audio
- **Why It's Great**: Largest free sound library, searchable, high quality

### Incompetech (Kevin MacLeod)
- **URL**: https://incompetech.com/music/royalty-free
- **License**: CC BY (requires attribution)
- **Content**: Royalty-free music
  - Background music
  - Ambient tracks
  - Combat music
- **Why It's Great**: Professional quality, widely used in indie games

### OpenGameArt Music
- **URL**: https://opengameart.org/art-search-advanced?keys=&field_art_type_tid%5B%5D=12
- **License**: Various CC licenses
- **Content**: Game music tracks
  - Chiptune/8-bit music
  - Orchestral
  - Ambient
- **Why It's Great**: Game-specific music, multiple styles

### Zapsplat
- **URL**: https://www.zapsplat.com
- **License**: Free with attribution
- **Content**: Sound effects
  - UI sounds
  - Nature sounds
  - Combat effects
- **Why It's Great**: High quality, easy to download

## Font Resources

### DaFont - Pixel Fonts
- **URL**: https://www.dafont.com/bitmap.php
- **License**: Check individual fonts
- **Content**: Pixel/bitmap fonts perfect for retro games

### Google Fonts - Press Start 2P
- **URL**: https://fonts.google.com/specimen/Press+Start+2P
- **License**: SIL Open Font License
- **Content**: Classic NES-style font

## Integration Notes

All assets downloaded should be placed in appropriate folders:
- **Sprites**: `src/assets/sprites/`
- **Tilesets**: `src/assets/tilesets/`
- **Sound**: `src/assets/sound/`
- **Music**: `src/assets/music/`
- **Fonts**: `src/assets/fonts/`

## Attribution Requirements

Remember to:
1. Check the license for each asset
2. Maintain attribution where required (usually CC-BY)
3. Keep a credits file listing all used assets
4. Include licenses in your game's credits

## Download Script

Run `python src/assets/scripts/download_assets.py` to automatically download sample free assets.
