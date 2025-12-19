# Story Directory

This directory contains all story-related content for the NES-style roguelike.

## Purpose

Central hub for narrative content: dialogue, cutscenes, story progression, character relationships, and plot events that connect hero, enemy, villain, and legendary characters.

## Structure

```
story/
├── story.py              # Main story system
├── dialogue.py           # Dialogue system
├── cutscenes.py          # Cutscene manager
├── quests.py             # Quest system
├── relationships.py      # Character relationships
├── events.py             # Story events
├── scripts/              # Story scripts
│   ├── prologue.py
│   ├── chapter_1.py
│   ├── chapter_2.py
│   └── epilogue.py
└── README.md             # This file
```

---

## Story Overview

### Main Plot

**Setting**: A world corrupted by the Dark Lord's evil power.

**Hero's Journey**:
1. **Prologue**: Hero awakens in destroyed village
2. **Act 1**: Discover the Dark Lord's existence
3. **Act 2**: Gather power and allies
4. **Act 3**: Face the Dark Lord
5. **Epilogue**: Restore peace to the land

---

## Story System

### Story Progression

```python
class StorySystem:
    """Manages overall story progression."""
    
    STORY_PHASES = {
        "prologue": "The Awakening",
        "chapter_1": "The Discovery",
        "chapter_2": "Gathering Power",
        "chapter_3": "The Final Battle",
        "epilogue": "Peace Restored"
    }
    
    def __init__(self):
        self.current_phase = "prologue"
        self.story_flags = {}
        
    def advance_phase(self, new_phase):
        """Progress to next story phase."""
        self.current_phase = new_phase
        self.trigger_cutscene(new_phase)
```

---

## Dialogue System

### Character Dialogue

```python
DIALOGUE = {
    "hero": {
        "start": [
            "Where... where am I?",
            "The village... it's destroyed!",
            "I must find out what happened."
        ]
    },
    
    "dark_lord": {
        "first_encounter": [
            "So... you've finally arrived.",
            "The prophecy's 'chosen one'.",
            "You think you can defeat me?",
            "Come then, HERO. Show me your power!"
        ]
    }
}
```

---

## Cutscene System

### Cutscene Types
- **Fade transitions**: Fade in/out
- **Dialogue scenes**: Character conversations
- **Image scenes**: Show story images
- **Battle intros**: Boss introduction cutscenes

```python
class Cutscene:
    """Manages cutscene playback."""
    
    def __init__(self, cutscene_id):
        self.cutscene_id = cutscene_id
        self.scenes = []
        self.is_active = False
```

---

## Quest System

### Main Quest Line

```python
MAIN_QUESTS = {
    "quest_1": {
        "title": "The Awakening",
        "description": "Explore the destroyed village",
        "objectives": [
            {"desc": "Find your sword", "target": "hero_sword"},
            {"desc": "Defeat 5 enemies", "count": 5}
        ]
    },
    
    "quest_2": {
        "title": "Gather the Artifacts",
        "description": "Collect the three ancient artifacts",
        "objectives": [
            {"desc": "Find Fire Crystal", "target": "fire_crystal"},
            {"desc": "Find Ice Crystal", "target": "ice_crystal"},
            {"desc": "Find Thunder Crystal", "target": "thunder_crystal"}
        ]
    },
    
    "quest_3": {
        "title": "The Final Confrontation",
        "description": "Defeat the Dark Lord",
        "objectives": [
            {"desc": "Defeat the Dark Lord", "target": "dark_lord"}
        ]
    }
}
```

---

## Character Relationships

### Relationship Matrix

```python
RELATIONSHIPS = {
    ("hero", "dark_lord"): "enemies",
    ("hero", "stranger"): "allies",
    ("dark_lord", "bosses"): "master",
    ("legendary", "hero"): "respect",
    ("legendary", "dark_lord"): "ancient_rivalry"
}
```

---

## Story Integration

### Connecting All Characters

**Hero**:
- Main protagonist
- Chosen one from prophecy
- Opposes Dark Lord

**Enemy**:
- Dark Lord's minions
- Corrupted by evil
- Block hero's progress

**Boss**:
- Dark Lord's lieutenants
- Story checkpoints
- Guard important areas

**Villain (Dark Lord)**:
- Main antagonist
- Final boss
- Central to story

**Legendary**:
- Ancient beings
- Tied to lore
- Optional encounters
- May have history with Dark Lord

---

## Multiple Endings

### Ending Types

```python
ENDINGS = {
    "true_ending": {
        "name": "True Hero",
        "requirements": {
            "artifacts_collected": 3,
            "dark_lord_defeated": True,
            "legendary_defeated": 1
        }
    },
    
    "good_ending": {
        "name": "Victorious",
        "requirements": {
            "dark_lord_defeated": True
        }
    },
    
    "bad_ending": {
        "name": "Darkness Falls",
        "requirements": {
            "hero_died": True
        }
    }
}
```

---

## Integration Example

```python
from story.story import StorySystem
from story.dialogue import DialogueSystem

class NESGame:
    def __init__(self):
        self.story = StorySystem()
        self.dialogue = DialogueSystem()
        
    def start_game(self):
        """Start new game."""
        self.story.play_cutscene("prologue")
        
    def on_boss_defeat(self, boss_name):
        """Handle boss defeat."""
        self.story.advance_phase("chapter_2")
        
    def on_villain_defeat(self):
        """Handle villain defeat."""
        self.story.advance_phase("epilogue")
```

---

## Story Checklist

### Essential Elements
- [ ] Story progression system
- [ ] Dialogue system
- [ ] Cutscenes (prologue, ending)
- [ ] Main quest line
- [ ] Character relationships
- [ ] Multiple endings

### Nice to Have
- [ ] Side quests
- [ ] Optional dialogue
- [ ] Hidden lore
- [ ] Character backstories

---

## Next Steps

1. Create base `StorySystem` class
2. Implement dialogue system
3. Create prologue cutscene
4. Add main quest line
5. Integrate with characters
6. Create multiple endings

---

*Created: 2025-12-19*
*All story content goes in this directory*
*Story connects hero, enemy, villain, and legendary*
