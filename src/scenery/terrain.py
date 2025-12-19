"""Terrain elements for the game world."""
import random

class Terrain:
    """Base class for terrain elements."""
    
    def __init__(self, x, y, char, color, blocks_movement=False, blocks_sight=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.blocks_movement = blocks_movement
        self.blocks_sight = blocks_sight
        self.name = "terrain"

class Tree(Terrain):
    """A tree in the world."""
    
    def __init__(self, x, y):
        tree_chars = ['♣', '♠', 'T', '↑']
        char = random.choice(tree_chars)
        color = (34, 139, 34)  # Forest green
        super().__init__(x, y, char, color, blocks_movement=True, blocks_sight=True)
        self.name = "tree"

class Rock(Terrain):
    """A rock in the world."""
    
    def __init__(self, x, y):
        rock_chars = ['○', '●', '*', '◘']
        char = random.choice(rock_chars)
        color = (128, 128, 128)  # Gray
        super().__init__(x, y, char, color, blocks_movement=True, blocks_sight=False)
        self.name = "rock"

class River(Terrain):
    """Water/river tile."""
    
    def __init__(self, x, y):
        water_chars = ['~', '≈', '∼']
        char = random.choice(water_chars)
        color = (64, 164, 223)  # Blue
        super().__init__(x, y, char, color, blocks_movement=True, blocks_sight=False)
        self.name = "river"

class Grass(Terrain):
    """Grass ground tile."""
    
    def __init__(self, x, y):
        grass_chars = ['.', ',', '"', '\'']
        char = random.choice(grass_chars)
        color = (50, 205, 50)  # Lime green
        super().__init__(x, y, char, color, blocks_movement=False, blocks_sight=False)
        self.name = "grass"
