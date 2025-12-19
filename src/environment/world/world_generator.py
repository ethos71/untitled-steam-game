"""World generator for creating random ASCII scenes."""
import random
import sys
import os
from collections import deque
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from assets.terrain import Tree, Rock, River, Grass, Bridge
from characters.hero.hero import Hero
from characters.hero.equipment import Equipment, EquipmentSlot, EquipmentStats

class WorldGenerator:
    """Generates a random world with terrain and a hero."""
    
    def __init__(self, width=80, height=50):
        self.width = width
        self.height = height
        self.terrain = {}
        self.hero = None
        self.chests = []
        
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
        
        # Ensure large landmasses (remove small islands)
        self._remove_small_islands()
        
        # Generate bridges to connect isolated landmasses
        self._generate_bridges()
        
        # Find a safe spawn location for the hero
        hero_x, hero_y = self._find_safe_spawn_location()
        
        self.hero = Hero(hero_x, hero_y)
        
        # Generate treasure chests (always accessible)
        self._generate_chests(num_chests=1)
        
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
    
    def _find_safe_spawn_location(self):
        """Find a safe spawn location with walkable tiles around it."""
        # Try center first
        center_x = self.width // 2
        center_y = self.height // 2
        
        if self._is_safe_spawn(center_x, center_y):
            return center_x, center_y
        
        # Try positions in expanding radius from center
        for radius in range(1, min(self.width, self.height) // 2):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if abs(dx) == radius or abs(dy) == radius:
                        x = center_x + dx
                        y = center_y + dy
                        if 0 <= x < self.width and 0 <= y < self.height:
                            if self._is_safe_spawn(x, y):
                                return x, y
        
        # Fallback: force clear a safe area at center
        self._clear_safe_area(center_x, center_y)
        return center_x, center_y
    
    def _is_safe_spawn(self, x, y):
        """Check if position has at least 3x3 walkable area."""
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                check_x, check_y = x + dx, y + dy
                if not self.is_walkable(check_x, check_y):
                    return False
        return True
    
    def _clear_safe_area(self, x, y):
        """Force clear a 3x3 walkable area around position."""
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                pos_x, pos_y = x + dx, y + dy
                if 0 <= pos_x < self.width and 0 <= pos_y < self.height:
                    self.terrain[(pos_x, pos_y)] = Grass(pos_x, pos_y)
    
    def _generate_chests(self, num_chests=1):
        """Generate treasure chests that are always accessible from hero position."""
        for _ in range(num_chests):
            max_attempts = 100
            chest_placed = False
            
            for attempt in range(max_attempts):
                # Try to place chest in a random location
                chest_x = random.randint(5, self.width - 5)
                chest_y = random.randint(5, self.height - 5)
                
                # Check if location is walkable
                if not self.is_walkable(chest_x, chest_y):
                    continue
                
                # Check if chest is reachable from hero position using BFS
                if self._is_reachable(self.hero.x, self.hero.y, chest_x, chest_y):
                    # Generate random item for chest
                    item = self._generate_random_item()
                    chest = {
                        'x': chest_x,
                        'y': chest_y,
                        'item': item,
                        'opened': False
                    }
                    self.chests.append(chest)
                    chest_placed = True
                    break
            
            if not chest_placed:
                # Fallback: place chest near hero if we couldn't find accessible spot
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    chest_x = self.hero.x + dx * 3
                    chest_y = self.hero.y + dy * 3
                    if self.is_walkable(chest_x, chest_y):
                        item = self._generate_random_item()
                        chest = {
                            'x': chest_x,
                            'y': chest_y,
                            'item': item,
                            'opened': False
                        }
                        self.chests.append(chest)
                        break
    
    def _is_reachable(self, start_x, start_y, end_x, end_y):
        """Check if end position is reachable from start using BFS pathfinding."""
        if start_x == end_x and start_y == end_y:
            return True
        
        visited = set()
        queue = deque([(start_x, start_y)])
        visited.add((start_x, start_y))
        
        while queue:
            x, y = queue.popleft()
            
            # Check all adjacent positions
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                
                if new_x == end_x and new_y == end_y:
                    return True
                
                if (new_x, new_y) not in visited and self.is_walkable(new_x, new_y):
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y))
                
                # Limit search to prevent infinite loops
                if len(visited) > 1000:
                    return False
        
        return False
    
    def _generate_random_item(self):
        """Generate a random equipment item."""
        items = [
            Equipment(
                name="Iron Helmet",
                slot=EquipmentSlot.HEAD,
                stats=EquipmentStats(defense=5, hp_bonus=10),
                description="A sturdy iron helmet"
            ),
            Equipment(
                name="Leather Armor",
                slot=EquipmentSlot.BODY,
                stats=EquipmentStats(defense=8, hp_bonus=15),
                description="Well-crafted leather armor"
            ),
            Equipment(
                name="Swift Boots",
                slot=EquipmentSlot.FEET,
                stats=EquipmentStats(speed=5, evasion=3),
                description="Boots that increase movement speed"
            ),
            Equipment(
                name="Ring of Strength",
                slot=EquipmentSlot.ACCESSORY_1,
                stats=EquipmentStats(attack=3, defense=2),
                description="A ring that enhances strength"
            ),
            Equipment(
                name="Iron Sword",
                slot=EquipmentSlot.WEAPON,
                stats=EquipmentStats(attack=10, accuracy=5),
                description="A reliable iron blade"
            ),
        ]
        
        return random.choice(items)
    
    def _remove_small_islands(self, min_size=20):
        """Remove small landmasses by flooding them with water."""
        # Find all landmasses using flood fill
        visited = set()
        landmasses = []
        
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in visited and self.is_walkable(x, y):
                    # Flood fill to find this landmass
                    landmass = self._flood_fill_landmass(x, y, visited)
                    if landmass:
                        landmasses.append(landmass)
        
        # Convert small landmasses to water
        for landmass in landmasses:
            if len(landmass) < min_size:
                for x, y in landmass:
                    self.terrain[(x, y)] = River(x, y)
    
    def _flood_fill_landmass(self, start_x, start_y, visited):
        """Flood fill to find all connected walkable tiles."""
        landmass = []
        queue = deque([(start_x, start_y)])
        visited.add((start_x, start_y))
        
        while queue:
            x, y = queue.popleft()
            landmass.append((x, y))
            
            # Check all adjacent positions
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                
                if (new_x, new_y) not in visited:
                    if 0 <= new_x < self.width and 0 <= new_y < self.height:
                        if self.is_walkable(new_x, new_y):
                            visited.add((new_x, new_y))
                            queue.append((new_x, new_y))
        
        return landmass
    
    def _generate_bridges(self):
        """Generate bridges to connect isolated landmasses."""
        # Find all landmasses
        visited = set()
        landmasses = []
        
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in visited and self.is_walkable(x, y):
                    landmass = self._flood_fill_landmass(x, y, visited)
                    if landmass:
                        landmasses.append(landmass)
        
        # If we have multiple landmasses, connect them
        if len(landmasses) > 1:
            # Sort by size (largest first)
            landmasses.sort(key=len, reverse=True)
            main_landmass = landmasses[0]
            
            # Connect each smaller landmass to the main one
            for i in range(1, len(landmasses)):
                self._build_bridge_between(main_landmass, landmasses[i])
    
    def _build_bridge_between(self, landmass1, landmass2):
        """Build a bridge between two landmasses."""
        # Find closest points between the two landmasses
        min_distance = float('inf')
        best_pair = None
        
        # Sample points to avoid checking every combination
        sample_size = min(50, len(landmass1), len(landmass2))
        sample1 = random.sample(landmass1, min(sample_size, len(landmass1)))
        sample2 = random.sample(landmass2, min(sample_size, len(landmass2)))
        
        for x1, y1 in sample1:
            for x2, y2 in sample2:
                distance = abs(x2 - x1) + abs(y2 - y1)
                if distance < min_distance:
                    min_distance = distance
                    best_pair = ((x1, y1), (x2, y2))
        
        if best_pair and min_distance < 30:  # Only bridge if not too far
            start, end = best_pair
            self._build_straight_bridge(start[0], start[1], end[0], end[1])
    
    def _build_straight_bridge(self, x1, y1, x2, y2):
        """Build a straight bridge between two points."""
        # Use A* style pathfinding to build bridge
        current_x, current_y = x1, y1
        
        while current_x != x2 or current_y != y2:
            # Move towards target
            if current_x < x2:
                current_x += 1
            elif current_x > x2:
                current_x -= 1
            elif current_y < y2:
                current_y += 1
            elif current_y > y2:
                current_y -= 1
            
            # Place bridge if over water, otherwise use grass
            if 0 <= current_x < self.width and 0 <= current_y < self.height:
                terrain = self.terrain.get((current_x, current_y))
                if isinstance(terrain, River):
                    self.terrain[(current_x, current_y)] = Bridge(current_x, current_y)
                elif not self.is_walkable(current_x, current_y):
                    # Clear obstacles
                    self.terrain[(current_x, current_y)] = Grass(current_x, current_y)


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
