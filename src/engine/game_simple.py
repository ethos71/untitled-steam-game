#!/usr/bin/env python3
"""NES/Atari style roguelike game."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame
from environment.world.world_generator import WorldGenerator

# Game constants
TILE_SIZE = 16
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 50
MAP_HEIGHT = 38
FPS = 60
TITLE = "Shell Descent - NES Roguelike"

# NES Color Palette
NES_PALETTE = {
    'black': (0, 0, 0),
    'grass': (0, 168, 0),
    'tree': (0, 88, 0),
    'rock': (124, 124, 124),
    'water': (0, 120, 248),
    'hero': (252, 160, 68),
    'ui_bg': (24, 24, 24),
    'ui_text': (248, 248, 248),
}


class Game:
    """Main game class."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.generator = WorldGenerator(width=MAP_WIDTH, height=MAP_HEIGHT)
        self.terrain = {}
        self.hero = None
        self.chests = []
        self.running = True
        self.camera_x = 0
        self.camera_y = 0
        
    def initialize(self):
        """Initialize the game world."""
        self.terrain, self.hero = self.generator.generate()
        self.chests = self.generator.chests
        self.update_camera()
        
    def handle_input(self):
        """Handle keyboard input."""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
            
        # Try to move the hero
        if dx != 0 or dy != 0:
            new_x = self.hero.x + dx
            new_y = self.hero.y + dy
            
            if self.generator.is_walkable(new_x, new_y):
                self.hero.move(dx, dy)
                self.update_camera()
                self._check_chest_interaction()
    
    def update_camera(self):
        """Center camera on hero."""
        tiles_wide = SCREEN_WIDTH // TILE_SIZE
        tiles_high = (SCREEN_HEIGHT - 100) // TILE_SIZE
        self.camera_x = max(0, min(self.hero.x - tiles_wide // 2, MAP_WIDTH - tiles_wide))
        self.camera_y = max(0, min(self.hero.y - tiles_high // 2, MAP_HEIGHT - tiles_high))
    
    def render(self):
        """Render the game world."""
        self.screen.fill(NES_PALETTE['black'])
        
        # Render terrain
        tiles_wide = SCREEN_WIDTH // TILE_SIZE
        tiles_high = (SCREEN_HEIGHT - 100) // TILE_SIZE
        
        for (x, y), tile in self.terrain.items():
            if self.camera_x <= x < self.camera_x + tiles_wide and self.camera_y <= y < self.camera_y + tiles_high:
                screen_x = (x - self.camera_x) * TILE_SIZE
                screen_y = (y - self.camera_y) * TILE_SIZE
                color = self._get_tile_color(tile.char)
                pygame.draw.rect(self.screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
        
        # Render chests
        for chest in self.chests:
            if self.camera_x <= chest['x'] < self.camera_x + tiles_wide and \
               self.camera_y <= chest['y'] < self.camera_y + tiles_high:
                screen_x = (chest['x'] - self.camera_x) * TILE_SIZE
                screen_y = (chest['y'] - self.camera_y) * TILE_SIZE
                chest_color = (139, 69, 19) if not chest['opened'] else (100, 50, 10)
                pygame.draw.rect(self.screen, chest_color, (screen_x + 2, screen_y + 2, TILE_SIZE - 4, TILE_SIZE - 4))
        
        # Render hero
        hero_screen_x = (self.hero.x - self.camera_x) * TILE_SIZE
        hero_screen_y = (self.hero.y - self.camera_y) * TILE_SIZE
        pygame.draw.circle(self.screen, NES_PALETTE['hero'], 
                          (hero_screen_x + TILE_SIZE // 2, hero_screen_y + TILE_SIZE // 2), 
                          TILE_SIZE // 2)
        
        # Render UI
        self._render_ui()
    
    def _get_tile_color(self, char):
        """Get NES color for tile character."""
        color_map = {
            '.': NES_PALETTE['grass'],
            'T': NES_PALETTE['tree'],
            '^': NES_PALETTE['rock'],
            '~': NES_PALETTE['water'],
        }
        return color_map.get(char, NES_PALETTE['grass'])
    
    def _render_ui(self):
        """Render UI elements."""
        ui_y = SCREEN_HEIGHT - 90
        pygame.draw.rect(self.screen, NES_PALETTE['ui_bg'], (0, ui_y, SCREEN_WIDTH, 90))
        
        font = pygame.font.Font(None, 36)
        hp_text = font.render(f"HP: {self.hero.hp}/{self.hero.max_hp}", True, NES_PALETTE['ui_text'])
        pos_text = font.render(f"Pos: ({self.hero.x}, {self.hero.y})", True, NES_PALETTE['ui_text'])
        help_text = font.render("WASD/Arrows:Move | R:Regen | ESC:Quit", True, NES_PALETTE['ui_text'])
        
        self.screen.blit(hp_text, (10, ui_y + 10))
        self.screen.blit(pos_text, (10, ui_y + 40))
        self.screen.blit(help_text, (250, ui_y + 25))
    
    def _check_chest_interaction(self):
        """Check if hero is on a chest and open it."""
        for chest in self.chests:
            if chest['x'] == self.hero.x and chest['y'] == self.hero.y and not chest['opened']:
                chest['opened'] = True
                item = chest['item']
                self.hero.inventory.append(item)
                print(f"Found {item.name}! Added to inventory.")


def main():
    """Main entry point."""
    game = Game()
    game.initialize()
    
    # Main game loop
    while game.running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                elif event.key == pygame.K_r:
                    game.initialize()
        
        # Handle continuous input
        game.handle_input()
        
        # Render
        game.render()
        pygame.display.flip()
        game.clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()
