"""Hero character for the roguelike game."""

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
