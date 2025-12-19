# Boss Directory

This directory contains all boss-related code for the NES-style roguelike.

## Purpose

All boss enemies, multi-phase battles, and boss-specific mechanics go in this folder.

## Structure

```
boss/
├── boss.py           # Base boss class
├── goblin_king.py    # Goblin King boss
├── dragon.py         # Dragon boss
├── necromancer.py    # Necromancer boss
├── phases.py         # Multi-phase battle system
└── README.md         # This file
```

## Boss vs Regular Enemy

### Bosses Have:
- **Multiple phases** - Change behavior at HP thresholds
- **Unique attacks** - Special abilities and patterns
- **Larger sprites** - 32x32 or larger
- **Boss music** - Special music track
- **Boss rooms** - Dedicated arenas
- **Guaranteed drops** - Keys, special items
- **Health bars** - On-screen HP display

### Regular Enemies:
- Single phase
- Simple AI
- Standard size (16x16)
- No special music
- Spawn anywhere
- Random drops

---

## Base Boss Class

```python
"""Base boss class for all boss enemies."""

class Boss:
    """Base class for all boss enemies."""
    
    def __init__(self, x, y, name, hp, attack):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.is_alive = True
        self.phase = 1
        self.max_phases = 3
        
    def take_damage(self, damage):
        """Apply damage and check phase transitions."""
        self.hp -= damage
        hp_percent = self.hp / self.max_hp
        
        if hp_percent < 0.66 and self.phase == 1:
            self.enter_phase(2)
        elif hp_percent < 0.33 and self.phase == 2:
            self.enter_phase(3)
        
        if self.hp <= 0:
            self.is_alive = False
    
    def enter_phase(self, new_phase):
        """Transition to new battle phase."""
        self.phase = new_phase
        # Override in subclasses
```

---

## Boss Types

### Goblin King
- **HP**: 100
- **Attack**: 8
- **Phases**: 3
- **Abilities**: Summon Goblins, Ground Slam

### Dragon
- **HP**: 200
- **Attack**: 15
- **Phases**: 2
- **Abilities**: Fire Breath, Wing Buffet

### Necromancer
- **HP**: 80
- **Attack**: 6
- **Phases**: 2
- **Abilities**: Raise Dead, Dark Bolt

---

## Boss HP Bar

```python
def render_boss_hp_bar(screen, boss, screen_width):
    """Render boss health bar at top of screen."""
    bar_width = screen_width - 40
    hp_percent = boss.hp / boss.max_hp
    fill_width = int(bar_width * hp_percent)
    
    # Color based on phase
    if boss.phase == 1:
        color = (0, 200, 0)  # Green
    elif boss.phase == 2:
        color = (255, 165, 0)  # Orange
    else:
        color = (255, 0, 0)  # Red
    
    pygame.draw.rect(screen, color, (20, 10, fill_width, 20))
```

---

## Integration Example

```python
from boss.goblin_king import GoblinKing

class NESGame:
    def __init__(self):
        self.current_boss = None
        self.in_boss_battle = False
    
    def start_boss_battle(self):
        """Start a boss battle."""
        self.current_boss = GoblinKing(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.in_boss_battle = True
    
    def update(self):
        if self.current_boss and self.current_boss.is_alive:
            self.current_boss.update(self)
```

---

## Next Steps

1. Create base `Boss` class with phases
2. Implement Goblin King (first boss)
3. Add phase transition system
4. Create boss HP bar
5. Add boss room generator
6. Integrate with game engine

---

*Created: 2025-12-19*
*All boss code goes in this directory*
