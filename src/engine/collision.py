"""
Collision System for NES Roguelike
Handles all collision detection and tile blocking logic
"""
import logging

logger = logging.getLogger(__name__)

class CollisionSystem:
    """Manages collision detection for the game"""
    
    # Define which tile types block movement
    BLOCKING_TILES = {'river', 'rock', 'tree', 'chest'}
    
    # Define which tile types are walkable
    WALKABLE_TILES = {'grass', 'bridge'}
    
    def __init__(self, world_generator):
        """
        Initialize collision system
        
        Args:
            world_generator: WorldGenerator instance with terrain data
        """
        self.world_generator = world_generator
        self.world = None
        self.chests = []
        logger.info("Collision system initialized")
    
    def set_world(self, world, chests):
        """
        Set the current world and chests for collision checking
        
        Args:
            world: Dictionary of terrain tiles
            chests: List of treasure chest dictionaries
        """
        self.world = world
        self.chests = chests
        logger.debug(f"Collision system updated with {len(chests)} chests")
    
    def is_blocked(self, x, y):
        """
        Check if a position is blocked
        
        Args:
            x: X coordinate to check
            y: Y coordinate to check
            
        Returns:
            bool: True if position is blocked, False if walkable
        """
        # Check world bounds
        if (x < 0 or x >= self.world_generator.width or
            y < 0 or y >= self.world_generator.height):
            logger.debug(f"Position ({x}, {y}) is out of bounds")
            return True
        
        # Check for closed chests at this position
        for chest in self.chests:
            if chest['x'] == x and chest['y'] == y and not chest['opened']:
                logger.debug(f"Position ({x}, {y}) blocked by chest")
                return True
        
        # Check terrain tile
        tile = self.world.get((x, y))
        if tile:
            tile_type = type(tile).__name__.lower()
            
            # Explicitly check if tile is walkable
            if tile_type in self.WALKABLE_TILES:
                return False
            
            # Check if tile is blocking
            if tile_type in self.BLOCKING_TILES:
                logger.debug(f"Position ({x}, {y}) blocked by {tile_type}")
                return True
        
        # Default to walkable (grass)
        return False
    
    def can_move(self, from_x, from_y, to_x, to_y):
        """
        Check if entity can move from one position to another
        
        Args:
            from_x: Current X position
            from_y: Current Y position
            to_x: Target X position
            to_y: Target Y position
            
        Returns:
            bool: True if move is valid, False otherwise
        """
        # Check if target position is blocked
        if self.is_blocked(to_x, to_y):
            return False
        
        # Additional checks can be added here (diagonal movement, etc.)
        return True
    
    def get_blocking_reason(self, x, y):
        """
        Get the reason why a position is blocked (for debugging/UI)
        
        Args:
            x: X coordinate to check
            y: Y coordinate to check
            
        Returns:
            str: Reason for blocking, or empty string if not blocked
        """
        if x < 0 or x >= self.world_generator.width or y < 0 or y >= self.world_generator.height:
            return "Out of bounds"
        
        for chest in self.chests:
            if chest['x'] == x and chest['y'] == y and not chest['opened']:
                return "Treasure chest"
        
        tile = self.world.get((x, y))
        if tile:
            tile_type = type(tile).__name__.lower()
            if tile_type in self.BLOCKING_TILES:
                return tile_type.capitalize()
        
        return ""
