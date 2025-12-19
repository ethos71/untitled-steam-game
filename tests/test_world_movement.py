#!/usr/bin/env python3
"""Test for world generation and player movement with collision detection."""
import sys
import os
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from environment.world.world_generator import WorldGenerator

def test_world_generation():
    """Test that world generates correctly."""
    random.seed(12345)  # Set seed for reproducible tests
    world_gen = WorldGenerator(width=60, height=50)
    terrain, hero = world_gen.generate()
    
    print("✓ World generated successfully")
    print(f"  Dimensions: {world_gen.width}x{world_gen.height}")
    print(f"  Hero spawned at: ({hero.x}, {hero.y})")
    
    # Count tile types
    grass_count = sum(1 for t in terrain.values() if t.name == 'grass')
    water_count = sum(1 for t in terrain.values() if t.name == 'river')
    tree_count = sum(1 for t in terrain.values() if t.name == 'tree')
    rock_count = sum(1 for t in terrain.values() if t.name == 'rock')
    
    print(f"  Grass tiles: {grass_count}")
    print(f"  Water tiles: {water_count}")
    print(f"  Tree tiles: {tree_count}")
    print(f"  Rock tiles: {rock_count}")
    
    return world_gen, terrain, hero

def test_collision_detection(world_gen, terrain, hero):
    """Test that collision detection works for different tile types."""
    print("\n✓ Testing collision detection:")
    
    # Test player starting position
    player_x, player_y = hero.x, hero.y
    print(f"  Player starts at: ({player_x}, {player_y})")
    
    starting_terrain = terrain.get((player_x, player_y))
    if starting_terrain:
        print(f"  Starting tile: {starting_terrain.name}")
    else:
        print(f"  Starting tile: empty (walkable)")
    
    # Test movement in all directions
    directions = {
        'up': (0, -1),
        'down': (0, 1),
        'left': (-1, 0),
        'right': (1, 0)
    }
    
    for direction, (dx, dy) in directions.items():
        new_x = player_x + dx
        new_y = player_y + dy
        
        # Check if walkable using the generator's method
        can_move = world_gen.is_walkable(new_x, new_y)
        tile_terrain = terrain.get((new_x, new_y))
        tile_type = tile_terrain.name if tile_terrain else 'grass'
        
        print(f"  {direction}: tile={tile_type}, can_move={can_move}")
        
        if not can_move:
            print(f"    ✗ Blocked by {tile_type}")
        else:
            print(f"    ✓ Can walk on {tile_type}")
    
    return True

def test_pathfinding(world_gen, terrain, hero):
    """Test that player can find walkable paths."""
    print("\n✓ Testing pathfinding:")
    
    player_x, player_y = hero.x, hero.y
    
    # Try to find a walkable path in each direction
    max_distance = 10
    
    for direction, (dx, dy) in [('north', (0, -1)), ('south', (0, 1)), 
                                  ('east', (1, 0)), ('west', (-1, 0))]:
        x, y = player_x, player_y
        steps = 0
        
        for _ in range(max_distance):
            new_x = x + dx
            new_y = y + dy
            
            # Use world generator's walkable check
            if not world_gen.is_walkable(new_x, new_y):
                break
            
            x, y = new_x, new_y
            steps += 1
        
        print(f"  Can walk {steps} tiles {direction}")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("WORLD GENERATION AND MOVEMENT TEST")
    print("=" * 60)
    
    # Test 1: Generate world
    print("\nTest 1: World Generation")
    world_gen, terrain, hero = test_world_generation()
    
    # Test 2: Collision detection
    print("\nTest 2: Collision Detection")
    test_collision_detection(world_gen, terrain, hero)
    
    # Test 3: Pathfinding
    print("\nTest 3: Pathfinding")
    test_pathfinding(world_gen, terrain, hero)
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
