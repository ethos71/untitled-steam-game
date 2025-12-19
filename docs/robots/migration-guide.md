# Migration Guide: ASCII to NES-Style Graphics

## Overview
This guide walks through the complete migration from ASCII tcod to NES-style pygame graphics.

---

## Phase 1: Setup ✅ COMPLETE

### What We Did
- [x] Created `src/engine/` directory
- [x] Created `src/assets/` structure (tiles, sprites, sounds)
- [x] Created `game_nes.py` with full NES rendering
- [x] Added pygame to requirements.txt

### Current Status
The NES-style game is **ready to play** with procedural graphics!

---

## Testing the New Engine

### Run the NES Game

```bash
cd src/engine
pip install pygame  # If not already installed
python3 game_nes.py
```

### Controls
- **WASD / Arrow Keys**: Move (8 directions with yubn)
- **R**: Regenerate world
- **C**: Toggle CRT scanline effect
- **F**: Toggle FPS counter
- **ESC**: Quit

### Features to Test
- [x] Smooth camera scrolling
- [x] Animated water tiles
- [x] NES color palette
- [x] CRT scanline effects
- [x] Graphical HP bar
- [x] 60 FPS gameplay

---

## Phase 2: Create Custom Assets (Optional)

The game works with procedural graphics, but you can replace them with custom art.

### Creating Tiles

#### Method 1: Piskel (Browser-based, Free)

1. **Go to**: https://www.piskelapp.com
2. **Create new sprite**: 16x16 pixels
3. **Draw grass tile**:
   - Base color: `#00A800` (green)
   - Add 5-10 darker pixels: `#008751` (dark green)
   - Add 3-5 lighter pixels: `#58D854` (light green)
4. **Export**: File → Export → PNG
5. **Save to**: `src/assets/tiles/grass.png`

#### Method 2: Aseprite (Professional, $20)

1. **New file**: 16x16 pixels, Indexed mode
2. **Import palette**: NES color palette
3. **Draw tile**: Use 3-4 colors max
4. **Export**: File → Export Sprite Sheet
5. **Save**: Individual PNGs or sprite sheet

#### Method 3: Python Script (Automated)

```python
# Create simple tiles with PIL
from PIL import Image, ImageDraw

def create_grass_tile():
    img = Image.new('RGB', (16, 16), (0, 168, 0))
    draw = ImageDraw.Draw(img)
    # Add texture
    for i in range(10):
        x, y = (i * 7) % 16, (i * 11) % 16
        draw.point((x, y), fill=(0, 135, 81))
    img.save('assets/tiles/grass.png')

create_grass_tile()
```

### Tile Checklist

Basic tiles needed:
- [ ] grass.png (base ground)
- [ ] tree.png (obstacle)
- [ ] rock.png (obstacle)
- [ ] water_01.png (animated frame 1)
- [ ] water_02.png (animated frame 2)
- [ ] water_03.png (animated frame 3)
- [ ] hero.png (player character)

Advanced tiles:
- [ ] grass_02.png (variation)
- [ ] grass_03.png (variation)
- [ ] tree_pine.png (variation)
- [ ] rock_large.png (variation)
- [ ] bush.png (decoration)

---

## Phase 3: Update Renderer to Load Assets

### Current: Procedural Graphics
```python
# In NESRenderer._create_tiles()
grass = pygame.Surface((self.tile_size, self.tile_size))
grass.fill(NES_COLORS['grass'])
# Draw procedurally...
```

### Updated: Load from Files
```python
# In NESRenderer._create_tiles()
def load_tile(self, filename, fallback_color):
    """Load tile from file with fallback."""
    try:
        tile = pygame.image.load(f'../assets/tiles/{filename}')
        tile = pygame.transform.scale(tile, (self.tile_size, self.tile_size))
        return tile
    except:
        # Fallback to procedural
        tile = pygame.Surface((self.tile_size, self.tile_size))
        tile.fill(fallback_color)
        return tile

# Usage
self.tile_cache['grass'] = self.load_tile('grass.png', NES_COLORS['grass'])
self.tile_cache['tree'] = self.load_tile('tree.png', NES_COLORS['tree'])
```

---

## Phase 4: Add Advanced Features

### 4.1 Sprite Animation

```python
class AnimatedSprite:
    """Handle sprite animation."""
    
    def __init__(self, frames, fps=8):
        self.frames = frames  # List of pygame Surfaces
        self.fps = fps
        self.current_frame = 0
        self.timer = 0
    
    def update(self, dt):
        self.timer += dt
        if self.timer >= 1.0 / self.fps:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_frame(self):
        return self.frames[self.current_frame]

# Usage
hero_frames = [
    pygame.image.load('assets/sprites/hero_walk_01.png'),
    pygame.image.load('assets/sprites/hero_walk_02.png'),
    pygame.image.load('assets/sprites/hero_walk_03.png'),
]
hero_animation = AnimatedSprite(hero_frames, fps=8)
```

### 4.2 Sound Effects

```python
class SoundManager:
    """Manage game sounds."""
    
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        """Load sound effects."""
        try:
            self.sounds['walk'] = pygame.mixer.Sound('sound/sfx/walk.wav')
            self.sounds['pickup'] = pygame.mixer.Sound('sound/sfx/pickup.wav')
        except:
            print("Sound files not found, continuing without audio")
    
    def play(self, sound_name):
        """Play a sound effect."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

# Usage
sound_manager = SoundManager()
sound_manager.play('walk')
```

### 4.3 Screen Shake Effect

```python
class Camera:
    def __init__(self):
        # ... existing code ...
        self.shake_amount = 0
        self.shake_duration = 0
    
    def shake(self, amount=5, duration=0.2):
        """Add camera shake effect."""
        self.shake_amount = amount
        self.shake_duration = duration
    
    def update(self, target_x, target_y):
        # ... existing camera code ...
        
        # Apply shake
        if self.shake_duration > 0:
            import random
            self.x += random.randint(-self.shake_amount, self.shake_amount)
            self.y += random.randint(-self.shake_amount, self.shake_amount)
            self.shake_duration -= 1/60  # Assuming 60 FPS
```

### 4.4 Particle Effects

```python
class Particle:
    """Simple particle for effects."""
    
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.age = 0
    
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.age += dt
        return self.age < self.lifetime
    
    def render(self, screen, camera):
        if self.age < self.lifetime:
            screen_x, screen_y = camera.apply(int(self.x), int(self.y))
            pygame.draw.circle(screen, self.color, (screen_x, screen_y), 2)

# Usage: Create dust particles when walking
particles = []
for _ in range(5):
    import random
    particle = Particle(
        hero.x, hero.y,
        random.uniform(-1, 1),
        random.uniform(-1, 1),
        NES_COLORS['gray'],
        0.5  # Half second lifetime
    )
    particles.append(particle)
```

---

## Phase 5: Performance Optimization

### 5.1 Dirty Rectangle Rendering

```python
def render(self):
    """Optimized rendering - only redraw changed areas."""
    # Full redraw occasionally
    if self.frame_count % 60 == 0:
        self.screen.fill(NES_COLORS['black'])
        self.dirty_rects = [self.screen.get_rect()]
    
    # Draw only changed tiles
    for rect in self.dirty_rects:
        # Draw tiles in rect...
        pass
    
    pygame.display.update(self.dirty_rects)
    self.dirty_rects = []
```

### 5.2 Sprite Batching

```python
# Group sprites for efficient rendering
terrain_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()

# Add sprites
for terrain in visible_terrain:
    terrain_group.add(terrain)

# Render all at once
terrain_group.draw(screen)
entity_group.draw(screen)
```

### 5.3 Tilemap Caching

```python
# Pre-render entire tilemap to surface
tilemap_surface = pygame.Surface((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
for pos, tile in terrain.items():
    tilemap_surface.blit(tile_image, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))

# In render loop, just blit visible portion
visible_rect = pygame.Rect(camera.x * TILE_SIZE, camera.y * TILE_SIZE, 
                           SCREEN_WIDTH, SCREEN_HEIGHT)
screen.blit(tilemap_surface, (0, 0), visible_rect)
```

---

## Phase 6: Steam Integration

### 6.1 Package for Distribution

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed \
    --add-data "assets:assets" \
    --icon=icon.ico \
    --name "NES_Roguelike" \
    src/engine/game_nes.py
```

### 6.2 Add Steam API

```python
# Install steamworks.py
pip install steamworks

# Initialize Steam
import steamworks
steamworks.STEAMWORKS.initialize()

# Unlock achievement
steamworks.STEAMWORKS.set_achievement("FIRST_KILL")
```

### 6.3 Update Build Scripts

```yaml
# .github/workflows/build-nes-game.yml
name: Build NES Game

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r src/requirements.txt
          pip install pyinstaller
      
      - name: Build executable
        run: |
          pyinstaller build.spec
      
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: game-${{ matrix.os }}
          path: dist/
```

---

## Troubleshooting

### Issue: "No module named pygame"
```bash
cd src/engine
pip install pygame
```

### Issue: "Cannot find assets"
Make sure you're running from `src/engine/` directory:
```bash
cd src/engine
python3 game_nes.py
```

### Issue: Low FPS
- Disable CRT effects (press C)
- Reduce map size in game_nes.py
- Use sprite batching

### Issue: Assets not loading
Check file paths:
```python
import os
print(os.getcwd())  # See current directory
print(os.listdir('../assets/tiles'))  # List tiles
```

---

## Comparison: Before vs After

### Before (ASCII/tcod)
- ✅ Fast prototyping
- ✅ No asset creation needed
- ❌ Limited visual appeal
- ❌ Small audience appeal
- ❌ Hard to add animations

### After (NES-style/pygame)
- ✅ Retro visual appeal
- ✅ Animated tiles
- ✅ Broader audience
- ✅ Easier Steam marketing
- ✅ More control over graphics
- ⚠️ Need to create/find assets (or use procedural)

---

## Next Steps

1. **Test the game**: Run `python3 game_nes.py`
2. **Create assets**: Make 5 basic tiles in Piskel
3. **Add sounds**: Generate 8-bit sound effects
4. **Add enemies**: Create enemy sprites and AI
5. **Add items**: Create collectible items
6. **Polish**: Add particle effects, screen shake
7. **Package**: Build executable with PyInstaller
8. **Deploy**: Upload to Steam

---

## Success Metrics

- [x] Game runs at 60 FPS
- [x] Camera follows player smoothly
- [x] CRT effects look good
- [ ] Custom tiles loaded
- [ ] Sound effects working
- [ ] Builds as standalone executable

---

*Created: 2025-12-18*
*Last Updated: 2025-12-18*
