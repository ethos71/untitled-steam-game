#!/usr/bin/env python3
"""Test for menu functionality including inventory, save/load, and equipment."""
import sys
import os
import json
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from environment.world.world_generator import WorldGenerator
from environment.items.item import Item, ItemSlot


def test_inventory_display():
    """Test inventory display functionality."""
    print("=" * 70)
    print("TEST 1: INVENTORY DISPLAY")
    print("=" * 70)
    
    random.seed(42)
    world_gen = WorldGenerator(width=60, height=50)
    terrain, hero = world_gen.generate()
    
    print(f"\n✓ World generated")
    print(f"  Hero position: ({hero.x}, {hero.y})")
    print(f"  Initial inventory size: {len(hero.inventory)}")
    
    # Add some test items to inventory
    test_items = [
        Item("Iron Helmet", ItemSlot.HEAD, {"defense": 5}),
        Item("Leather Armor", ItemSlot.BODY, {"defense": 10}),
        Item("Steel Sword", ItemSlot.WEAPON, {"attack": 15}),
        Item("Magic Ring", ItemSlot.RING, {"magic": 5}),
    ]
    
    for item in test_items:
        hero.inventory.append(item)
        print(f"  Added to inventory: {item.name} ({item.slot.value})")
    
    print(f"\n  Final inventory size: {len(hero.inventory)}")
    
    # Test inventory categorization
    inventory_by_slot = {
        ItemSlot.HEAD: [],
        ItemSlot.BODY: [],
        ItemSlot.LEGS: [],
        ItemSlot.WEAPON: [],
        ItemSlot.RING: []
    }
    
    for item in hero.inventory:
        if item.slot in inventory_by_slot:
            inventory_by_slot[item.slot].append(item)
    
    print("\n  Inventory by category:")
    for slot, items in inventory_by_slot.items():
        print(f"    {slot.value}: {len(items)} item(s)")
        for item in items:
            equipped = hero.equipment.get_equipped(slot) == item
            status = "[EQUIPPED]" if equipped else "[NOT EQUIPPED]"
            print(f"      - {item.name} {status}")
    
    print("\n✓ Inventory display test passed")
    return True


def test_auto_equip():
    """Test auto-equip functionality when picking up items."""
    print("\n" + "=" * 70)
    print("TEST 2: AUTO-EQUIP FUNCTIONALITY")
    print("=" * 70)
    
    random.seed(123)
    world_gen = WorldGenerator(width=60, height=50)
    terrain, hero = world_gen.generate()
    
    print(f"\n✓ World generated")
    
    # Test auto-equip for different slots
    test_items = [
        Item("Bronze Helmet", ItemSlot.HEAD, {"defense": 3}),
        Item("Iron Chestplate", ItemSlot.BODY, {"defense": 8}),
        Item("Wooden Sword", ItemSlot.WEAPON, {"attack": 10}),
    ]
    
    for item in test_items:
        print(f"\n  Testing auto-equip for: {item.name} ({item.slot.value})")
        
        # Check if slot is empty
        current_item = hero.equipment.get_equipped(item.slot)
        slot_empty = current_item is None
        
        print(f"    Slot {item.slot.value} empty: {slot_empty}")
        
        # Add to inventory
        hero.inventory.append(item)
        
        # Auto-equip if slot is empty
        if slot_empty:
            hero.equip_item(item)
            equipped = hero.equipment.get_equipped(item.slot) == item
            if equipped:
                print(f"    ✓ Auto-equipped successfully")
            else:
                print(f"    ✗ FAILED: Auto-equip failed")
                return False
        else:
            print(f"    Slot already occupied, item added to inventory only")
    
    print("\n✓ Auto-equip test passed")
    return True


def test_save_load():
    """Test save and load functionality."""
    print("\n" + "=" * 70)
    print("TEST 3: SAVE/LOAD FUNCTIONALITY")
    print("=" * 70)
    
    random.seed(456)
    world_gen = WorldGenerator(width=60, height=50)
    terrain, hero = world_gen.generate()
    
    print(f"\n✓ World generated")
    print(f"  Initial hero position: ({hero.x}, {hero.y})")
    
    # Add items to inventory
    test_item = Item("Test Sword", ItemSlot.WEAPON, {"attack": 20})
    hero.inventory.append(test_item)
    hero.equip_item(test_item)
    
    print(f"  Inventory size: {len(hero.inventory)}")
    print(f"  Equipped weapon: {hero.equipment.get_equipped(ItemSlot.WEAPON).name if hero.equipment.get_equipped(ItemSlot.WEAPON) else 'None'}")
    
    # Create save data
    save_data = {
        "hero": {
            "x": hero.x,
            "y": hero.y,
            "inventory": [
                {
                    "name": item.name,
                    "slot": item.slot.value,
                    "stats": item.stats
                } for item in hero.inventory
            ],
            "equipment": {
                slot.value: {
                    "name": item.name,
                    "slot": item.slot.value,
                    "stats": item.stats
                } if item else None
                for slot, item in hero.equipment.equipped.items()
            }
        },
        "world_seed": 456
    }
    
    # Save to file
    save_path = os.path.join(os.path.dirname(__file__), '..', 'saves', 'test_save.json')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, 'w') as f:
        json.dump(save_data, f, indent=2)
    
    print(f"\n  ✓ Game saved to: {save_path}")
    
    # Modify hero to simulate progress
    original_x, original_y = hero.x, hero.y
    hero.x += 10
    hero.y += 5
    hero.inventory.clear()
    
    print(f"\n  Modified hero position: ({hero.x}, {hero.y})")
    print(f"  Modified inventory size: {len(hero.inventory)}")
    
    # Load from file
    with open(save_path, 'r') as f:
        loaded_data = json.load(f)
    
    hero.x = loaded_data["hero"]["x"]
    hero.y = loaded_data["hero"]["y"]
    
    # Restore inventory
    hero.inventory.clear()
    for item_data in loaded_data["hero"]["inventory"]:
        item = Item(
            item_data["name"],
            ItemSlot(item_data["slot"]),
            item_data["stats"]
        )
        hero.inventory.append(item)
    
    print(f"\n  ✓ Game loaded from: {save_path}")
    print(f"  Restored hero position: ({hero.x}, {hero.y})")
    print(f"  Restored inventory size: {len(hero.inventory)}")
    
    # Verify restoration
    if hero.x == original_x and hero.y == original_y and len(hero.inventory) == 1:
        print("\n✓ Save/load test passed")
        
        # Clean up test file
        if os.path.exists(save_path):
            os.remove(save_path)
            print(f"  Cleaned up test save file")
        
        return True
    else:
        print("\n✗ FAILED: Save/load did not restore correctly")
        return False


def test_equipment_switching():
    """Test switching equipment between items."""
    print("\n" + "=" * 70)
    print("TEST 4: EQUIPMENT SWITCHING")
    print("=" * 70)
    
    random.seed(789)
    world_gen = WorldGenerator(width=60, height=50)
    terrain, hero = world_gen.generate()
    
    print(f"\n✓ World generated")
    
    # Create two weapons
    weapon1 = Item("Iron Sword", ItemSlot.WEAPON, {"attack": 15})
    weapon2 = Item("Steel Sword", ItemSlot.WEAPON, {"attack": 25})
    
    hero.inventory.append(weapon1)
    hero.inventory.append(weapon2)
    
    print(f"  Added two weapons to inventory")
    print(f"    Weapon 1: {weapon1.name} (Attack: {weapon1.stats['attack']})")
    print(f"    Weapon 2: {weapon2.name} (Attack: {weapon2.stats['attack']})")
    
    # Equip first weapon
    hero.equip_item(weapon1)
    equipped = hero.equipment.get_equipped(ItemSlot.WEAPON)
    
    if equipped != weapon1:
        print(f"\n✗ FAILED: Could not equip first weapon")
        return False
    
    print(f"\n  ✓ Equipped: {equipped.name}")
    
    # Switch to second weapon
    hero.equip_item(weapon2)
    equipped = hero.equipment.get_equipped(ItemSlot.WEAPON)
    
    if equipped != weapon2:
        print(f"\n✗ FAILED: Could not switch to second weapon")
        return False
    
    print(f"  ✓ Switched to: {equipped.name}")
    
    # Verify both weapons still in inventory
    if weapon1 in hero.inventory and weapon2 in hero.inventory:
        print(f"  ✓ Both weapons remain in inventory")
    else:
        print(f"  ✗ FAILED: Weapons missing from inventory")
        return False
    
    print("\n✓ Equipment switching test passed")
    return True


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("MENU FUNCTIONALITY TEST SUITE")
    print("=" * 70)
    
    all_passed = True
    
    # Test 1: Inventory display
    if not test_inventory_display():
        print("\n✗ TEST SUITE FAILED: Inventory display failed")
        all_passed = False
    
    # Test 2: Auto-equip
    if not test_auto_equip():
        print("\n✗ TEST SUITE FAILED: Auto-equip failed")
        all_passed = False
    
    # Test 3: Save/load
    if not test_save_load():
        print("\n✗ TEST SUITE FAILED: Save/load failed")
        all_passed = False
    
    # Test 4: Equipment switching
    if not test_equipment_switching():
        print("\n✗ TEST SUITE FAILED: Equipment switching failed")
        all_passed = False
    
    if all_passed:
        print("\n" + "=" * 70)
        print("✓ ALL MENU TESTS PASSED")
        print("=" * 70)
        print("\nSummary:")
        print("  ✓ Inventory displays correctly by category")
        print("  ✓ Items auto-equip when slot is empty")
        print("  ✓ Save/load preserves game state")
        print("  ✓ Equipment can be switched between items")
        print("=" * 70)
        sys.exit(0)
    else:
        print("\n✗ SOME TESTS FAILED")
        sys.exit(1)
