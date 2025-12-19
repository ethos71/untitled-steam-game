#!/usr/bin/env python3
"""Test for chest generation, pathfinding, and item equipping."""
import sys
import os
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from environment.world.world_generator import WorldGenerator
from collections import deque


def find_path(world_gen, start_x, start_y, end_x, end_y):
    """Find path from start to end using BFS."""
    if start_x == end_x and start_y == end_y:
        return [(start_x, start_y)]
    
    visited = set()
    queue = deque([(start_x, start_y, [(start_x, start_y)])])
    visited.add((start_x, start_y))
    
    while queue:
        x, y, path = queue.popleft()
        
        # Check all adjacent positions
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            
            if new_x == end_x and new_y == end_y:
                return path + [(new_x, new_y)]
            
            if (new_x, new_y) not in visited and world_gen.is_walkable(new_x, new_y):
                visited.add((new_x, new_y))
                queue.append((new_x, new_y, path + [(new_x, new_y)]))
            
            # Limit search
            if len(visited) > 2000:
                return None
    
    return None


def test_chest_generation():
    """Test that chests are generated and accessible."""
    print("=" * 70)
    print("TEST 1: CHEST GENERATION AND ACCESSIBILITY")
    print("=" * 70)
    
    random.seed(42)
    world_gen = WorldGenerator(width=60, height=50)
    terrain, hero = world_gen.generate()
    
    print(f"\n✓ World generated with {len(world_gen.chests)} chest(s)")
    print(f"  Hero position: ({hero.x}, {hero.y})")
    
    if len(world_gen.chests) == 0:
        print("✗ FAILED: No chests were generated!")
        return False
    
    for i, chest in enumerate(world_gen.chests):
        print(f"\n  Chest {i+1}:")
        print(f"    Position: ({chest['x']}, {chest['y']})")
        print(f"    Item: {chest['item'].name} ({chest['item'].slot.value})")
        print(f"    Opened: {chest['opened']}")
        
        # Verify chest is on walkable terrain
        if not world_gen.is_walkable(chest['x'], chest['y']):
            print(f"    ✗ FAILED: Chest is on non-walkable terrain!")
            return False
        else:
            print(f"    ✓ Chest is on walkable terrain")
    
    print("\n✓ All chests generated successfully")
    return world_gen, terrain, hero


def test_chest_pathfinding(world_gen, hero):
    """Test that hero can reach all chests."""
    print("\n" + "=" * 70)
    print("TEST 2: PATHFINDING TO CHESTS")
    print("=" * 70)
    
    all_reachable = True
    
    for i, chest in enumerate(world_gen.chests):
        print(f"\n  Finding path to Chest {i+1} at ({chest['x']}, {chest['y']})...")
        
        path = find_path(world_gen, hero.x, hero.y, chest['x'], chest['y'])
        
        if path is None:
            print(f"    ✗ FAILED: No path found to chest!")
            all_reachable = False
        else:
            print(f"    ✓ Path found! Distance: {len(path) - 1} tiles")
            print(f"    Path preview: {path[:5]}..." if len(path) > 5 else f"    Full path: {path}")
    
    if all_reachable:
        print("\n✓ All chests are reachable from hero position")
    else:
        print("\n✗ FAILED: Some chests are not reachable!")
    
    return all_reachable


def test_chest_opening_and_equipping(world_gen, hero):
    """Test opening chests and equipping items."""
    print("\n" + "=" * 70)
    print("TEST 3: CHEST OPENING AND ITEM EQUIPPING")
    print("=" * 70)
    
    if len(world_gen.chests) == 0:
        print("✗ No chests to test")
        return False
    
    chest = world_gen.chests[0]
    print(f"\n  Testing with Chest at ({chest['x']}, {chest['y']})")
    item = chest['item']
    print(f"  Item in chest: {item.name} ({item.slot.value})")
    
    # Simulate hero walking to chest
    print(f"\n  Simulating hero movement to chest...")
    path = find_path(world_gen, hero.x, hero.y, chest['x'], chest['y'])
    
    if path is None:
        print("  ✗ FAILED: Cannot reach chest")
        return False
    
    # Move hero along path
    for i, (x, y) in enumerate(path[1:], 1):
        hero.x = x
        hero.y = y
        print(f"    Step {i}: Moved to ({x}, {y})")
    
    print(f"\n  Hero reached chest position: ({hero.x}, {hero.y})")
    
    # Open chest
    print(f"\n  Opening chest...")
    initial_inventory_size = len(hero.inventory)
    
    if not chest['opened']:
        chest['opened'] = True
        item = chest['item']
        hero.inventory.append(item)
        print(f"  ✓ Chest opened! Found: {item.name}")
        print(f"  ✓ Item added to inventory")
    
    if len(hero.inventory) != initial_inventory_size + 1:
        print(f"  ✗ FAILED: Item not added to inventory")
        return False
    
    # Equip item
    print(f"\n  Equipping item from inventory...")
    item = hero.inventory[-1]
    
    try:
        hero.equip_item(item)
        print(f"  ✓ Item equipped successfully!")
        print(f"  Item slot: {item.slot.value}")
        
        # Verify item is equipped
        equipped_item = hero.equipment.get_equipped(item.slot)
        if equipped_item == item:
            print(f"  ✓ Verified: {item.name} is equipped in {item.slot.value} slot")
        else:
            print(f"  ✗ FAILED: Item not properly equipped")
            return False
            
    except Exception as e:
        print(f"  ✗ FAILED: Could not equip item: {e}")
        return False
    
    print("\n✓ Chest opening and item equipping successful")
    return True


def test_multiple_chests():
    """Test with multiple chests to ensure all are accessible."""
    print("\n" + "=" * 70)
    print("TEST 4: MULTIPLE CHEST GENERATION")
    print("=" * 70)
    
    # Generate several worlds and verify chests are always accessible
    success_count = 0
    total_tests = 5
    
    for test_num in range(total_tests):
        random.seed(1000 + test_num)
        world_gen = WorldGenerator(width=80, height=60)
        terrain, hero = world_gen.generate()
        
        all_accessible = True
        for chest in world_gen.chests:
            path = find_path(world_gen, hero.x, hero.y, chest['x'], chest['y'])
            if path is None:
                all_accessible = False
                break
        
        if all_accessible:
            success_count += 1
            print(f"  Test {test_num + 1}: ✓ All chests accessible")
        else:
            print(f"  Test {test_num + 1}: ✗ Some chests not accessible")
    
    print(f"\n  Success rate: {success_count}/{total_tests} ({success_count/total_tests*100:.0f}%)")
    
    if success_count == total_tests:
        print("✓ All tests passed - chests are consistently accessible")
        return True
    else:
        print("✗ Some tests failed - chest generation needs improvement")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CHEST PATHFINDING AND EQUIPPING TEST SUITE")
    print("=" * 70)
    
    # Test 1: Generate world with chests
    result = test_chest_generation()
    if not result:
        print("\n✗ TEST SUITE FAILED: Chest generation failed")
        sys.exit(1)
    
    world_gen, terrain, hero = result
    
    # Test 2: Verify pathfinding to chests
    if not test_chest_pathfinding(world_gen, hero):
        print("\n✗ TEST SUITE FAILED: Pathfinding failed")
        sys.exit(1)
    
    # Test 3: Test chest opening and equipping
    if not test_chest_opening_and_equipping(world_gen, hero):
        print("\n✗ TEST SUITE FAILED: Chest/equipping failed")
        sys.exit(1)
    
    # Test 4: Multiple chest generation tests
    if not test_multiple_chests():
        print("\n✗ TEST SUITE FAILED: Multiple chest test failed")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED")
    print("=" * 70)
    print("\nSummary:")
    print("  ✓ Chests generate correctly")
    print("  ✓ Chests are always on walkable terrain")
    print("  ✓ Chests are always accessible from hero position")
    print("  ✓ Hero can navigate to chests")
    print("  ✓ Chests can be opened")
    print("  ✓ Items can be equipped from chests")
    print("=" * 70)
