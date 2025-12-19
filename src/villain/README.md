# Villain Directory

This directory contains the main villain/antagonist code for the NES-style roguelike.

## Purpose

The primary antagonist, story elements, final boss mechanics, and villain-related systems go in this folder.

## Structure

```
villain/
├── villain.py        # Base villain class
├── dark_lord.py      # The Dark Lord (main villain)
├── cutscenes.py      # Villain cutscenes and dialogue
├── story.py          # Story progression system
└── README.md         # This file
```

## Villain vs Boss vs Enemy

### Villain (Main Antagonist):
- **Story-driven** - Central to plot
- **Final encounter** - End-game challenge
- **Multiple forms** - Transform during battle
- **Dialogue/cutscenes** - Story interaction
- **Epic arena** - Final battle location
- **True ending** - Determines game conclusion

### Boss:
- Multi-phase battles
- Mid-game encounters
- Special abilities

### Enemy:
- Regular encounters
- Simple AI

---

## Base Villain Class

```python
"""Base villain class for the main antagonist."""

class Villain:
    """Base class for the main villain."""
    
    def __init__(self, x, y, name, hp, attack):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.is_alive = True
        self.form = 1
        self.max_forms = 3
        
    def transform(self, new_form):
        """Transform into new form."""
        self.form = new_form
        print(f"{self.name} transforms!")
```

---

## The Dark Lord

### Forms

#### Form 1: "The Sorcerer" (100-50% HP)
- Magic attacks
- Summons minions
- Teleportation

#### Form 2: "The Demon" (50-20% HP)
- Monstrous transformation
- Fire attacks
- Enhanced speed

#### Form 3: "The Ancient One" (20-0% HP)
- True form
- Ultimate powers
- Final phase

---

## Story Integration

```python
class StorySystem:
    """Manages game story progression."""
    
    STORY_PHASES = [
        "introduction",
        "first_encounter",
        "gathering_power",
        "final_confrontation",
        "true_ending"
    ]
    
    def __init__(self):
        self.current_phase = "introduction"
```

---

## Cutscene System

```python
class Cutscene:
    """Manages dialogue scenes."""
    
    def __init__(self, dialogue_lines):
        self.dialogue_lines = dialogue_lines
        self.current_line = 0
        self.is_active = False
```

---

## Victory Conditions

```python
def check_victory_condition(game_state):
    """Determine ending."""
    
    if game_state.villain.is_alive == False:
        if game_state.artifacts_collected == 5:
            return "TRUE_ENDING"
        else:
            return "GOOD_ENDING"
```

---

## Integration Example

```python
from villain.dark_lord import DarkLord

class NESGame:
    def __init__(self):
        self.villain = None
        self.in_final_battle = False
    
    def start_final_battle(self):
        """Begin final boss encounter."""
        self.villain = DarkLord(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.in_final_battle = True
```

---

## Next Steps

1. Create base `Villain` class
2. Implement Dark Lord with 3 forms
3. Add dialogue/cutscene system
4. Create final arena
5. Implement story progression
6. Add multiple endings

---

*Created: 2025-12-19*
*All villain code goes in this directory*
