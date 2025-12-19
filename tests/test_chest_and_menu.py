"""
Test chest opening and menu inventory display
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame
from src.engine.game_nes import Game
import time

def test_chest_and_menu():
    """Test that chest opening adds items to inventory and displays in menu"""
    print("\n=== Testing Chest Opening and Menu Display ===\n")
    
    # Initialize pygame
    pygame.init()
    
    # Create game
    game = Game()
    
    # Import MenuState from same place as game
    from engine.menu import MenuState
    game.new_game()
    
    print(f"Hero starting position: {game.hero.x, game.hero.y}")
    print(f"Initial inventory: {game.menu.inventory}")
    print(f"Initial equipment: {game.menu.equipment_slots}")
    
    # Find chest position
    assert len(game.treasure) > 0, "No chests generated"
    chest = game.treasure[0]
    chest_pos = (chest['x'], chest['y'])
    print(f"\nChest found at: {chest_pos}")
    
    # Move hero next to chest
    game.hero.x, game.hero.y = chest['x'] - 1, chest['y']
    print(f"Moved hero next to chest at: {game.hero.x, game.hero.y}")
    
    # Open chest
    print("\nAttempting to open chest...")
    game.try_open_chest()
    
    print(f"\nAfter opening chest:")
    print(f"Inventory: {[item.name for item in game.menu.inventory]}")
    print(f"Equipment slots:")
    for slot, item in game.menu.equipment_slots.items():
        print(f"  {slot.value}: {item.name if item else 'Empty'}")
    
    # Verify item was added
    assert len(game.menu.inventory) > 0, "No items in inventory after opening chest"
    print(f"\n✓ Item added to inventory: {game.menu.inventory[0].name}")
    
    # Check if auto-equipped
    equipped_count = sum(1 for item in game.menu.equipment_slots.values() if item is not None)
    print(f"✓ {equipped_count} item(s) auto-equipped")
    
    # Open menu
    print("\nOpening menu...")
    game.menu.open()
    assert game.menu.is_open(), "Menu should be open"
    print(f"✓ Menu opened, state: {game.menu.state}")
    
    # Navigate to inventory
    print("\nNavigating to inventory...")
    game.menu._open_inventory()
    print(f"Menu state after _open_inventory: {game.menu.state}")
    print(f"Expected state: {MenuState.INVENTORY}")
    print(f"States equal: {game.menu.state == MenuState.INVENTORY}")
    assert game.menu.state == MenuState.INVENTORY, f"Should be in inventory state, got {game.menu.state}"
    print(f"✓ In inventory menu")
    
    # Check inventory menu items
    print(f"\nInventory menu items:")
    for i, menu_item in enumerate(game.menu.inventory_menu_items):
        print(f"  {i}: {menu_item.text} (enabled: {menu_item.enabled})")
    
    # Verify the item appears in menu
    item_names = [item.text for item in game.menu.inventory_menu_items]
    found_item = any(game.menu.inventory[0].name in text for text in item_names)
    assert found_item, f"Item '{game.menu.inventory[0].name}' not found in menu display"
    print(f"\n✓ Item appears in inventory menu")
    
    # Check for EQUIPPED tag
    equipped_text = [text for text in item_names if "[EQUIPPED]" in text]
    if equipped_text:
        print(f"✓ Found equipped items in menu: {equipped_text}")
    
    pygame.quit()
    print("\n=== TEST PASSED ===\n")
    return True

if __name__ == "__main__":
    try:
        test_chest_and_menu()
    except Exception as e:
        print(f"\n!!! TEST FAILED !!!")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
