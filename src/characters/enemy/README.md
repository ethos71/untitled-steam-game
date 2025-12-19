# Enemy Directory

This directory contains all enemy-related code for the NES-style roguelike.

## Purpose

All enemy types, AI behaviors, and enemy-related systems go in this folder.

## Structure

```
enemy/
├── enemy.py          # Base enemy class
├── goblin.py         # Goblin enemy type
├── skeleton.py       # Skeleton enemy type
├── ai.py             # Enemy AI behaviors
└── README.md         # This file
```

## Base Enemy Class

### Example: `enemy.py`

```python
"""Base enemy class for all monsters."""

class Enemy:
    """Base class for all enemies."""
    
    def __init__(self, x, y, name, char, color, hp, attack, defense):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.is_alive = True
        
    def move(self, dx, dy):
        """Move the enemy by dx, dy."""
        self.x += dx
        self.y += dy
        
    def take_damage(self, damage):
        """Apply damage to enemy."""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
    
    def update(self, game_state):
        """Update enemy AI and behavior."""
        pass  # Override in subclasses
```

## Enemy Types

### Goblin
- **Character**: `g`
- **Color**: Green
- **HP**: 10
- **Attack**: 2

### Skeleton
- **Character**: `s`
- **Color**: White/Gray
- **HP**: 15
- **Attack**: 3

## AI Behaviors

### Chase AI
```python
def chase_ai(enemy, player):
    """Move towards player."""
    dx = player.x - enemy.x
    dy = player.y - enemy.y
    
    if abs(dx) > abs(dy):
        enemy.move(1 if dx > 0 else -1, 0)
    else:
        enemy.move(0, 1 if dy > 0 else -1)
```

## Integration

### In world_generator.py
```python
from enemy.goblin import Goblin

# Spawn enemies
self.enemies = []
for _ in range(10):
    x = random.randint(0, self.width)
    y = random.randint(0, self.height)
    if self.is_walkable(x, y):
        self.enemies.append(Goblin(x, y))
```

### In game_nes.py
```python
# Update enemies
for enemy in self.enemies:
    if enemy.is_alive:
        enemy.update(self)

# Render enemies
for enemy in self.enemies:
    if enemy.is_alive:
        # Render enemy sprite
        pass
```

## Next Steps

1. Create base `Enemy` class
2. Implement Goblin enemy
3. Add chase AI
4. Integrate with game engine
5. Add combat system

---

*Created: 2025-12-19*
*All enemy code goes in this directory*
