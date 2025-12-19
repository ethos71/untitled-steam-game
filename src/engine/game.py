#!/usr/bin/env python3
"""
NES Roguelike - Simplified Main Game Engine
Clean architecture with separated concerns
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
from engine.game_state import GameState
from engine.renderer import Renderer
from engine.input_handler import InputHandler
from engine.simple_menu import SimpleMenu

# Game constants
SPRITE_SIZE = 32
GRID_WIDTH = 25
GRID_HEIGHT = 19
WINDOW_WIDTH = GRID_WIDTH * SPRITE_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * SPRITE_SIZE
FPS = 60

class Game:
    """Main game class - coordinates all systems"""
    
    def __init__(self):
        logger.info("=== NES Roguelike Starting ===")
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("NES Roguelike")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        
        # Initialize game systems
        self.game_state = GameState(GRID_WIDTH, GRID_HEIGHT)
        self.renderer = Renderer(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.input_handler = InputHandler()
        self.menu = SimpleMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.world_generator = WorldGenerator(GRID_WIDTH * 2, GRID_HEIGHT * 2)
        
        # Start new game
        self.new_game()
        
        logger.info("Game initialized successfully")
    
    def new_game(self):
        """Start a new game"""
        logger.info("Starting new game")
        
        # Generate world
        world, hero = self.world_generator.generate()
        self.game_state.set_world(world, self.world_generator.width, self.world_generator.height)
        self.game_state.set_hero_position(hero.x, hero.y)
        
        # Add chests
        for chest_data in self.world_generator.chests:
            self.game_state.add_chest(
                chest_data['x'],
                chest_data['y'],
                chest_data['item']
            )
        
        logger.info(f"World generated: {self.world_generator.width}x{self.world_generator.height}")
        logger.info(f"Hero at ({hero.x}, {hero.y})")
        logger.info(f"{len(self.game_state.chests)} chests placed")
    
    def run(self):
        """Main game loop"""
        logger.info("Starting game loop")
        running = True
        
        try:
            while running:
                # Handle input
                running = self.input_handler.handle_events(self.game_state, self.menu)
                
                # Render
                self.screen.fill((0, 0, 0))
                self.renderer.render_world(self.screen, self.game_state, GRID_WIDTH, GRID_HEIGHT)
                self.renderer.render_chests(self.screen, self.game_state)
                self.renderer.render_hero(self.screen, self.game_state)
                
                # Render menu if open
                if self.input_handler.menu_open:
                    self.menu.render(self.screen, self.font, self.game_state)
                
                pygame.display.flip()
                self.clock.tick(FPS)
                
        except Exception as e:
            logger.error(f"Game crashed: {e}", exc_info=True)
            raise
        finally:
            logger.info("Game loop ended")
            pygame.quit()

def main():
    """Entry point"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
