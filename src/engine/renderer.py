"""
Simplified rendering system
"""
import pygame
import logging

logger = logging.getLogger(__name__)

SPRITE_SIZE = 32

class Renderer:
    """Handles all rendering"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sprites = self._create_sprites()
        logger.info("Renderer initialized")
    
    def _create_sprites(self):
        """Create all game sprites"""
        sprites = {}
        
        # Grass - simple green with variation
        grass = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        for y in range(SPRITE_SIZE):
            for x in range(SPRITE_SIZE):
                color = (0, 168, 0) if (x + y) % 4 < 2 else (0, 180, 0)
                grass.set_at((x, y), color)
        sprites['grass'] = grass
        
        # River - blue with waves
        river = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        river.fill((0, 88, 248))
        for y in range(0, SPRITE_SIZE, 4):
            for x in range(SPRITE_SIZE):
                if (x + y) % 8 < 4:
                    river.set_at((x, y), (88, 160, 248))
        sprites['river'] = river
        
        # Rock - gray boulder
        rock = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        rock.fill((0, 168, 0))
        pygame.draw.circle(rock, (136, 136, 136), (16, 16), 12)
        pygame.draw.circle(rock, (100, 100, 100), (16, 16), 10)
        sprites['rock'] = rock
        
        # Tree - green circle on brown trunk
        tree = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        tree.fill((0, 168, 0))
        pygame.draw.rect(tree, (101, 67, 33), (12, 18, 8, 14))  # Trunk
        pygame.draw.circle(tree, (0, 120, 0), (16, 12), 10)  # Foliage
        pygame.draw.circle(tree, (0, 100, 0), (16, 12), 8)
        sprites['tree'] = tree
        
        # Bridge - brown planks
        bridge = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        for x in range(0, SPRITE_SIZE, 8):
            pygame.draw.rect(bridge, (139, 69, 19), (x, 0, 6, SPRITE_SIZE))
        sprites['bridge'] = bridge
        
        # Chest - brown box with gold lock
        chest = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        chest.fill((0, 168, 0))
        pygame.draw.rect(chest, (160, 82, 45), (6, 10, 20, 16))  # Body
        pygame.draw.rect(chest, (139, 69, 19), (6, 8, 20, 6))  # Lid
        pygame.draw.rect(chest, (255, 215, 0), (13, 16, 6, 6))  # Lock
        sprites['chest'] = chest
        
        # Hero - red character
        hero = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        hero.fill((0, 168, 0))
        pygame.draw.circle(hero, (255, 220, 177), (16, 10), 6)  # Head
        pygame.draw.rect(hero, (255, 0, 0), (10, 14, 12, 10))  # Body
        pygame.draw.rect(hero, (0, 0, 139), (10, 24, 5, 6))  # Left leg
        pygame.draw.rect(hero, (0, 0, 139), (17, 24, 5, 6))  # Right leg
        sprites['hero'] = hero
        
        logger.info("Created all sprites")
        return sprites
    
    def render_world(self, screen, game_state, grid_width, grid_height):
        """Render the visible world"""
        for y in range(grid_height):
            for x in range(grid_width):
                world_x = x + game_state.camera_x
                world_y = y + game_state.camera_y
                
                if (0 <= world_x < game_state.world_width and
                    0 <= world_y < game_state.world_height):
                    
                    tile = game_state.world.get((world_x, world_y))
                    if tile:
                        tile_type = type(tile).__name__.lower()
                        sprite = self.sprites.get(tile_type, self.sprites['grass'])
                    else:
                        sprite = self.sprites['grass']
                    
                    screen.blit(sprite, (x * SPRITE_SIZE, y * SPRITE_SIZE))
    
    def render_chests(self, screen, game_state):
        """Render treasure chests"""
        for chest in game_state.chests:
            screen_x = (chest['x'] - game_state.camera_x) * SPRITE_SIZE
            screen_y = (chest['y'] - game_state.camera_y) * SPRITE_SIZE
            
            if 0 <= screen_x < self.screen_width and 0 <= screen_y < self.screen_height:
                screen.blit(self.sprites['chest'], (screen_x, screen_y))
                # If opened, draw an indicator
                if chest['opened']:
                    # Draw a lighter overlay to show it's opened
                    overlay = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
                    overlay.fill((255, 255, 255))
                    overlay.set_alpha(100)
                    screen.blit(overlay, (screen_x, screen_y))
    
    def render_hero(self, screen, game_state):
        """Render hero"""
        screen_x = (game_state.hero_x - game_state.camera_x) * SPRITE_SIZE
        screen_y = (game_state.hero_y - game_state.camera_y) * SPRITE_SIZE
        screen.blit(self.sprites['hero'], (screen_x, screen_y))
