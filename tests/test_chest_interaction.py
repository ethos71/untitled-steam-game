"""
Test chest interaction and collision system
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from engine.game_state import GameState
from engine.collision import CollisionSystem
from environment.world.world_generator import WorldGenerator

def test_chest_interaction():
    """Test that chests can be opened and items are received"""
    print("Testing chest interaction...")
    
    # Create game state
    grid_width = 25
    grid_height = 19
    world_gen = WorldGenerator(width=50, height=38)
    game_state = GameState(grid_width, grid_height)
    game_state.collision = CollisionSystem(world_gen)
    
    # Generate a world
    world, hero = world_gen.generate()
    game_state.set_world(world, world_gen.width, world_gen.height)
    game_state.set_hero_position(hero.x, hero.y)
    
    # Add chests from world generator
    for chest_data in world_gen.chests:
        game_state.add_chest(chest_data['x'], chest_data['y'], chest_data['item'])
    
    # Update collision system with world data
    game_state.collision.set_world(world, game_state.chests)
    
    print(f"World generated with {len(game_state.chests)} chest(s)")
    print(f"Hero at ({game_state.hero_x}, {game_state.hero_y})")
    
    if game_state.chests:
        chest = game_state.chests[0]
        print(f"Chest at ({chest['x']}, {chest['y']}), opened: {chest['opened']}")
        
        # Test chest is blocking before opened
        is_blocked = game_state.collision.is_blocked(chest['x'], chest['y'])
        print(f"Chest position blocked: {is_blocked}")
        assert is_blocked, "Chest should block movement before opening"
        
        # Open chest
        item = game_state.open_chest(chest)
        print(f"Opened chest, received: {item.name if item else 'nothing'}")
        assert item is not None, "Should receive an item from chest"
        assert chest['opened'], "Chest should be marked as opened"
        
        # Test chest still blocks after opening (chests don't disappear)
        is_blocked_after = game_state.collision.is_blocked(chest['x'], chest['y'])
        print(f"Chest position blocked after opening: {is_blocked_after}")
        
        # Check item was added to inventory
        print(f"Inventory: {game_state.inventory}")
        
        # Check if item was auto-equipped
        item_equipped = False
        for slot, equipped_item in game_state.inventory.items():
            if equipped_item and slot != 'items':
                item_equipped = True
                print(f"Item equipped in {slot}: {equipped_item}")
        
        if not item_equipped and game_state.inventory['items']:
            print(f"Item in items list: {game_state.inventory['items']}")
        
        print("✓ Chest interaction test passed!")
        return True
    else:
        print("✗ No chests generated!")
        return False

def test_chest_persistence():
    """Test that chests remain in the chests list after opening"""
    print("\nTesting chest persistence...")
    
    grid_width = 25
    grid_height = 19
    world_gen = WorldGenerator(width=50, height=38)
    game_state = GameState(grid_width, grid_height)
    game_state.collision = CollisionSystem(world_gen)
    
    # Generate world
    world, hero = world_gen.generate()
    game_state.set_world(world, world_gen.width, world_gen.height)
    game_state.set_hero_position(hero.x, hero.y)
    
    # Add chests
    for chest_data in world_gen.chests:
        game_state.add_chest(chest_data['x'], chest_data['y'], chest_data['item'])
    
    # Update collision system
    game_state.collision.set_world(world, game_state.chests)
    
    initial_chest_count = len(game_state.chests)
    print(f"Initial chest count: {initial_chest_count}")
    
    if game_state.chests:
        chest = game_state.chests[0]
        game_state.open_chest(chest)
        
        final_chest_count = len(game_state.chests)
        print(f"Final chest count: {final_chest_count}")
        
        assert final_chest_count == initial_chest_count, "Chests should not be removed from list"
        assert chest in game_state.chests, "Opened chest should still be in list"
        
        print("✓ Chest persistence test passed!")
        return True
    
    return False

if __name__ == "__main__":
    try:
        result1 = test_chest_interaction()
        result2 = test_chest_persistence()
        
        if result1 and result2:
            print("\n✓ All chest tests passed!")
            sys.exit(0)
        else:
            print("\n✗ Some tests failed")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
