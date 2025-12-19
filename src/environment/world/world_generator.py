"""World generator for creating random ASCII scenes."""
import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from assets.terrain import Tree, Rock, River, Grass
from characters.hero.hero import Hero

class WorldGenerator:
    """Generates a random world with terrain and a hero."""
    
    def __init__(self, width=80, height=50):
        self.width = width
        self.height = height
        self.terrain = {}
        self.hero = None
        
    def generate(self):
        """Generate a complete world scene."""
        # Fill with grass first
        self._generate_grass()
        
        # Generate rivers (1-3 rivers)
        num_rivers = random.randint(1, 3)
        for _ in range(num_rivers):
            self._generate_river()
        
        # Generate trees (scattered forest patches)
        self._generate_trees(density=0.15)
        
        # Generate rocks (scattered)
        self._generate_rocks(density=0.05)
        
        # Place hero at the center
        hero_x = self.width // 2
        hero_y = self.height // 2
        
        # Make sure hero isn't spawning on blocking terrain
        if (hero_x, hero_y) in self.terrain:
            if self.terrain[(hero_x, hero_y)].blocks_movement:
                del self.terrain[(hero_x, hero_y)]
                
        self.hero = Hero(hero_x, hero_y)
        
        return self.terrain, self.hero
    
    def _generate_grass(self):
        """Fill the world with grass."""
        for y in range(self.height):
            for x in range(self.width):
                self.terrain[(x, y)] = Grass(x, y)
    
    def _generate_river(self):
        """Generate a winding river across the map."""
        # Decide if river is vertical or horizontal
        is_vertical = random.choice([True, False])
        
        if is_vertical:
            # Start from top or bottom
            x = random.randint(5, self.width - 5)
            y_range = range(self.height) if random.random() > 0.5 else range(self.height - 1, -1, -1)
            
            for y in y_range:
                # River width (1-3 tiles)
                width = random.randint(1, 3)
                for w in range(width):
                    river_x = x + w - width // 2
                    if 0 <= river_x < self.width:
                        self.terrain[(river_x, y)] = River(river_x, y)
                
                # Random meandering
                if random.random() > 0.7:
                    x += random.choice([-1, 1])
                    x = max(2, min(self.width - 3, x))
        else:
            # Horizontal river
            y = random.randint(5, self.height - 5)
            x_range = range(self.width) if random.random() > 0.5 else range(self.width - 1, -1, -1)
            
            for x in x_range:
                # River width (1-3 tiles)
                width = random.randint(1, 3)
                for w in range(width):
                    river_y = y + w - width // 2
                    if 0 <= river_y < self.height:
                        self.terrain[(x, river_y)] = River(x, river_y)
                
                # Random meandering
                if random.random() > 0.7:
                    y += random.choice([-1, 1])
                    y = max(2, min(self.height - 3, y))
    
    def _generate_trees(self, density=0.15):
        """Generate tree clusters."""
        # Create several forest patches
        num_patches = random.randint(3, 7)
        
        for _ in range(num_patches):
            # Center of the patch
            center_x = random.randint(5, self.width - 5)
            center_y = random.randint(5, self.height - 5)
            patch_radius = random.randint(3, 8)
            
            # Place trees in a roughly circular pattern
            for y in range(max(0, center_y - patch_radius), min(self.height, center_y + patch_radius)):
                for x in range(max(0, center_x - patch_radius), min(self.width, center_x + patch_radius)):
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    
                    if distance < patch_radius and random.random() < density:
                        # Don't overwrite rivers
                        if (x, y) in self.terrain and not isinstance(self.terrain[(x, y)], River):
                            self.terrain[(x, y)] = Tree(x, y)
    
    def _generate_rocks(self, density=0.05):
        """Generate scattered rocks."""
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    # Don't overwrite rivers or trees
                    if (x, y) in self.terrain:
                        current = self.terrain[(x, y)]
                        if not isinstance(current, (River, Tree)):
                            self.terrain[(x, y)] = Rock(x, y)
    
    def get_terrain_at(self, x, y):
        """Get terrain at specific position."""
        return self.terrain.get((x, y))
    
    def is_walkable(self, x, y):
        """Check if position is walkable."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        
        terrain = self.terrain.get((x, y))
        return terrain is None or not terrain.blocks_movement


def main():
    """Test the world generator."""
    print("Generating ASCII roguelike world...")
    
    generator = WorldGenerator(width=80, height=40)
    terrain, hero = generator.generate()
    
    # Print the world
    print("\n" + "=" * 80)
    for y in range(generator.height):
        line = ""
        for x in range(generator.width):
            # Check if hero is at this position
            if hero.x == x and hero.y == y:
                line += hero.render_char()
            elif (x, y) in terrain:
                line += terrain[(x, y)].char
            else:
                line += " "
        print(line)
    print("=" * 80)
    
    print(f"\nHero spawned at: ({hero.x}, {hero.y})")
    print(f"World size: {generator.width}x{generator.height}")
    print(f"Total terrain objects: {len(terrain)}")
    
    # Count terrain types
    tree_count = sum(1 for t in terrain.values() if t.name == "tree")
    rock_count = sum(1 for t in terrain.values() if t.name == "rock")
    river_count = sum(1 for t in terrain.values() if t.name == "river")
    
    print(f"Trees: {tree_count}, Rocks: {rock_count}, River tiles: {river_count}")


if __name__ == "__main__":
    main()
