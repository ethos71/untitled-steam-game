"""
Centralized game state management
"""
import logging

logger = logging.getLogger(__name__)

class GameState:
    """Manages all game state in one place"""
    
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        # World state
        self.world = {}
        self.world_width = 0
        self.world_height = 0
        
        # Hero state
        self.hero_x = 0
        self.hero_y = 0
        
        # Camera state
        self.camera_x = 0
        self.camera_y = 0
        
        # Treasure state
        self.chests = []
        
        # Inventory state
        self.inventory = {
            'head': None,
            'body': None,
            'hands': None,
            'legs': None,
            'feet': None,
            'weapon': None,
            'shield': None,
            'accessory_1': None,
            'accessory_2': None,
            'items': []  # Unequipped items
        }
        
        logger.info("Game state initialized")
    
    def set_world(self, world, width, height):
        """Set world data"""
        self.world = world
        self.world_width = width
        self.world_height = height
        logger.info(f"World set: {width}x{height}")
    
    def set_hero_position(self, x, y):
        """Set hero position"""
        self.hero_x = x
        self.hero_y = y
        self.center_camera()
        logger.debug(f"Hero position: ({x}, {y})")
    
    def center_camera(self):
        """Center camera on hero"""
        self.camera_x = self.hero_x - self.grid_width // 2
        self.camera_y = self.hero_y - self.grid_height // 2
        
        # Clamp to world bounds
        self.camera_x = max(0, min(self.camera_x, self.world_width - self.grid_width))
        self.camera_y = max(0, min(self.camera_y, self.world_height - self.grid_height))
    
    def add_chest(self, x, y, item):
        """Add a treasure chest"""
        self.chests.append({
            'x': x,
            'y': y,
            'item': item,
            'opened': False
        })
    
    def get_chest_at(self, x, y):
        """Get unopened chest at position"""
        for chest in self.chests:
            if chest['x'] == x and chest['y'] == y and not chest['opened']:
                return chest
        return None
    
    def open_chest(self, chest):
        """Open a chest and add item to inventory"""
        if chest and not chest['opened']:
            chest['opened'] = True
            item = chest['item']
            self.add_item(item)
            logger.info(f"Opened chest: {item.name}")
            return item
        return None
    
    def add_item(self, item):
        """Add item to inventory and auto-equip if slot is empty"""
        slot_type = item.slot.value if hasattr(item.slot, 'value') else item.slot
        
        # Map item slots to inventory slots (direct mapping now)
        if slot_type in self.inventory and slot_type != 'items':
            if self.inventory[slot_type] is None:
                self.inventory[slot_type] = item
                logger.info(f"Auto-equipped {item.name} to {slot_type}")
                return
            # Handle accessory slots (accessory_1, accessory_2)
            elif slot_type == 'accessory':
                if self.inventory['accessory_1'] is None:
                    self.inventory['accessory_1'] = item
                    logger.info(f"Auto-equipped {item.name} to accessory_1")
                    return
                elif self.inventory['accessory_2'] is None:
                    self.inventory['accessory_2'] = item
                    logger.info(f"Auto-equipped {item.name} to accessory_2")
                    return
        
        # If no slot available, add to items list
        self.inventory['items'].append(item)
        logger.info(f"Added {item.name} to inventory")
    
    def can_move_to(self, x, y):
        """Check if hero can move to position"""
        # Check bounds
        if x < 0 or x >= self.world_width or y < 0 or y >= self.world_height:
            return False
        
        # Check tile collision
        tile = self.world.get((x, y))
        if tile:
            tile_type = type(tile).__name__.lower()
            if tile_type in ['river', 'rock', 'tree']:
                return False
        
        return True
    
    def move_hero(self, dx, dy):
        """Move hero if possible"""
        new_x = self.hero_x + dx
        new_y = self.hero_y + dy
        
        if self.can_move_to(new_x, new_y):
            self.set_hero_position(new_x, new_y)
            return True
        return False
