#!/usr/bin/env python3
"""NES/Atari style roguelike game."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame
from environment.world.world_generator import WorldGenerator
from engine.save_system import SaveSystem
from characters.hero.equipment import Item

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
        self.save_system = SaveSystem()
        self.show_menu = False
        self.menu_state = "main"  # main, save, load
        self.autosave_timer = 0
        self.AUTOSAVE_INTERVAL = 300  # Auto-save every 5 minutes (300 seconds)
        
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
                
                # Trigger autosave after movement
                self.autosave_timer += 1
                if self.autosave_timer >= 60:  # Every 60 moves
                    self._autosave()
                    self.autosave_timer = 0
    
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
        
        # Render menu if active
        if self.show_menu:
            self._render_menu()
    
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
        help_text = font.render("WASD:Move | M:Menu | R:Regen | ESC:Quit", True, NES_PALETTE['ui_text'])
        
        self.screen.blit(hp_text, (10, ui_y + 10))
        self.screen.blit(pos_text, (10, ui_y + 40))
        self.screen.blit(help_text, (250, ui_y + 25))
    
    def _check_chest_interaction(self):
        """Check if hero is on a chest and open it."""
        for chest in self.chests:
            if chest['x'] == self.hero.x and chest['y'] == self.hero.y and not chest['opened']:
                chest['opened'] = True
                item = chest['item']
                
                # Auto-equip if slot is empty
                previous = self.hero.equipment_manager.equip(item, auto_equip=True)
                
                if previous is None and self.hero.equipment_manager.get_equipped(item.slot) == item:
                    print(f"Found {item.name}! Auto-equipped.")
                else:
                    # Slot was full, add to inventory
                    self.hero.inventory.append(item)
                    print(f"Found {item.name}! Added to inventory.")
    
    def _autosave(self):
        """Perform auto-save."""
        game_state = {
            'hero': self.hero,
            'terrain': self.terrain,
            'chests': self.chests,
            'width': MAP_WIDTH,
            'height': MAP_HEIGHT
        }
        if self.save_system.autosave(game_state):
            print("Game auto-saved!")
    
    def save_game(self, slot_name):
        """Save game to specific slot."""
        game_state = {
            'hero': self.hero,
            'terrain': self.terrain,
            'chests': self.chests,
            'width': MAP_WIDTH,
            'height': MAP_HEIGHT
        }
        if self.save_system.save_game(game_state, slot_name):
            print(f"Game saved to {slot_name}!")
            return True
        return False
    
    def load_game(self, slot_name):
        """Load game from specific slot."""
        data = self.save_system.load_game(slot_name)
        if data:
            self._restore_from_data(data)
            print(f"Game loaded from {slot_name}!")
            return True
        return False
    
    def _restore_from_data(self, data):
        """Restore game state from loaded data."""
        from environment.world.tile import Tile
        
        # Restore terrain
        self.terrain = {}
        for key, tile_data in data['terrain'].items():
            x, y = map(int, key.split(','))
            self.terrain[(x, y)] = Tile(tile_data['char'], tile_data['walkable'])
        
        # Restore hero
        self.hero.x = data['hero']['x']
        self.hero.y = data['hero']['y']
        self.hero.hp = data['hero']['hp']
        self.hero.max_hp = data['hero']['max_hp']
        
        # Restore inventory
        self.hero.inventory = []
        for item_data in data['hero']['inventory']:
            item = Item(item_data['name'], item_data['slot'], item_data['stats'])
            self.hero.inventory.append(item)
        
        # Restore equipment
        for slot, item_data in data['hero']['equipment'].items():
            if item_data:
                item = Item(item_data['name'], item_data['slot'], item_data['stats'])
                self.hero.equipment_manager.equipment[slot] = item
        
        # Restore chests
        self.chests = data['chests']
        
        self.update_camera()
    
    def _render_menu(self):
        """Render save/load menu."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(NES_PALETTE['black'])
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 36)
        
        if self.menu_state == "main":
            title = font.render("MENU", True, NES_PALETTE['ui_text'])
            self.screen.blit(title, (SCREEN_WIDTH // 2 - 60, 100))
            
            options = ["1. Save Game", "2. Load Game", "3. Resume", "ESC. Quit"]
            for i, option in enumerate(options):
                text = small_font.render(option, True, NES_PALETTE['ui_text'])
                self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, 200 + i * 50))
        
        elif self.menu_state == "save":
            title = font.render("SAVE GAME", True, NES_PALETTE['ui_text'])
            self.screen.blit(title, (SCREEN_WIDTH // 2 - 100, 100))
            
            instructions = small_font.render("Enter slot name (1-5) or ESC to cancel", True, NES_PALETTE['ui_text'])
            self.screen.blit(instructions, (SCREEN_WIDTH // 2 - 250, 200))
        
        elif self.menu_state == "load":
            title = font.render("LOAD GAME", True, NES_PALETTE['ui_text'])
            self.screen.blit(title, (SCREEN_WIDTH // 2 - 100, 100))
            
            saves = self.save_system.list_saves()
            if saves:
                for i, save in enumerate(saves[:5]):
                    text = small_font.render(f"{i+1}. {save['name']} - {save['timestamp'][:19]}", 
                                            True, NES_PALETTE['ui_text'])
                    self.screen.blit(text, (50, 200 + i * 40))
            else:
                text = small_font.render("No saves found", True, NES_PALETTE['ui_text'])
                self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, 200))
            
            instructions = small_font.render("Press slot number (1-5) or ESC to cancel", 
                                            True, NES_PALETTE['ui_text'])
            self.screen.blit(instructions, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 100))


def main():
    """Main entry point."""
    game = Game()
    
    # Try to load autosave on crash recovery
    autosave_data = game.save_system.load_autosave()
    if autosave_data:
        print("Autosave found! Press L to load or any other key to start new game...")
        # For now, just start new game (can enhance with prompt later)
    
    game.initialize()
    
    # Main game loop
    while game.running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game._autosave()
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game.show_menu:
                        game.show_menu = False
                        game.menu_state = "main"
                    else:
                        game._autosave()
                        game.running = False
                elif event.key == pygame.K_m:
                    game.show_menu = not game.show_menu
                    game.menu_state = "main"
                elif game.show_menu:
                    if game.menu_state == "main":
                        if event.key == pygame.K_1:
                            game.menu_state = "save"
                        elif event.key == pygame.K_2:
                            game.menu_state = "load"
                        elif event.key == pygame.K_3:
                            game.show_menu = False
                    elif game.menu_state == "save":
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                            slot = f"save_{event.key - pygame.K_1 + 1}"
                            game.save_game(slot)
                            game.show_menu = False
                            game.menu_state = "main"
                    elif game.menu_state == "load":
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                            slot = f"save_{event.key - pygame.K_1 + 1}"
                            game.load_game(slot)
                            game.show_menu = False
                            game.menu_state = "main"
                elif event.key == pygame.K_r:
                    game.initialize()
        
        # Handle continuous input (only if menu is not shown)
        if not game.show_menu:
            game.handle_input()
        
        # Render
        game.render()
        pygame.display.flip()
        game.clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()
