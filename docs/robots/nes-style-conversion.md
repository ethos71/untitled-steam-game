# Converting ASCII to NES/Atari Style Graphics

## Overview
Transform your ASCII roguelike into a retro NES/Atari-style game with tile-based graphics while keeping the same game logic.

---

## Option 1: pygame (Best for NES/Atari Feel)

### Why pygame?
- **Perfect for retro graphics**: Designed for 2D pixel art
- **Simple tile rendering**: Easy sprite/tile system
- **Pixel-perfect control**: Direct pixel manipulation
- **NES color palette support**: Can match exact NES colors
- **Cross-platform**: Works on Steam
- **Active community**: Tons of tutorials

### Implementation
```python
import pygame

# NES resolution: 256x240
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240
TILE_SIZE = 8  # 8x8 pixel tiles (NES standard)

# NES color palette (authentic colors)
NES_COLORS = {
    'black': (0, 0, 0),
    'dark_blue': (0, 30, 116),
    'dark_green': (0, 135, 81),
    'brown': (118, 66, 13),
    'gray': (181, 181, 181),
    'green': (0, 177, 64),
    'blue': (0, 136, 255),
    'white': (255, 255, 255),
}
```

---

## Option 2: Godot Engine (Most Professional)

### Why Godot?
- **Built-in pixel art mode**: Dedicated 2D pixel rendering
- **Tilemap system**: Native tilemap support
- **Shader support**: CRT filters, scanlines, color palettes
- **Animation tools**: Easy sprite animation
- **Steam integration**: Official Steam plugin
- **Visual editor**: Design levels visually

### Features
- Pixel-perfect rendering
- Layer system for parallax
- Particle effects (NES-style)
- Built-in physics
- Save system

---

## Option 3: LÖVE (Love2D) - Lightweight

### Why LÖVE?
- **Lua scripting**: Easy to learn
- **Perfect for 2D**: Designed for 2D games
- **Pixel scaling**: Built-in nearest-neighbor filtering
- **Small footprint**: Tiny executable size
- **Fast prototyping**: Quick iteration

---

## Option 4: PyGame Zero (Easiest Migration)

### Why PyGame Zero?
- **Keep Python code**: Minimal changes needed
- **Simple API**: Even easier than pygame
- **Automatic asset loading**: Just drop images in folder
- **Quick conversion**: Convert existing game fast

---

## Recommended Approach: pygame Migration

### Step-by-Step Conversion

#### 1. Create Tile Sprites (8x8 or 16x16)
```
tiles/
├── grass_01.png
├── grass_02.png
├── tree_01.png
├── tree_02.png
├── rock_01.png
├── water_01.png
└── hero.png
```

#### 2. Sprite Creation Tools
- **Aseprite** (Best, $20): Professional pixel art
- **Piskel** (Free): Browser-based pixel editor
- **GraphicsGale** (Free): Classic pixel art tool
- **GIMP** (Free): With pixel art plugin

#### 3. NES Color Palette
Use authentic NES 54-color palette:
```python
NES_PALETTE = [
    (124, 124, 124), (0, 0, 252), (0, 0, 188), (68, 40, 188),
    (148, 0, 132), (168, 0, 32), (168, 16, 0), (136, 20, 0),
    (80, 48, 0), (0, 120, 0), (0, 104, 0), (0, 88, 0),
    (0, 64, 88), (0, 0, 0), (0, 0, 0), (0, 0, 0),
    (188, 188, 188), (0, 120, 248), (0, 88, 248), (104, 68, 252),
    (216, 0, 204), (228, 0, 88), (248, 56, 0), (228, 92, 16),
    (172, 124, 0), (0, 184, 0), (0, 168, 0), (0, 168, 68),
    (0, 136, 136), (0, 0, 0), (0, 0, 0), (0, 0, 0),
    (248, 248, 248), (60, 188, 252), (104, 136, 252), (152, 120, 248),
    (248, 120, 248), (248, 88, 152), (248, 120, 88), (252, 160, 68),
    (248, 184, 0), (184, 248, 24), (88, 216, 84), (88, 248, 152),
    (0, 232, 216), (120, 120, 120), (0, 0, 0), (0, 0, 0),
    (252, 252, 252), (164, 228, 252), (184, 184, 248), (216, 184, 248),
    (248, 184, 248), (248, 164, 192), (240, 208, 176), (252, 224, 168),
    (248, 216, 120), (216, 248, 120), (184, 248, 184), (184, 248, 216),
    (0, 252, 252), (216, 216, 216), (0, 0, 0), (0, 0, 0),
]
```

#### 4. NES Resolution Options
- **256x240**: Original NES (4:3 aspect)
- **320x240**: Wider view
- **512x480**: 2x scale
- **768x720**: 3x scale (best for modern displays)

#### 5. NES-Style Features to Add
- **Sprite flickering**: Authentic NES limitation effect
- **4 colors per sprite**: NES color limit
- **Scrolling**: Smooth screen scrolling
- **Scanlines**: CRT effect overlay
- **Tile animation**: Animate water, grass
- **8-direction sprites**: Character facing directions

---

## Detailed pygame Implementation

### Basic Structure
```python
import pygame
import sys

# Constants
SCREEN_WIDTH = 768  # 3x NES resolution
SCREEN_HEIGHT = 720
TILE_SIZE = 24  # 3x scale of 8x8
FPS = 60

class NESGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load tiles
        self.tiles = self.load_tiles()
        
    def load_tiles(self):
        """Load all tile sprites."""
        tiles = {}
        tiles['grass'] = pygame.image.load('tiles/grass.png')
        tiles['tree'] = pygame.image.load('tiles/tree.png')
        tiles['rock'] = pygame.image.load('tiles/rock.png')
        tiles['water'] = pygame.image.load('tiles/water.png')
        tiles['hero'] = pygame.image.load('tiles/hero.png')
        
        # Scale up for crisp pixels
        for key in tiles:
            tiles[key] = pygame.transform.scale(
                tiles[key], 
                (TILE_SIZE, TILE_SIZE)
            )
        return tiles
    
    def render(self):
        """Render the game world."""
        self.screen.fill((0, 0, 0))
        
        # Render tiles
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.get_tile(x, y)
                tile_sprite = self.tiles.get(tile_type)
                if tile_sprite:
                    self.screen.blit(
                        tile_sprite,
                        (x * TILE_SIZE, y * TILE_SIZE)
                    )
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)
            
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
```

---

## CRT/Scanline Effects

### Add Retro Feel
```python
def apply_crt_effect(surface):
    """Apply CRT scanline effect."""
    width, height = surface.get_size()
    
    # Create scanlines
    for y in range(0, height, 2):
        pygame.draw.line(
            surface,
            (0, 0, 0, 50),  # Semi-transparent black
            (0, y),
            (width, y),
            1
        )
    
    # Slight screen curve (optional)
    # Add vignette effect
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(
        overlay,
        (0, 0, 0, 30),
        (0, 0, width, height),
        20  # Border width
    )
    surface.blit(overlay, (0, 0))
```

---

## Sprite Sheet System

### Efficient Texture Management
```python
class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename)
    
    def get_sprite(self, x, y, width, height):
        """Extract sprite from sheet."""
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))  # Transparent
        return sprite
    
    def get_tile(self, row, col, tile_size=8):
        """Get tile by grid position."""
        return self.get_sprite(
            col * tile_size,
            row * tile_size,
            tile_size,
            tile_size
        )
```

---

## Animation System

### NES-Style Animation
```python
class AnimatedSprite:
    def __init__(self, frames, fps=10):
        self.frames = frames
        self.current_frame = 0
        self.fps = fps
        self.timer = 0
    
    def update(self, dt):
        """Update animation."""
        self.timer += dt
        if self.timer >= 1.0 / self.fps:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_current_frame(self):
        return self.frames[self.current_frame]

# Usage
hero_walk = AnimatedSprite([
    hero_frame_1,
    hero_frame_2,
    hero_frame_3,
    hero_frame_2,
], fps=8)
```

---

## Sound/Music (NES-Style)

### Libraries
- **pygame.mixer**: Built-in audio
- **pyaudio**: More control
- **pysound**: Retro sound generation

### 8-bit Sound Generation
```python
import pygame.mixer
import numpy as np

def generate_square_wave(frequency, duration):
    """Generate NES-style square wave."""
    sample_rate = 22050
    samples = int(sample_rate * duration)
    wave = np.zeros(samples)
    
    for i in range(samples):
        wave[i] = 1 if (i // (sample_rate // frequency // 2)) % 2 == 0 else -1
    
    # Convert to 16-bit
    wave = (wave * 32767).astype(np.int16)
    sound = pygame.sndarray.make_sound(wave)
    return sound
```

---

## Asset Creation Guide

### Tile Design Principles
1. **Size**: 8x8 or 16x16 pixels
2. **Colors**: 3-4 colors per tile (NES limit)
3. **Contrast**: High contrast for visibility
4. **Consistency**: Match style across all tiles
5. **Readability**: Clear at small size

### Character Design
1. **Simple shapes**: Easy to read
2. **Distinctive silhouette**: Recognizable
3. **Limited animation**: 2-4 frames
4. **Color coded**: Different colors for states

### Creating Your First Tile
```
1. Open Aseprite/Piskel
2. Create 8x8 canvas
3. Choose 3-4 colors from NES palette
4. Draw simple grass pattern
5. Export as PNG
6. Create variants (grass_01, grass_02)
```

---

## Migration Plan

### Phase 1: Setup pygame
```bash
cd src
pip install pygame
```

### Phase 2: Create Basic Tiles
- Grass (2-3 variants)
- Tree (1-2 types)
- Rock (1-2 types)
- Water (animated, 2-4 frames)
- Hero (4-8 directions)

### Phase 3: Convert World Generator
- Keep same generation logic
- Map ASCII chars to tile types
- Use tile IDs instead of characters

### Phase 4: Implement Renderer
- Create pygame window
- Tile rendering system
- Camera/scrolling
- UI overlay

### Phase 5: Add NES Features
- CRT scanlines
- Color palette shader
- 8-bit sound effects
- Screen transitions

---

## Performance Optimization

### NES-Era Techniques
```python
# Dirty rectangle rendering (only redraw changed areas)
dirty_rects = []
for entity in changed_entities:
    dirty_rects.append(entity.rect)
pygame.display.update(dirty_rects)

# Sprite batching
sprite_group = pygame.sprite.Group()
sprite_group.draw(screen)

# Tilemap caching
tilemap_surface = pygame.Surface((map_width, map_height))
# Draw once, blit many times
```

---

## Recommended Next Steps

### Immediate (Keep It Simple)
1. Install pygame
2. Create 5 basic tiles (8x8 or 16x16)
3. Convert world_generator to use tile IDs
4. Create basic pygame renderer
5. Test with simple graphics

### Short Term (Add Polish)
1. Create animated tiles (water)
2. Add hero walking animation
3. Implement camera system
4. Add CRT scanlines
5. Create 8-bit sound effects

### Long Term (Full NES Experience)
1. Complete tile set (50+ tiles)
2. Multiple enemy types
3. UI graphics (hearts, items)
4. Chiptune music
5. Screen transitions
6. Particle effects

---

## Example Asset Packs (Free)

- **Kenney.nl**: Free game assets
- **OpenGameArt.org**: Community assets
- **itch.io**: Pixel art packs
- **Lospec**: Palette resources

---

## Tools Summary

| Tool | Purpose | Cost | Best For |
|------|---------|------|----------|
| Aseprite | Pixel art | $20 | Professional |
| Piskel | Pixel art | Free | Beginners |
| pygame | Engine | Free | Full control |
| Godot | Engine | Free | Advanced features |
| LÖVE | Engine | Free | Lua developers |

---

*Created: 2025-12-18*
