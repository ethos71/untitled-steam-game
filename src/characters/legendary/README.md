# Legendary Directory

This directory contains legendary enemies, items, and rare encounters for the NES-style roguelike.

## Purpose

Legendary content: ultra-rare enemies, mythical creatures, legendary weapons, and special encounters that are harder than bosses.

## Structure

```
legendary/
├── legendary.py          # Base legendary class
├── phoenix.py            # Phoenix legendary creature
├── hydra.py              # Multi-headed hydra
├── ancient_guardian.py   # Ancient guardian
├── legendary_items.py    # Legendary weapons and artifacts
├── encounters.py         # Special legendary encounters
└── README.md             # This file
```

## Legendary vs Villain vs Boss vs Enemy

### Legendary (Ultimate Challenge):
- **Ultra-rare** - 0.1-5% spawn chance
- **Optional** - Not required for main story
- **Extreme difficulty** - Harder than most bosses
- **Unique mechanics** - Special gimmicks
- **Epic loot** - Best items in game
- **Achievement-worthy** - Bragging rights

### Villain: Story-driven final encounter
### Boss: Multi-phase battles, mid-game
### Enemy: Regular encounters

---

## Legendary Rarity Tiers

- **Tier 1 - Rare**: 5% spawn, unique abilities
- **Tier 2 - Epic**: 1% spawn, multiple phases
- **Tier 3 - Mythical**: 0.1% spawn, strongest in game

---

## Legendary Creatures

### Phoenix (Fire Legendary)
**Rarity**: Epic (1%)  
**HP**: 300  
**Attack**: 20  
**Unique**: **Rebirth** - Resurrects 2 times

### Hydra (Multi-Head)
**Rarity**: Epic (1%)  
**HP**: 400  
**Attack**: 15  
**Unique**: **Growing Heads** - Cut 1, grow 2

### Ancient Guardian (Stone)
**Rarity**: Rare (5%)  
**HP**: 500  
**Defense**: 20  
**Unique**: **Stone Form** - Invulnerable phases

### Leviathan (Water)
**Rarity**: Mythical (0.1%)  
**HP**: 1000  
**Attack**: 30  
**Unique**: **Ocean Control** - Floods arena

---

## Legendary Items

```python
LEGENDARY_WEAPONS = {
    "Excalibur": {"damage": 50, "special": "Holy Strike"},
    "Mjolnir": {"damage": 45, "special": "Lightning Strike"},
    "Infinity Blade": {"damage": 60, "special": "Reality Slash"}
}
```

---

## Spawn System

```python
class LegendarySpawner:
    def attempt_spawn(self):
        roll = random.random()
        if roll < 0.001:    # Mythical
            return spawn_mythical()
        elif roll < 0.01:   # Epic
            return spawn_epic()
        elif roll < 0.05:   # Rare
            return spawn_rare()
```

---

## Visual Effects

- **Glowing Aura**: Color-coded by rarity
- **Pulsing Effect**: Draws attention
- **Warning Messages**: "A MYTHICAL LEGENDARY has appeared!"

---

## Difficulty Comparison

| Type | HP | Spawn | Difficulty |
|------|----|----|------------|
| Enemy | 10-30 | Common | ★☆☆☆☆ |
| Boss | 80-200 | Story | ★★★☆☆ |
| Villain | 500 | Once | ★★★★☆ |
| Legendary Rare | 300-500 | 5% | ★★★★☆ |
| Legendary Epic | 300-400 | 1% | ★★★★★ |
| Legendary Mythical | 1000+ | 0.1% | ★★★★★+ |

---

## Next Steps

1. Create base `Legendary` class
2. Implement Phoenix with rebirth
3. Add spawn system with rarities
4. Create legendary aura effects
5. Add legendary loot drops

---

*Created: 2025-12-19*
*All legendary code goes in this directory*
