# Game Assets

This directory contains all game assets for the NES-style roguelike.

## Directory Structure

```
src/
├── assets/
│   ├── tiles/         # Tile graphics (grass, trees, rocks, water)
│   └── sprites/       # Character and entity sprites
└── sound/             # Sound effects and music (in src/sound/)
```

## Asset Specifications

### Tiles
- **Size**: 16x16 pixels
- **Format**: PNG with transparency
- **Color Limit**: 3-4 colors per tile (NES style)
- **Naming**: lowercase_descriptor.png (e.g., grass_01.png)

### Sprites
- **Size**: 16x16 pixels (or 16x32 for tall sprites)
- **Format**: PNG with transparency
- **Animation**: Multiple frames in separate files or sprite sheets
- **Naming**: entity_action_frame.png (e.g., hero_walk_01.png)

### Sounds (Located in src/sound/)
- **Format**: WAV or OGG
- **Sample Rate**: 22050 Hz (retro quality)
- **Channels**: Mono or Stereo
- **Bit Depth**: 16-bit
- **Location**: All sound files go in `src/sound/` directory

## Currently Using

The game currently uses **procedural graphics** generated in code. This allows the game to run without external asset files.

## NES Color Palette

Stick to these authentic NES colors for maximum retro feel:

```
Black:       #0C0C0C  (12, 12, 12)
Dark Gray:   #505050  (80, 80, 80)
Gray:        #7C7C7C  (124, 124, 124)
Light Gray:  #BCBCBC  (188, 188, 188)
White:       #FCFCFC  (252, 252, 252)

Dark Green:  #005800  (0, 88, 0)
Green:       #00A800  (0, 168, 0)
Light Green: #58D854  (88, 216, 84)

Dark Blue:   #0058F8  (0, 88, 248)
Blue:        #0078F8  (0, 120, 248)
Light Blue:  #3CBCFC  (60, 188, 252)

Brown:       #764213  (118, 66, 13)
Orange:      #FCA044  (252, 160, 68)
Red:         #E40058  (228, 0, 88)
```

## Tools

### Recommended Pixel Art Tools
- **Aseprite** ($20) - Professional, best for animation
- **Piskel** (Free) - Browser-based, easy to use
- **GraphicsGale** (Free) - Windows only, classic tool
- **GIMP** (Free) - With pixel art plugin

### Free Asset Resources
- **Kenney.nl** - Free game assets
- **OpenGameArt.org** - Community assets
- **itch.io** - Pixel art packs (some free)
- **Lospec** - Palettes and tools

---
*Created: 2025-12-18*
