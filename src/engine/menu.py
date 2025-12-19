"""
Menu System for NES/Atari Style Game
Handles equipment management and game settings
"""

import pygame
from enum import Enum
from typing import Optional, List, Callable
from dataclasses import dataclass


class MenuState(Enum):
    """Menu states"""
    CLOSED = "closed"
    MAIN = "main"
    EQUIPMENT = "equipment"
    OPTIONS = "options"


class EquipSlot(Enum):
    """Equipment slots for hero"""
    HEAD = "Head"
    CHEST = "Chest"
    FEET = "Feet"
    RING_1 = "Ring 1"
    RING_2 = "Ring 2"
    WEAPON_1 = "Weapon 1"
    WEAPON_2 = "Weapon 2"


@dataclass
class MenuItem:
    """Menu item with text and action"""
    text: str
    action: Callable
    enabled: bool = True


class MenuSystem:
    """Manages game menus"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state = MenuState.CLOSED
        self.selected_index = 0
        
        # Menu colors (NES palette inspired)
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 200, 0)
        self.disabled_color = (100, 100, 100)
        self.border_color = (200, 200, 200)
        
        # Equipment slots
        self.equipment_slots = {
            EquipSlot.HEAD: None,
            EquipSlot.CHEST: None,
            EquipSlot.FEET: None,
            EquipSlot.RING_1: None,
            EquipSlot.RING_2: None,
            EquipSlot.WEAPON_1: None,
            EquipSlot.WEAPON_2: None,
        }
        
        # Options
        self.options = {
            "volume": 50,
            "sfx_volume": 50,
            "screen_shake": True,
            "particles": True,
            "difficulty": "Normal",
        }
        
        # Current menus
        self.main_menu_items = []
        self.equipment_menu_items = []
        self.options_menu_items = []
        
        self._build_menus()
    
    def _build_menus(self):
        """Build all menu structures"""
        self.main_menu_items = [
            MenuItem("Equipment", self._open_equipment),
            MenuItem("Options", self._open_options),
            MenuItem("Resume", self.close),
        ]
        
        self.equipment_menu_items = [
            MenuItem(f"{slot.value}: {self._get_equipped_name(slot)}", 
                    lambda s=slot: self._select_equipment(s))
            for slot in EquipSlot
        ]
        self.equipment_menu_items.append(MenuItem("Back", self._open_main))
        
        self.options_menu_items = [
            MenuItem(f"Music Volume: {self.options['volume']}", self._adjust_volume),
            MenuItem(f"SFX Volume: {self.options['sfx_volume']}", self._adjust_sfx),
            MenuItem(f"Screen Shake: {'ON' if self.options['screen_shake'] else 'OFF'}", 
                    self._toggle_shake),
            MenuItem(f"Particles: {'ON' if self.options['particles'] else 'OFF'}", 
                    self._toggle_particles),
            MenuItem(f"Difficulty: {self.options['difficulty']}", self._cycle_difficulty),
            MenuItem("Back", self._open_main),
        ]
    
    def _get_equipped_name(self, slot: EquipSlot) -> str:
        """Get name of equipped item or 'Empty'"""
        item = self.equipment_slots[slot]
        return item.name if item else "Empty"
    
    def open(self):
        """Open main menu"""
        self.state = MenuState.MAIN
        self.selected_index = 0
    
    def close(self):
        """Close menu"""
        self.state = MenuState.CLOSED
        self.selected_index = 0
    
    def is_open(self) -> bool:
        """Check if menu is open"""
        return self.state != MenuState.CLOSED
    
    def _open_main(self):
        """Open main menu"""
        self.state = MenuState.MAIN
        self.selected_index = 0
    
    def _open_equipment(self):
        """Open equipment menu"""
        self.state = MenuState.EQUIPMENT
        self.selected_index = 0
        self._build_menus()  # Rebuild to update equipment display
    
    def _open_options(self):
        """Open options menu"""
        self.state = MenuState.OPTIONS
        self.selected_index = 0
    
    def _select_equipment(self, slot: EquipSlot):
        """Handle equipment selection"""
        print(f"Selected equipment slot: {slot.value}")
        # TODO: Open inventory to select item for this slot
    
    def _adjust_volume(self):
        """Adjust music volume"""
        self.options['volume'] = (self.options['volume'] + 10) % 110
        self._build_menus()
    
    def _adjust_sfx(self):
        """Adjust SFX volume"""
        self.options['sfx_volume'] = (self.options['sfx_volume'] + 10) % 110
        self._build_menus()
    
    def _toggle_shake(self):
        """Toggle screen shake"""
        self.options['screen_shake'] = not self.options['screen_shake']
        self._build_menus()
    
    def _toggle_particles(self):
        """Toggle particles"""
        self.options['particles'] = not self.options['particles']
        self._build_menus()
    
    def _cycle_difficulty(self):
        """Cycle through difficulty options"""
        difficulties = ["Easy", "Normal", "Hard", "Nightmare"]
        current = difficulties.index(self.options['difficulty'])
        self.options['difficulty'] = difficulties[(current + 1) % len(difficulties)]
        self._build_menus()
    
    def handle_input(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._activate_selected()
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self._move_selection(-1)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self._move_selection(1)
            elif event.key == pygame.K_ESCAPE:
                if self.state == MenuState.MAIN:
                    self.close()
                else:
                    self._open_main()
    
    def _get_current_menu(self) -> List[MenuItem]:
        """Get current menu items"""
        if self.state == MenuState.MAIN:
            return self.main_menu_items
        elif self.state == MenuState.EQUIPMENT:
            return self.equipment_menu_items
        elif self.state == MenuState.OPTIONS:
            return self.options_menu_items
        return []
    
    def _move_selection(self, direction: int):
        """Move menu selection"""
        menu = self._get_current_menu()
        if menu:
            self.selected_index = (self.selected_index + direction) % len(menu)
    
    def _activate_selected(self):
        """Activate selected menu item"""
        menu = self._get_current_menu()
        if menu and 0 <= self.selected_index < len(menu):
            item = menu[self.selected_index]
            if item.enabled:
                item.action()
    
    def equip_item(self, slot: EquipSlot, item):
        """Equip an item to a slot"""
        old_item = self.equipment_slots[slot]
        self.equipment_slots[slot] = item
        self._build_menus()
        return old_item
    
    def render(self, screen, font):
        """Render the menu"""
        if not self.is_open():
            return
        
        # Menu dimensions
        menu_width = 400
        menu_height = 350
        menu_x = (self.screen_width - menu_width) // 2
        menu_y = (self.screen_height - menu_height) // 2
        
        # Draw menu background
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, self.bg_color, menu_rect)
        pygame.draw.rect(screen, self.border_color, menu_rect, 3)
        
        # Draw title
        title = self._get_menu_title()
        title_surf = font.render(title, True, self.text_color)
        title_rect = title_surf.get_rect(centerx=menu_x + menu_width // 2, top=menu_y + 20)
        screen.blit(title_surf, title_rect)
        
        # Draw menu items
        menu = self._get_current_menu()
        item_y = menu_y + 70
        item_spacing = 35
        
        for i, item in enumerate(menu):
            color = self.selected_color if i == self.selected_index else self.text_color
            if not item.enabled:
                color = self.disabled_color
            
            # Draw selection indicator
            if i == self.selected_index:
                indicator = "> "
            else:
                indicator = "  "
            
            text_surf = font.render(indicator + item.text, True, color)
            screen.blit(text_surf, (menu_x + 40, item_y))
            item_y += item_spacing
    
    def _get_menu_title(self) -> str:
        """Get current menu title"""
        if self.state == MenuState.MAIN:
            return "MENU"
        elif self.state == MenuState.EQUIPMENT:
            return "EQUIPMENT"
        elif self.state == MenuState.OPTIONS:
            return "OPTIONS"
        return ""
