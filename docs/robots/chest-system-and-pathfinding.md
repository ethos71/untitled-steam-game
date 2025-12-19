# Treasure Chest System and Pathfinding

## Overview
The treasure chest system ensures that every chest generated in the game world is accessible to the player using pathfinding verification. This prevents frustrating scenarios where chests spawn behind impassable terrain.

## Key Features

### 1. Guaranteed Accessibility
- **BFS Pathfinding**: Each chest location is verified using Breadth-First Search (BFS) to ensure a valid path exists from the hero's spawn point
- **Fallback Placement**: If pathfinding fails after 100 attempts, chest is placed near the hero in a guaranteed accessible location
- **No Blocked Chests**: The system will never generate a chest that cannot be reached

### 2. Chest Generation Process
1. **Random Placement**: Attempts to place chest at random walkable location
2. **Walkability Check**: Verifies the chest position is on traversable terrain
3. **Pathfinding Verification**: Uses BFS to confirm path exists from hero to chest
4. **Item Generation**: Creates random equipment item for the chest
5. **Fallback**: If placement fails, uses nearby guaranteed-accessible positions

### 3. Chest Interaction
- **Auto-Open**: Walking onto a chest tile automatically opens it
- **Inventory**: Opened items are added to hero's inventory
- **Equipment**: Players can equip items from inventory via menu system
- **Visual Feedback**: Chests change color when opened (brown → dark brown)

## Technical Implementation

### WorldGenerator Class
Located in: `src/environment/world/world_generator.py`

```python
def _generate_chests(self, num_chests=1):
    """Generate treasure chests that are always accessible from hero position."""
    # Uses pathfinding to verify each chest is reachable
    
def _is_reachable(self, start_x, start_y, end_x, end_y):
    """Check if end position is reachable from start using BFS pathfinding."""
    # BFS algorithm with visited set and queue
    # Limit: 1000 tiles searched to prevent infinite loops
```

### Game Class Integration
Located in: `src/engine/game_simple.py`

```python
def _check_chest_interaction(self):
    """Check if hero is on a chest and open it."""
    # Called after every hero movement
    # Adds item to inventory when chest is opened
```

### Equipment System
Located in: `src/characters/hero/equipment.py`

- **7 Equipment Slots**: Head, Body, Hands, Legs, Feet, Weapon, Shield, Accessory 1, Accessory 2
- **Stat Bonuses**: Attack, Defense, Magic Attack/Defense, Speed, HP/MP bonuses, Evasion, Accuracy
- **Equip Manager**: Handles equipment swapping and stat calculation

### Hero Class
Located in: `src/characters/hero/hero.py`

```python
def equip_item(self, equipment):
    """Equip an item from inventory."""
    # Handles equipment swapping
    # Old equipment returns to inventory
```

## Testing

### Test Suite: test_chest_pathfinding.py
Located in: `tests/test_chest_pathfinding.py`

**Test Coverage:**
1. **Chest Generation**: Verifies chests spawn on walkable terrain
2. **Pathfinding**: Confirms paths exist from hero to all chests
3. **Chest Opening**: Tests chest interaction and inventory addition
4. **Item Equipping**: Validates equipment system integration
5. **Multiple Worlds**: Tests consistency across random world generations

**Run Tests:**
```bash
python3 tests/test_chest_pathfinding.py
```

**Expected Output:**
```
======================================================================
✓ ALL TESTS PASSED
======================================================================

Summary:
  ✓ Chests generate correctly
  ✓ Chests are always on walkable terrain
  ✓ Chests are always accessible from hero position
  ✓ Hero can navigate to chests
  ✓ Chests can be opened
  ✓ Items can be equipped from chests
======================================================================
```

## Item Generation

### Random Equipment
Chests generate random equipment with varied stats:

- **Iron Helmet**: Head slot, +5 Defense, +10 HP
- **Leather Armor**: Body slot, +8 Defense, +15 HP
- **Swift Boots**: Feet slot, +5 Speed, +3 Evasion
- **Ring of Strength**: Accessory slot, +3 Attack, +2 Defense
- **Iron Sword**: Weapon slot, +10 Attack, +5 Accuracy

### Future Enhancements
- Rarity system integration (Common, Uncommon, Rare, Epic, Legendary)
- Shell-level scaling (deeper shells = better loot)
- Item prefixes/suffixes for variety
- Set bonuses for matching equipment
- Consumables (potions, elixirs)

## Algorithm Details

### BFS Pathfinding
```
1. Start at hero position
2. Add position to queue and visited set
3. While queue not empty:
   a. Pop position from queue
   b. Check all 4 adjacent tiles (up, down, left, right)
   c. If adjacent tile is chest position: SUCCESS
   d. If adjacent tile is walkable and not visited:
      - Add to visited set
      - Add to queue
   e. If visited > 1000 tiles: FAIL (prevent infinite loop)
4. If queue empty: FAIL (no path exists)
```

### Walkability Rules
- **Walkable**: Grass tiles, empty spaces
- **Blocked**: Trees, Rocks, Rivers, out of bounds

## Visual Design

### Chest Sprites
- **Closed Chest**: Brown rectangle (RGB: 139, 69, 19)
- **Opened Chest**: Dark brown rectangle (RGB: 100, 50, 10)
- **Size**: 16x16 pixels (matching tile size)
- **Position**: Centered in tile grid

### NES Palette Colors
Used for all game elements:
- Grass: (0, 168, 0)
- Tree: (0, 88, 0)
- Rock: (124, 124, 124)
- Water: (0, 120, 248)
- Hero: (252, 160, 68)

## Performance Considerations

### Optimization
- **Search Limit**: BFS limited to 1000 tiles to prevent lag
- **Single Chest**: Currently one chest per world (fast generation)
- **Caching**: Terrain walkability pre-calculated during generation
- **Early Exit**: Pathfinding stops immediately when path found

### Future Optimizations
- A* pathfinding for faster searches
- Pre-computed accessibility maps
- Chunk-based generation for large worlds
- Multiple chests with distributed placement

## Game Design Notes

### Player Experience
- **Fair Gameplay**: No unreachable rewards = no player frustration
- **Exploration**: Encourages movement through world to find chests
- **Progression**: Equipment system provides tangible power upgrades
- **Visual Feedback**: Clear indication of chest status (opened/closed)

### Balance Considerations
- **One Chest Per Shell**: Keeps item acquisition meaningful
- **Random Items**: Adds replayability and variety
- **Guaranteed Access**: Respects player time investment
- **Equipment Slots**: Limited slots force strategic choices

## Related Systems

### Equipment System
See: `src/characters/hero/equipment.py`
- 9 equipment slots total
- Stat bonuses stack additively
- Equipment swapping returns old items to inventory

### Inventory System
See: `src/characters/hero/hero.py`
- Simple list-based inventory
- Items stored as Equipment objects
- No weight/space limits (currently)

### World Generation
See: `src/environment/world/world_generator.py`
- Procedural terrain generation
- Rivers, trees, rocks, grass
- Hero spawns at center
- Chests placed with accessibility checks

## Troubleshooting

### Chest Not Opening
- Verify hero position matches chest position exactly
- Check that chest['opened'] is False
- Ensure _check_chest_interaction() called after movement

### Pathfinding Fails
- Increase max_attempts from 100
- Reduce world size or obstacle density
- Check fallback placement logic
- Verify BFS search limit (1000 tiles)

### Item Not Equipping
- Confirm item in hero.inventory
- Check equipment slot availability
- Verify Equipment object has correct slot attribute

## Future Development

### Planned Features
1. **Multiple Chests**: Support for N chests per shell
2. **Rarity Tiers**: Integrate treasure.py rarity system
3. **Shell Scaling**: Loot quality increases in deeper shells
4. **Mini-map**: Show chest locations after discovery
5. **Chest Varieties**: Locked chests, mimics, hidden chests
6. **Loot Tables**: Shell-specific item pools
7. **Consumables**: Potions and elixirs in chests

### Integration Points
- Menu system for inventory/equipment UI
- Save system for persistent inventory
- Multiplayer chest synchronization
- Achievement system (chests opened, rare items found)

## References

- **BFS Algorithm**: [Wikipedia - Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search)
- **Equipment Systems**: Final Fantasy, Diablo, Dark Souls
- **Procedural Generation**: Spelunky, Binding of Isaac, Enter the Gungeon
