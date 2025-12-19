#!/usr/bin/env python3
"""
NES Roguelike - Main Game Engine
Retro NES/Atari style roguelike with 32x32 pixel sprites
"""
import pygame
import sys
import os
import logging
from datetime import datetime

# Setup logging
log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'game_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from environment.world.world_generator import WorldGenerator
from characters.hero.hero import Hero
from characters.hero.equipment import EquipmentManager
from environment.items.treasure import TreasureChest
from engine.menu import MenuSystem
from engine.save_system import SaveSystem
from engine.collision import CollisionSystem

# Game constants
SPRITE_SIZE = 32  # 32x32 pixel sprites for NES style
GRID_WIDTH = 25
GRID_HEIGHT = 19
WINDOW_WIDTH = GRID_WIDTH * SPRITE_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * SPRITE_SIZE
FPS = 60

# NES Color Palette
NES_COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'grass': (0, 168, 0),      # Bright green
    'river': (0, 88, 248),     # Bright blue
    'rock': (136, 136, 136),   # Gray
    'tree': (0, 120, 0),       # Dark green
    'bridge': (139, 69, 19),   # Brown
    'chest': (252, 216, 168),  # Light brown/tan
    'hero': (255, 0, 0),       # Red
    'ui_bg': (36, 36, 36),     # Dark gray for UI
    'ui_text': (248, 248, 248) # Off-white for text
}

class Game:
    def __init__(self):
        logger.info("Initializing NES Roguelike")
        pygame.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("NES Roguelike")
        self.clock = pygame.time.Clock()
        
        self.world_generator = WorldGenerator(GRID_WIDTH, GRID_HEIGHT)
        self.world = None
        self.hero = None
        self.treasure = None
        self.equipment = EquipmentManager()
        self.collision = CollisionSystem(self.world_generator)
        
        self.camera_x = 0
        self.camera_y = 0
        
        # Create font for menu
        self.font = pygame.font.Font(None, 36)
        
        self.menu = MenuSystem(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.save_system = SaveSystem()
        
        self.auto_save_counter = 0
        self.auto_save_interval = 300  # Auto-save every 5 seconds (300 frames at 60 FPS)
        
        # Message system
        self.message = ""
        self.message_timer = 0
        self.message_duration = 180  # 3 seconds at 60 FPS
        
        # Create sprite surfaces
        self.sprites = self._create_sprites()
        
        self.new_game()
        logger.info("Game initialized successfully")
    
    def _create_sprites(self):
        """Create 32x32 NES-style pixel art sprite surfaces"""
        sprites = {}
        
        # Grass sprite - detailed pixel art
        grass = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        grass_pixels = [
            [0, 168, 0], [0, 180, 0], [0, 168, 0], [0, 180, 0]
        ]
        for y in range(SPRITE_SIZE):
            for x in range(SPRITE_SIZE):
                color_idx = (x // 8 + y // 8) % 2
                base_color = grass_pixels[color_idx * 2] if color_idx == 0 else grass_pixels[1]
                grass.set_at((x, y), tuple(base_color))
        sprites['grass'] = grass
        
        # River sprite - animated water effect
        river = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        river.fill((0, 88, 248))
        for y in range(0, SPRITE_SIZE, 8):
            for x in range(SPRITE_SIZE):
                if (x + y) % 16 < 8:
                    river.set_at((x, y), (0, 120, 248))
                    if y + 1 < SPRITE_SIZE:
                        river.set_at((x, y + 1), (88, 160, 248))
        sprites['river'] = river
        
        # Rock sprite - chunky pixel rock
        rock = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        rock.fill((0, 168, 0))
        rock_pattern = [
            "      ####      ",
            "    ########    ",
            "   ##########   ",
            "  ############  ",
            " ############## ",
            " ############## ",
            "################",
            "################",
            "################",
            "################",
            " ############## ",
            " ############## ",
            "  ############  ",
            "   ##########   ",
            "    ########    ",
            "      ####      "
        ]
        for y, row in enumerate(rock_pattern):
            for x, char in enumerate(row):
                if char == '#':
                    px = x * 2
                    py = y * 2
                    color = (136, 136, 136) if (x + y) % 2 == 0 else (100, 100, 100)
                    pygame.draw.rect(rock, color, (px, py, 2, 2))
        sprites['rock'] = rock
        
        # Tree sprite - classic NES tree
        tree = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        tree.fill((0, 168, 0))
        # Trunk
        for y in range(20, 32):
            for x in range(12, 20):
                tree.set_at((x, y), (101, 67, 33))
        # Foliage layers
        foliage_pattern = [
            "    ####    ",
            "  ########  ",
            " ########## ",
            "############",
            "############",
            " ########## ",
            "  ########  "
        ]
        for y, row in enumerate(foliage_pattern):
            for x, char in enumerate(row):
                if char == '#':
                    px = x * 2 + 4
                    py = y * 2 + 4
                    color = (0, 120, 0) if (x + y) % 2 == 0 else (0, 100, 0)
                    pygame.draw.rect(tree, color, (px, py, 2, 2))
        sprites['tree'] = tree
        
        # Bridge sprite - wooden planks
        bridge = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        for y in range(SPRITE_SIZE):
            for x in range(SPRITE_SIZE):
                if x % 8 < 6:
                    bridge.set_at((x, y), (139, 69, 19))
                else:
                    bridge.set_at((x, y), (101, 50, 10))
        sprites['bridge'] = bridge
        
        # Chest sprite - treasure chest
        chest = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        chest.fill((0, 168, 0))
        # Chest body
        for y in range(12, 24):
            for x in range(8, 24):
                chest.set_at((x, y), (160, 82, 45))
        # Chest lid
        for y in range(8, 12):
            for x in range(8, 24):
                chest.set_at((x, y), (139, 69, 19))
        # Lock
        for y in range(16, 20):
            for x in range(14, 18):
                chest.set_at((x, y), (255, 215, 0))
        sprites['chest'] = chest
        
        # Hero sprite - Link-inspired character
        hero = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        hero.fill((0, 168, 0))
        # Head
        for y in range(6, 14):
            for x in range(10, 22):
                if 8 <= y <= 12:
                    hero.set_at((x, y), (255, 220, 177))
        # Body
        for y in range(14, 22):
            for x in range(10, 22):
                hero.set_at((x, y), (255, 0, 0))
        # Legs
        for y in range(22, 28):
            for x in range(10, 15):
                hero.set_at((x, y), (0, 0, 139))
            for x in range(17, 22):
                hero.set_at((x, y), (0, 0, 139))
        sprites['hero'] = hero
        
        return sprites
    
    def new_game(self):
        """Start a new game"""
        logger.info("Starting new game")
        self.world, self.hero = self.world_generator.generate()
        self.treasure = self.world_generator.chests
        self.collision.set_world(self.world, self.treasure)
        logger.info(f"Hero spawned at ({self.hero.x}, {self.hero.y})")
        logger.info(f"Generated {len(self.treasure)} treasure chests")
        
        self.center_camera()
    
    def center_camera(self):
        """Center camera on hero"""
        self.camera_x = self.hero.x - GRID_WIDTH // 2
        self.camera_y = self.hero.y - GRID_HEIGHT // 2
        
        # Clamp camera to world bounds
        self.camera_x = max(0, min(self.camera_x, 
                                   self.world_generator.width - GRID_WIDTH))
        self.camera_y = max(0, min(self.camera_y, 
                                   self.world_generator.height - GRID_HEIGHT))
    
    def handle_input(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Game quit by user")
                return False
            
            if event.type == pygame.KEYDOWN:
                from engine.menu import MenuState
                if self.menu.state != MenuState.CLOSED:
                    self.menu.handle_input(event)
                else:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB or event.key == pygame.K_m:
                        self.menu.toggle()
                    elif event.key == pygame.K_SPACE:
                        self.try_open_chest()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.move_hero(0, -1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.move_hero(0, 1)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.move_hero(-1, 0)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.move_hero(1, 0)
        
        return True
    
    def move_hero(self, dx, dy):
        """Move hero with collision detection"""
        new_x = self.hero.x + dx
        new_y = self.hero.y + dy
        
        # Use collision system to check if move is valid
        if not self.collision.can_move(self.hero.x, self.hero.y, new_x, new_y):
            # Get blocking reason for debugging
            reason = self.collision.get_blocking_reason(new_x, new_y)
            logger.debug(f"Movement to ({new_x}, {new_y}) blocked by: {reason}")
            return
        
        # Move hero
        self.hero.x = new_x
        self.hero.y = new_y
        self.center_camera()
        logger.debug(f"Hero moved to ({new_x}, {new_y})")
    
    def try_open_chest(self):
        """Try to open a chest next to the hero (not on hero)"""
        # Check adjacent tiles for chests (NOT the hero's current position)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            check_x = self.hero.x + dx
            check_y = self.hero.y + dy
            
            for chest in self.treasure:
                if (chest['x'] == check_x and 
                    chest['y'] == check_y and 
                    not chest['opened']):
                    self.open_treasure(chest)
                    return
        
        logger.debug("No chest nearby to open")
    
    def open_treasure(self, chest):
        """Open treasure chest and get item"""
        item = chest['item']
        chest['opened'] = True
        logger.info(f"Treasure opened! Found: {item.name}")
        
        # Add item to menu system (which handles auto-equipping)
        self.menu.add_to_inventory(item)
        
        # Show message to player
        self.show_message(f"Found: {item.name}!")
    
    def show_message(self, text):
        """Display a message to the player"""
        self.message = text
        self.message_timer = self.message_duration
        logger.debug(f"Message shown: {text}")
    
    def auto_save(self):
        """Perform auto-save"""
        self.auto_save_counter += 1
        if self.auto_save_counter >= self.auto_save_interval:
            game_state = {
                'hero': self.hero,
                'terrain': self.world,
                'chests': self.treasure,
                'seed': None,
                'width': GRID_WIDTH,
                'height': GRID_HEIGHT,
            }
            try:
                self.save_system.autosave(game_state)
                logger.debug("Auto-saved game")
            except Exception as e:
                logger.error(f"Auto-save failed: {e}")
            self.auto_save_counter = 0
    
    def update(self):
        """Update game state"""
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""
    
    def render(self):
        """Render the game"""
        self.screen.fill(NES_COLORS['black'])
        
        # Render world
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                world_x = x + self.camera_x
                world_y = y + self.camera_y
                
                if (world_x >= 0 and world_x < self.world_generator.width and
                    world_y >= 0 and world_y < self.world_generator.height):
                    
                    tile = self.world.get((world_x, world_y))
                    if tile:
                        tile_type = type(tile).__name__.lower()
                        sprite = self.sprites.get(tile_type, self.sprites['grass'])
                        self.screen.blit(sprite, (x * SPRITE_SIZE, y * SPRITE_SIZE))
        
        # Render treasure
        if self.treasure:
            for chest in self.treasure:
                if not chest['opened']:
                    screen_x = (chest['x'] - self.camera_x) * SPRITE_SIZE
                    screen_y = (chest['y'] - self.camera_y) * SPRITE_SIZE
                    if 0 <= screen_x < WINDOW_WIDTH and 0 <= screen_y < WINDOW_HEIGHT:
                        self.screen.blit(self.sprites['chest'], (screen_x, screen_y))
        
        # Render hero
        screen_x = (self.hero.x - self.camera_x) * SPRITE_SIZE
        screen_y = (self.hero.y - self.camera_y) * SPRITE_SIZE
        self.screen.blit(self.sprites['hero'], (screen_x, screen_y))
        
        # Render menu
        from engine.menu import MenuState
        if self.menu.state != MenuState.CLOSED:
            self.menu.render(self.screen, self.font)
        
        # Render message at bottom of screen
        if self.message:
            message_surf = self.font.render(self.message, True, NES_COLORS['white'])
            message_rect = message_surf.get_rect()
            message_rect.centerx = WINDOW_WIDTH // 2
            message_rect.bottom = WINDOW_HEIGHT - 10
            
            # Draw background for message
            bg_rect = message_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, NES_COLORS['black'], bg_rect)
            pygame.draw.rect(self.screen, NES_COLORS['white'], bg_rect, 2)
            
            self.screen.blit(message_surf, message_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        logger.info("Starting game loop")
        running = True
        
        try:
            while running:
                running = self.handle_input()
                self.update()
                self.auto_save()
                self.render()
                self.clock.tick(FPS)
        except Exception as e:
            logger.error(f"Game crashed: {e}", exc_info=True)
            raise
        finally:
            logger.info("Game loop ended")
            pygame.quit()

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
