#!/usr/bin/env python3
"""Main game entry point for the ASCII roguelike."""
import tcod
from world.world_generator import WorldGenerator

# Game constants
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
TITLE = "ASCII Roguelike"

# Color palette
COLOR_DARK_WALL = (0, 0, 100)
COLOR_DARK_GROUND = (50, 50, 150)


class Game:
    """Main game class."""
    
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.generator = WorldGenerator(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.terrain = {}
        self.hero = None
        self.running = True
        
    def initialize(self):
        """Initialize the game world."""
        self.terrain, self.hero = self.generator.generate()
        
    def handle_input(self, event):
        """Handle keyboard input."""
        if event.type == "QUIT":
            self.running = False
            return
            
        if event.type == "KEYDOWN":
            # Movement keys
            dx, dy = 0, 0
            
            if event.sym == tcod.event.K_UP or event.sym == tcod.event.K_k:
                dy = -1
            elif event.sym == tcod.event.K_DOWN or event.sym == tcod.event.K_j:
                dy = 1
            elif event.sym == tcod.event.K_LEFT or event.sym == tcod.event.K_h:
                dx = -1
            elif event.sym == tcod.event.K_RIGHT or event.sym == tcod.event.K_l:
                dx = 1
            elif event.sym == tcod.event.K_y:  # Diagonal: up-left
                dx, dy = -1, -1
            elif event.sym == tcod.event.K_u:  # Diagonal: up-right
                dx, dy = 1, -1
            elif event.sym == tcod.event.K_b:  # Diagonal: down-left
                dx, dy = -1, 1
            elif event.sym == tcod.event.K_n:  # Diagonal: down-right
                dx, dy = 1, 1
            elif event.sym == tcod.event.K_ESCAPE:
                self.running = False
                return
            elif event.sym == tcod.event.K_r:  # Regenerate world
                self.initialize()
                return
                
            # Try to move the hero
            if dx != 0 or dy != 0:
                new_x = self.hero.x + dx
                new_y = self.hero.y + dy
                
                if self.generator.is_walkable(new_x, new_y):
                    self.hero.move(dx, dy)
    
    def render(self, console):
        """Render the game world."""
        console.clear()
        
        # Render terrain
        for (x, y), tile in self.terrain.items():
            console.print(x, y, tile.char, fg=tile.color)
        
        # Render hero
        console.print(
            self.hero.x, 
            self.hero.y, 
            self.hero.render_char(), 
            fg=self.hero.color
        )
        
        # Render UI
        self._render_ui(console)
    
    def _render_ui(self, console):
        """Render UI elements."""
        # Status bar at bottom
        hp_text = f"HP: {self.hero.hp}/{self.hero.max_hp}"
        pos_text = f"Pos: ({self.hero.x}, {self.hero.y})"
        help_text = "Arrow/hjkl:Move | r:Regen | ESC:Quit"
        
        console.print(0, self.screen_height - 2, "=" * self.screen_width, fg=(100, 100, 100))
        console.print(1, self.screen_height - 1, hp_text, fg=(255, 255, 255))
        console.print(20, self.screen_height - 1, pos_text, fg=(255, 255, 255))
        console.print(40, self.screen_height - 1, help_text, fg=(200, 200, 200))


def main():
    """Main entry point."""
    # Load the font
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    # Create the game
    game = Game()
    game.initialize()
    
    # Create the console and context
    with tcod.context.new(
        columns=game.screen_width,
        rows=game.screen_height,
        tileset=tileset,
        title=TITLE,
        vsync=True,
    ) as context:
        console = tcod.Console(game.screen_width, game.screen_height, order="F")
        
        # Main game loop
        while game.running:
            # Render
            game.render(console)
            context.present(console)
            
            # Handle events
            for event in tcod.event.wait():
                context.convert_event(event)
                game.handle_input(event)


if __name__ == "__main__":
    main()
