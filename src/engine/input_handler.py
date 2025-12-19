"""
Input handling system
"""
import pygame
import logging

logger = logging.getLogger(__name__)

class InputHandler:
    """Handles all keyboard/mouse input"""
    
    def __init__(self):
        self.menu_open = False
        logger.info("Input handler initialized")
    
    def handle_events(self, game_state, menu_system):
        """Process all input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quit event received")
                return False
            
            if event.type == pygame.KEYDOWN:
                if not self.handle_keydown(event, game_state, menu_system):
                    return False
        
        return True
    
    def handle_keydown(self, event, game_state, menu_system):
        """Handle key press"""
        key = event.key
        
        # Menu controls
        if key in [pygame.K_TAB, pygame.K_m, pygame.K_ESCAPE]:
            self.menu_open = not self.menu_open
            logger.debug(f"Menu toggled: {self.menu_open}")
            return True
        
        # If menu is open, handle menu input
        if self.menu_open:
            return self.handle_menu_input(key, menu_system)
        
        # Game controls
        if key == pygame.K_SPACE:
            return self.try_open_chest(game_state)
        elif key in [pygame.K_UP, pygame.K_w]:
            game_state.move_hero(0, -1)
        elif key in [pygame.K_DOWN, pygame.K_s]:
            game_state.move_hero(0, 1)
        elif key in [pygame.K_LEFT, pygame.K_a]:
            game_state.move_hero(-1, 0)
        elif key in [pygame.K_RIGHT, pygame.K_d]:
            game_state.move_hero(1, 0)
        
        return True
    
    def handle_menu_input(self, key, menu_system):
        """Handle menu navigation"""
        if key == pygame.K_UP:
            menu_system.move_cursor(-1)
        elif key == pygame.K_DOWN:
            menu_system.move_cursor(1)
        elif key == pygame.K_RETURN:
            menu_system.select_option()
        
        return True
    
    def try_open_chest(self, game_state):
        """Try to open chest near hero"""
        # Check hero's tile and adjacent tiles
        for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            check_x = game_state.hero_x + dx
            check_y = game_state.hero_y + dy
            
            chest = game_state.get_chest_at(check_x, check_y)
            if chest:
                item = game_state.open_chest(chest)
                if item:
                    logger.info(f"Opened chest with {item.name}")
                return True
        
        logger.debug("No chest nearby")
        return True
