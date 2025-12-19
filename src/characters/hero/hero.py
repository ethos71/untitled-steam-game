"""Hero character for the roguelike game."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from characters.hero.equipment import EquipmentManager

class Hero:
    """Represents the player character."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.char = '@'
        self.color = (255, 255, 255)  # White
        self.hp = 100
        self.max_hp = 100
        self.name = "Hero"
        self.inventory = []
        self.equipment = EquipmentManager()
        
    def move(self, dx, dy):
        """Move the hero by dx, dy."""
        self.x += dx
        self.y += dy
        
    def get_position(self):
        """Return current position."""
        return (self.x, self.y)
    
    def render_char(self):
        """Return the character to render."""
        return self.char
    
    def equip_item(self, equipment):
        """Equip an item from inventory."""
        if equipment in self.inventory:
            old_equipment = self.equipment.equip(equipment)
            if old_equipment:
                # Put old equipment back in inventory
                self.inventory.append(old_equipment)
            # Remove equipped item from inventory
            self.inventory.remove(equipment)
            return True
        return False
