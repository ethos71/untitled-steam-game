# DLC Directory

This directory contains all downloadable content (DLC) for the NES-style roguelike.

## Purpose

Extra **paid content** that extends the base game with new features, content, and experiences.

## Structure

```
dlc/
├── expansion_1/          # First major expansion
│   ├── content/          # New levels, enemies, items
│   ├── assets/           # Graphics and sounds
│   └── README.md         # Expansion details
├── expansion_2/          # Second major expansion
├── character_pack_1/     # New playable characters
├── dungeon_pack_1/       # New dungeons and areas
├── cosmetic_pack_1/      # Skins and visual upgrades
└── README.md             # This file
```

---

## DLC vs Base Game

### Base Game
- Core story and gameplay
- Main villain encounter
- Essential features
- **Free or initial purchase price**

### DLC (Downloadable Content)
- Optional expansions
- Extra content and features
- New stories/characters/areas
- **Separate paid purchases**

---

## DLC Types

### 1. Major Expansions ($9.99 - $19.99)
- New story chapters
- New areas/dungeons (10+ hours)
- New bosses and villains
- 20+ new items/weapons

### 2. Content Packs ($4.99 - $9.99)
- New character classes
- New dungeon types
- New enemy types
- 10+ new items

### 3. Cosmetic Packs ($1.99 - $4.99)
- Character skins
- Weapon skins
- Tile sets/themes
- Sound packs

---

## Planned DLC

### Expansion 1: "The Frozen Wastes"
**Price**: $9.99  
**Release**: 3-6 months after base game

**Content**:
- New Area: Frozen Wastes (15+ floors)
- New Boss: Ice Queen
- New Enemies: 10 ice creatures
- New Items: 25 ice-themed items
- New Mechanic: Freezing status

### Expansion 2: "Shadow Realm"
**Price**: $12.99  
**Release**: 6-9 months after base game

**Content**:
- New Area: Shadow Realm (20+ floors)
- New Villain: Shadow King
- New Enemies: 15 shadow creatures
- New Items: 30 shadow-themed items
- Alternate ending path

### Character Pack 1: "Heroes of Legend"
**Price**: $4.99  
**Release**: 1-2 months after base game

**Content**:
- 3 new playable characters
- Warrior (high HP, melee)
- Mage (magic attacks)
- Rogue (stealth, speed)

---

## DLC Management

### Steam Integration

```python
class DLCManager:
    """Manages DLC detection and loading."""
    
    def check_owned_dlc(self):
        """Check which DLC player owns via Steam API."""
        pass
    
    def load_dlc(self, dlc_name):
        """Load DLC content into game."""
        pass
```

### Content Gating

```python
def check_dlc_access(area_name):
    """Prevent access without DLC ownership."""
    if not dlc_manager.owns_dlc(area_name):
        show_purchase_prompt()
        return False
    return True
```

---

## Season Pass

**Price**: $24.99 (save $10)

**Includes**:
- Expansion 1 ($9.99)
- Expansion 2 ($12.99)
- Character Pack 1 ($4.99)
- Dungeon Pack 1 ($5.99)
- **Total Value**: $34.96

---

## DLC Best Practices

1. **No Pay-to-Win** - DLC doesn't make game easier
2. **Substantial Content** - Worth the price
3. **Optional** - Base game is complete
4. **Value** - Hours of content per dollar
5. **Integration** - Feels natural

---

## Development Priority

### Phase 1: Base Game (PRIORITY)
Complete the base game first before any DLC

### Phase 2: Post-Launch DLC
After base game is released and successful

---

## Revenue Projection

### Conservative (30% attach rate)
- Base game: 10,000 sales @ $19.99 = $199,900
- DLC: 3,000 sales @ avg $8 = $24,000
- **Year 1 Total**: ~$223,900

### Optimistic (50% attach rate)
- Base game: 50,000 sales @ $19.99 = $999,500
- DLC: 25,000 sales @ avg $8 = $200,000
- **Year 1 Total**: ~$1,199,500

---

## Next Steps

1. **Complete base game first** ⚠️
2. Set up Steam DLC infrastructure
3. Plan Expansion 1 content
4. Develop DLC detection system
5. Create first expansion
6. Release on Steam

---

*Created: 2025-12-19*
*All DLC content goes in this directory*
*DLC is extra PAID content separate from base game*

**Important**: Focus on base game completion before DLC development!
