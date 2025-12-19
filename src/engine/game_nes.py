#!/usr/bin/env python3
"""NES-style roguelike game engine."""
import pygame
import sys
import os
import logging
import traceback
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from environment.world.world_generator import WorldGenerator
from environment.items.treasure import place_treasure_chest
from engine.menu import MenuSystem

# Setup logging
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f'game_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# NES-inspired constants
TILE_SIZE = 16  # 16x16 tiles
MAP_WIDTH = 60
MAP_HEIGHT = 50
SCREEN_WIDTH = TILE_SIZE * 30  # Show 30 tiles wide (480px)
SCREEN_HEIGHT = TILE_SIZE * 25  # Show 25 tiles high (400px)
FPS = 60

# NES color palette (authentic)
NES_COLORS = {
    'black': (12, 12, 12),
    'dark_gray': (80, 80, 80),
    'gray': (124, 124, 124),
    'light_gray': (188, 188, 188),
    'white': (252, 252, 252),
    
    'grass': (0, 168, 0),
    'grass_dark': (0, 135, 81),
    'grass_light': (88, 216, 84),
    
    'tree': (0, 88, 0),
    'tree_trunk': (118, 66, 13),
    
    'rock': (124, 124, 124),
    'rock_dark': (80, 80, 80),
    'rock_light': (188, 188, 188),
    
    'water': (0, 120, 248),
    'water_dark': (0, 88, 248),
    'water_light': (60, 188, 252),
    
    'hero_skin': (252, 160, 68),
    'hero_clothes': (228, 0, 88),
    'hero_hair': (118, 66, 13),
    
    'ui_bg': (24, 24, 24),
    'ui_text': (248, 248, 248),
    'ui_accent': (252, 120, 88),
}


class NESRenderer:
    """Renders tiles in NES style with procedural graphics."""
    
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.tile_cache = {}
        self.animation_frame = 0
        self._create_tiles()
    
    def _create_tiles(self):
        """Create procedural tile graphics in NES style."""
        ts = self.tile_size
        
        # === GRASS TILES ===
        grass = pygame.Surface((ts, ts))
        grass.fill(NES_COLORS['grass'])
        # Add grass texture (random dots)
        for i in range(15):
            x = (i * 7) % ts
            y = (i * 11) % ts
            color = NES_COLORS['grass_dark'] if i % 2 else NES_COLORS['grass_light']
            pygame.draw.rect(grass, color, (x, y, 1, 1))
        self.tile_cache['grass'] = grass
        
        # === TREE TILE ===
        tree = pygame.Surface((ts, ts))
        tree.fill(NES_COLORS['grass'])
        # Tree crown (circle)
        pygame.draw.circle(tree, NES_COLORS['tree'], 
                         (ts//2, ts//2 - 2), ts//3)
        # Dark shadow
        pygame.draw.circle(tree, NES_COLORS['tree_trunk'],
                         (ts//2 - 1, ts//2), ts//4)
        # Trunk
        pygame.draw.rect(tree, NES_COLORS['tree_trunk'],
                        (ts//2 - 2, ts//2 + 2, 4, ts//3))
        self.tile_cache['tree'] = tree
        
        # === ROCK TILE ===
        rock = pygame.Surface((ts, ts))
        rock.fill(NES_COLORS['grass'])
        # Main rock body
        points = [
            (ts//2, ts//3),
            (ts*2//3, ts//2),
            (ts*3//5, ts*3//4),
            (ts*2//5, ts*3//4),
            (ts//3, ts//2)
        ]
        pygame.draw.polygon(rock, NES_COLORS['rock'], points)
        # Highlight
        pygame.draw.line(rock, NES_COLORS['rock_light'],
                        (ts//2, ts//3), (ts*2//3 - 2, ts//2), 2)
        # Shadow
        pygame.draw.line(rock, NES_COLORS['rock_dark'],
                        (ts*2//5 + 1, ts*3//4 - 1), (ts*3//5 - 1, ts*3//4 - 1), 2)
        self.tile_cache['rock'] = rock
        
        # === WATER TILES (animated) ===
        # Frame 1
        water1 = pygame.Surface((ts, ts))
        water1.fill(NES_COLORS['water'])
        pygame.draw.line(water1, NES_COLORS['water_light'],
                        (0, ts//3), (ts, ts//3), 1)
        pygame.draw.line(water1, NES_COLORS['water_dark'],
                        (0, ts*2//3), (ts, ts*2//3), 1)
        self.tile_cache['river_1'] = water1
        
        # Frame 2
        water2 = pygame.Surface((ts, ts))
        water2.fill(NES_COLORS['water'])
        pygame.draw.line(water2, NES_COLORS['water_light'],
                        (0, ts//3 + 1), (ts, ts//3 + 1), 1)
        pygame.draw.line(water2, NES_COLORS['water_dark'],
                        (0, ts*2//3 + 1), (ts, ts*2//3 + 1), 1)
        self.tile_cache['river_2'] = water2
        
        # Frame 3
        water3 = pygame.Surface((ts, ts))
        water3.fill(NES_COLORS['water'])
        pygame.draw.line(water3, NES_COLORS['water_light'],
                        (0, ts//3 + 2), (ts, ts//3 + 2), 1)
        pygame.draw.line(water3, NES_COLORS['water_dark'],
                        (0, ts*2//3 + 2), (ts, ts*2//3 + 2), 1)
        self.tile_cache['river_3'] = water3
        
        # === HERO TILE ===
        hero = pygame.Surface((ts, ts))
        hero.fill(NES_COLORS['grass'])
        hero.set_colorkey(NES_COLORS['grass'])  # Transparent background
        
        # Head
        pygame.draw.circle(hero, NES_COLORS['hero_skin'],
                         (ts//2, ts//3), ts//4)
        # Hair
        pygame.draw.circle(hero, NES_COLORS['hero_hair'],
                         (ts//2, ts//3 - 2), ts//5)
        # Body
        pygame.draw.rect(hero, NES_COLORS['hero_clothes'],
                        (ts//2 - 3, ts//2, 6, ts//3))
        # Eyes
        pygame.draw.circle(hero, NES_COLORS['black'],
                         (ts//2 - 2, ts//3), 1)
        pygame.draw.circle(hero, NES_COLORS['black'],
                         (ts//2 + 2, ts//3), 1)
        self.tile_cache['hero'] = hero
        
        # === TREASURE CHEST ===
        chest = pygame.Surface((ts, ts))
        chest.fill(NES_COLORS['grass'])
        # Chest body
        chest_color = (218, 165, 32)  # Gold
        pygame.draw.rect(chest, chest_color,
                        (ts//4, ts//2, ts//2, ts//2 - 2))
        # Chest lid
        pygame.draw.rect(chest, (180, 140, 20),
                        (ts//4, ts//2 - 3, ts//2, 4))
        # Lock
        pygame.draw.circle(chest, NES_COLORS['black'],
                          (ts//2, ts//2 + 3), 2)
        self.tile_cache['chest'] = chest
        
        # Opened chest
        chest_open = pygame.Surface((ts, ts))
        chest_open.fill(NES_COLORS['grass'])
        pygame.draw.rect(chest_open, chest_color,
                        (ts//4, ts//2, ts//2, ts//2 - 2))
        pygame.draw.rect(chest_open, (180, 140, 20),
                        (ts//4, ts//3, ts//2, 3))
        # Sparkle effect
        pygame.draw.circle(chest_open, NES_COLORS['white'],
                          (ts//2, ts//2 + 2), 3, 1)
        self.tile_cache['chest_open'] = chest_open
    
    def get_tile(self, tile_type):
        """Get tile surface, handling animation."""
        if tile_type == 'river':
            # Animated water
            frame = (self.animation_frame // 10) % 3 + 1
            return self.tile_cache.get(f'river_{frame}', self.tile_cache['grass'])
        return self.tile_cache.get(tile_type, self.tile_cache['grass'])
    
    def update_animation(self):
        """Update animation frame counter."""
        self.animation_frame += 1


class Camera:
    """Camera system for smooth scrolling."""
    
    def __init__(self, width, height, map_width, map_height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height
    
    def update(self, target_x, target_y):
        """Center camera on target position."""
        tiles_x = self.width // TILE_SIZE
        tiles_y = self.height // TILE_SIZE
        
        self.x = target_x - tiles_x // 2
        self.y = target_y - tiles_y // 2
        
        # Clamp to map bounds
        self.x = max(0, min(self.x, self.map_width - tiles_x))
        self.y = max(0, min(self.y, self.map_height - tiles_y))
    
    def apply(self, world_x, world_y):
        """Convert world coordinates to screen coordinates."""
        screen_x = (world_x - self.x) * TILE_SIZE
        screen_y = (world_y - self.y) * TILE_SIZE
        return screen_x, screen_y


class CRTEffect:
    """Apply CRT monitor effects."""
    
    @staticmethod
    def apply_scanlines(surface):
        """Add horizontal scanlines."""
        width, height = surface.get_size()
        scanline = pygame.Surface((width, 1), pygame.SRCALPHA)
        scanline.fill((0, 0, 0, 30))
        
        for y in range(0, height, 2):
            surface.blit(scanline, (0, y))
    
    @staticmethod
    def apply_vignette(surface):
        """Add vignette effect around edges."""
        width, height = surface.get_size()
        vignette = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw darker rectangles from outside in
        for i in range(30):
            alpha = min(i * 2, 100)
            pygame.draw.rect(vignette, (0, 0, 0, alpha),
                           (i, i, width - i*2, height - i*2), 1)
        
        surface.blit(vignette, (0, 0))


class NESGame:
    """Main NES-style game class."""
    
    def __init__(self):
        logger.info("Initializing NES game...")
        try:
            pygame.init()
            pygame.display.set_caption("NES Roguelike Adventure")
            
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.clock = pygame.time.Clock()
            self.running = True
            
            # Create renderer
            logger.debug("Creating NES renderer...")
            self.renderer = NESRenderer(TILE_SIZE)
            
            # Generate world
            logger.debug("Generating world...")
            self.generator = WorldGenerator(width=MAP_WIDTH, height=MAP_HEIGHT)
            self.terrain, self.hero = self.generator.generate()
            logger.info(f"World generated - Hero at ({self.hero.x}, {self.hero.y})")
            
            # Get chests from generator (they're already guaranteed accessible)
            self.treasure_chests = self.generator.chests
            logger.info(f"Generated {len(self.treasure_chests)} treasure chests")
            
            # Camera system
            self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT)
            self.camera.update(self.hero.x, self.hero.y)
            
            # Menu system
            logger.debug("Initializing menu system...")
            self.menu = MenuSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.font = pygame.font.Font(None, 28)
            
            # Settings
            self.crt_effect = True
            self.show_fps = True
            self.message = ""
            self.message_timer = 0
            
            logger.info("Game initialization complete!")
        except Exception as e:
            logger.error(f"Failed to initialize game: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def handle_input(self):
        """Handle keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle menu input first
            if self.menu.is_open():
                self.menu.handle_input(event)
                continue
            
            if event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                
                # Movement (WASD + Arrow keys)
                if event.key in (pygame.K_UP, pygame.K_w, pygame.K_k):
                    dy = -1
                elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_j):
                    dy = 1
                elif event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_h):
                    dx = -1
                elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_l):
                    dx = 1
                
                # Diagonal movement (vi-style)
                elif event.key == pygame.K_y:  # up-left
                    dx, dy = -1, -1
                elif event.key == pygame.K_u:  # up-right
                    dx, dy = 1, -1
                elif event.key == pygame.K_b:  # down-left
                    dx, dy = -1, 1
                elif event.key == pygame.K_n:  # down-right
                    dx, dy = 1, 1
                
                # Special keys
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_TAB:
                    # Open menu (SELECT button)
                    self.menu.open()
                elif event.key == pygame.K_SPACE:
                    # Interact with chest
                    self._try_open_chest()
                elif event.key == pygame.K_r:
                    # Regenerate world
                    self.terrain, self.hero = self.generator.generate()
                    # Get new chests from generator
                    self.treasure_chests = self.generator.chests
                    self.camera.update(self.hero.x, self.hero.y)
                elif event.key == pygame.K_c:
                    # Toggle CRT effect
                    self.crt_effect = not self.crt_effect
                elif event.key == pygame.K_f:
                    # Toggle FPS display
                    self.show_fps = not self.show_fps
                
                # Try to move hero
                if dx != 0 or dy != 0:
                    logger.debug(f"Attempting to move hero by ({dx}, {dy})")
                    new_x = self.hero.x + dx
                    new_y = self.hero.y + dy
                    
                    # Check if chest is at target position
                    chest_blocking = False
                    for chest in self.treasure_chests:
                        if chest['x'] == new_x and chest['y'] == new_y and not chest['opened']:
                            chest_blocking = True
                            break
                    
                    if not chest_blocking and self.generator.is_walkable(new_x, new_y):
                        self.hero.move(dx, dy)
                        self.camera.update(self.hero.x, self.hero.y)
    
    def _try_open_chest(self):
        """Try to open a chest near the hero."""
        logger.debug(f"Attempting to open chest near hero at ({self.hero.x}, {self.hero.y})")
        # Check adjacent tiles
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_x = self.hero.x + dx
                check_y = self.hero.y + dy
                
                for chest in self.treasure_chests:
                    if chest['x'] == check_x and chest['y'] == check_y and not chest['opened']:
                        logger.info(f"Opening chest at ({check_x}, {check_y})")
                        chest['opened'] = True
                        item = chest['item']
                        self.hero.inventory.append(item)
                        # Add to menu inventory system
                        self.menu.add_to_inventory(item)
                        if item:
                            self.message = f"Found: {item.name}!"
                            self.message_timer = 180  # 3 seconds at 60 FPS
                            logger.info(f"Treasure found: {item.name} ({item.slot.value})")
                            print(f"\n{'='*50}")
                            print(f"TREASURE FOUND!")
                            print(f"{'='*50}")
                            print(f"Item: {item.name}")
                            print(f"Slot: {item.slot.value}")
                            print(f"Stats: {item.stats}")
                            print(f"{'='*50}\n")
                        return
    
    def render(self):
        """Render the game world."""
        self.screen.fill(NES_COLORS['black'])
        
        tiles_x = SCREEN_WIDTH // TILE_SIZE
        tiles_y = SCREEN_HEIGHT // TILE_SIZE
        
        # Render visible tiles only
        for ty in range(tiles_y + 2):  # +2 for smooth scrolling
            for tx in range(tiles_x + 2):
                world_x = int(self.camera.x + tx)
                world_y = int(self.camera.y + ty)
                
                if 0 <= world_x < MAP_WIDTH and 0 <= world_y < MAP_HEIGHT:
                    # Get terrain at this position
                    terrain = self.terrain.get((world_x, world_y))
                    if terrain:
                        tile = self.renderer.get_tile(terrain.name)
                        screen_x, screen_y = self.camera.apply(world_x, world_y)
                        self.screen.blit(tile, (screen_x, screen_y))
        
        # Render treasure chests
        for chest in self.treasure_chests:
            chest_x, chest_y = self.camera.apply(chest['x'], chest['y'])
            if -TILE_SIZE < chest_x < SCREEN_WIDTH and -TILE_SIZE < chest_y < SCREEN_HEIGHT:
                chest_tile = self.renderer.get_tile('chest_open' if chest['opened'] else 'chest')
                self.screen.blit(chest_tile, (chest_x, chest_y))
        
        # Render hero
        hero_screen_x, hero_screen_y = self.camera.apply(self.hero.x, self.hero.y)
        hero_tile = self.renderer.get_tile('hero')
        self.screen.blit(hero_tile, (hero_screen_x, hero_screen_y))
        
        # Render UI
        self.render_ui()
        
        # Render menu on top
        if self.menu.is_open():
            self.menu.render(self.screen, self.font)
        
        # Apply CRT effects
        if self.crt_effect:
            CRTEffect.apply_scanlines(self.screen)
            CRTEffect.apply_vignette(self.screen)
        
        pygame.display.flip()
    
    def render_ui(self):
        """Render UI overlay."""
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)
        
        # Status bar background
        ui_height = 32
        ui_bg = pygame.Surface((SCREEN_WIDTH, ui_height))
        ui_bg.fill(NES_COLORS['ui_bg'])
        self.screen.blit(ui_bg, (0, SCREEN_HEIGHT - ui_height))
        
        # HP bar (graphical)
        hp_percent = self.hero.hp / self.hero.max_hp
        bar_width = 80
        bar_height = 8
        bar_x = 10
        bar_y = SCREEN_HEIGHT - 20
        
        # HP bar background
        pygame.draw.rect(self.screen, NES_COLORS['dark_gray'],
                        (bar_x, bar_y, bar_width, bar_height))
        # HP bar fill
        pygame.draw.rect(self.screen, NES_COLORS['ui_accent'],
                        (bar_x, bar_y, int(bar_width * hp_percent), bar_height))
        # HP bar border
        pygame.draw.rect(self.screen, NES_COLORS['white'],
                        (bar_x, bar_y, bar_width, bar_height), 1)
        
        # HP text
        hp_text = small_font.render(
            f"HP {self.hero.hp}/{self.hero.max_hp}",
            True,
            NES_COLORS['ui_text']
        )
        self.screen.blit(hp_text, (bar_x + bar_width + 5, bar_y))
        
        # Position
        pos_text = small_font.render(
            f"X:{self.hero.x} Y:{self.hero.y}",
            True,
            NES_COLORS['ui_text']
        )
        self.screen.blit(pos_text, (200, SCREEN_HEIGHT - 20))
        
        # Controls hint
        help_text = small_font.render(
            "WASD:Move | TAB:Menu | SPACE:Open | R:Regen | ESC:Quit",
            True,
            NES_COLORS['light_gray']
        )
        self.screen.blit(help_text, (10, SCREEN_HEIGHT - ui_height + 3))
        
        # Message display
        if self.message_timer > 0:
            msg_font = pygame.font.Font(None, 32)
            msg_surf = msg_font.render(self.message, True, NES_COLORS['grass_light'])
            msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, 40))
            # Draw background
            bg_rect = msg_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, NES_COLORS['black'], bg_rect)
            pygame.draw.rect(self.screen, NES_COLORS['grass_light'], bg_rect, 2)
            self.screen.blit(msg_surf, msg_rect)
        
        # FPS counter
        if self.show_fps:
            fps = int(self.clock.get_fps())
            fps_text = small_font.render(f"FPS: {fps}", True, NES_COLORS['grass_light'])
            self.screen.blit(fps_text, (SCREEN_WIDTH - 70, 5))
    
    def update(self):
        """Update game state."""
        self.renderer.update_animation()
        
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def run(self):
        """Main game loop."""
        logger.info("Starting main game loop")
        print("=" * 50)
        print("NES-STYLE ROGUELIKE")
        print("=" * 50)
        print("\nControls:")
        print("  Movement: WASD, Arrow Keys, or hjkl (vi-style)")
        print("  Diagonal: yubn keys")
        print("  Menu: TAB (Select button)")
        print("  Open Chest: SPACE (when near chest)")
        print("  Regenerate World: R")
        print("  Toggle CRT Effect: C")
        print("  Toggle FPS: F")
        print("  Quit: ESC")
        print("\nStarting game...")
        print("=" * 50 + "\n")
        
        try:
            while self.running:
                self.handle_input()
                self.update()
                self.render()
                self.clock.tick(FPS)
        except Exception as e:
            logger.error(f"Game loop crashed: {e}")
            logger.error(traceback.format_exc())
            # Write crash report
            crash_file = os.path.join(LOG_DIR, f'crash_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
            with open(crash_file, 'w') as f:
                f.write(f"Game Crash Report\n")
                f.write(f"{'='*50}\n")
                f.write(f"Time: {datetime.now()}\n")
                f.write(f"Error: {e}\n\n")
                f.write(f"Traceback:\n")
                f.write(traceback.format_exc())
            logger.error(f"Crash report written to {crash_file}")
            print(f"\nGame crashed! Error logged to: {crash_file}")
            raise
        finally:
            logger.info("Game loop ended")
            print("\nThanks for playing!")
            pygame.quit()


def main():
    """Entry point."""
    try:
        logger.info("Starting game...")
        game = NESGame()
        game.run()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        logger.critical(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
