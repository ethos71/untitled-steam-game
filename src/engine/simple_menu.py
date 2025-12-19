"""
Simplified menu system
"""
import pygame
import logging

logger = logging.getLogger(__name__)

class SimpleMenu:
    """Simple menu display"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cursor = 0
        self.options = ['Inventory', 'Options', 'Save', 'Load', 'Close']
        logger.info("Menu system initialized")
    
    def move_cursor(self, direction):
        """Move menu cursor"""
        self.cursor = (self.cursor + direction) % len(self.options)
    
    def select_option(self):
        """Handle menu selection"""
        option = self.options[self.cursor]
        logger.info(f"Menu option selected: {option}")
        # TODO: Implement menu actions
    
    def render(self, screen, font, game_state):
        """Render menu overlay"""
        # Semi-transparent background
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 20))
        screen.blit(overlay, (0, 0))
        
        # Menu title
        title = font.render("MENU", True, (255, 255, 255))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        
        # Inventory section
        y = 120
        inv_title = font.render("INVENTORY", True, (200, 200, 200))
        screen.blit(inv_title, (50, y))
        y += 40
        
        slots = ['head', 'chest', 'legs', 'weapon1', 'weapon2', 'ring1', 'ring2']
        for slot in slots:
            item = game_state.inventory.get(slot)
            item_name = item.name if item else "Empty"
            text = font.render(f"{slot.upper()}: {item_name}", True, (150, 150, 150))
            screen.blit(text, (70, y))
            y += 35
        
        # Menu options
        y = self.height - 200
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.cursor else (180, 180, 180)
            text = font.render(f"{'>' if i == self.cursor else ' '} {option}", True, color)
            screen.blit(text, (self.width // 2 - 100, y))
            y += 35
