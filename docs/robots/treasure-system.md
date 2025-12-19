# Treasure Chest System Documentation

## Overview
Each shell contains one treasure chest with randomly generated loot. The quality and power of items scale with the shell level.

## Finding Treasure
- **Visual**: Treasure chests appear as golden boxes (□)
- **Location**: One chest spawns per shell in a random walkable location
- **Interaction**: Press **SPACE** when standing adjacent to a chest to open it

## Chest States
- **Closed**: Golden box (□) - Contains unopened loot
- **Opened**: Different appearance (■) - Already looted, cannot open again

## Item Generation

### Rarity Tiers
Items are generated with one of five rarity levels:

1. **Common** (White)
   - Base stats
   - Most frequent drop

2. **Uncommon** (Green)
   - 1.5x stat multiplier
   - Moderate drop rate

3. **Rare** (Blue)
   - 2x stat multiplier
   - Less common

4. **Epic** (Purple)
   - 3x stat multiplier
   - Rare find

5. **Legendary** (Orange/Gold)
   - 5x stat multiplier
   - Extremely rare

### Rarity Distribution
Rarity chances increase with shell level:
- **Shell 1**: 60% Common, 25% Uncommon, 10% Rare, 4% Epic, 1% Legendary
- **Shell 5**: 35% Common, 35% Uncommon, 20% Rare, 9% Epic, 3% Legendary
- **Shell 9**: 10% Common, 40% Uncommon, 30% Rare, 15% Epic, 5% Legendary

### Item Types

#### Weapons
- Types: Sword, Axe, Spear, Dagger, Staff, Bow, Hammer, Mace, Katana, Scythe
- Stats: Attack power, Accuracy
- Slot: Weapon 1 or Weapon 2

#### Armor
- Types: Helmet, Chestplate, Boots, Gauntlets, Shield
- Stats: Defense, HP bonus
- Slots: Head, Chest, Feet

#### Accessories
- Types: Ring, Amulet, Pendant, Bracelet, Talisman
- Stats: Magic power, MP bonus
- Slots: Ring 1, Ring 2

#### Consumables
- Types: Potion, Elixir, Remedy, Tonic, Ether
- Stats: HP restore, MP restore
- Usage: One-time use items

## Item Scaling
Item power scales with shell level:
```
Base Power = (5 + Shell Level × 3) × Rarity Multiplier
```

### Examples
- **Shell 1 Common Sword**: 8 Attack
- **Shell 1 Legendary Sword**: 40 Attack
- **Shell 5 Rare Chestplate**: 28 Defense, 56 HP
- **Shell 9 Epic Ring**: 72 Magic Power, 216 MP

## Technical Details

### File Structure
- `src/environment/items/treasure.py` - Treasure chest and item generation

### Key Classes
- `TreasureChest` - Individual chest with position and loot
- `Item` - Generated item with stats
- `ItemType` - Enum for item categories
- `ItemRarity` - Enum for rarity tiers

### Key Functions
- `place_treasure_chest()` - Spawns chest in valid location
- `TreasureChest._generate_item()` - Creates random item
- `TreasureChest.open()` - Opens chest and returns item

## Game Integration
1. World generator places hero and terrain
2. One treasure chest spawns in random walkable tile
3. Player explores and finds chest
4. Player presses SPACE near chest
5. Chest opens, item is generated and displayed
6. Item can be equipped from inventory (future feature)

## Visual Feedback
When opening a chest:
- On-screen message displays item name
- Console prints detailed item information
- Message persists for 3 seconds
- Chest changes to "opened" appearance

## Future Enhancements
- Multiple chests per shell (scaling with shell size)
- Locked chests requiring keys
- Trapped chests with challenges
- Chest quality indicators (silver, gold, platinum)
- Animated opening sequence
- Item preview before taking
- Choice between multiple items
