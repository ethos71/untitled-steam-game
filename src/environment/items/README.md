# Items Directory

This directory contains all items, weapons, consumables, and inventory systems for the NES-style roguelike.

## Purpose

Central hub for all collectible items: weapons, armor, consumables, quest items, and the inventory system.

## Structure

```
items/
├── item.py               # Base item class
├── weapon.py             # Weapon items
├── armor.py              # Armor items
├── consumable.py         # Potions, food, etc.
├── quest_item.py         # Story quest items
├── inventory.py          # Inventory system
├── equipment.py          # Equipment manager
├── item_database.py      # All item definitions
└── README.md             # This file
```

---

## Item Types

### **1. Weapons**
Offensive items that increase attack power

**Examples**:
- Wooden Sword (starter)
- Iron Sword
- Fire Blade
- Legendary Excalibur

### **2. Armor**
Defensive items that reduce damage

**Examples**:
- Leather Armor (starter)
- Iron Armor
- Dragon Scale Armor
- Legendary Aegis Shield

### **3. Consumables**
Single-use items with immediate effects

**Examples**:
- Health Potion (restore HP)
- Mana Potion (restore MP)
- Elixir (full restore)
- Phoenix Feather (auto-revive)

### **4. Quest Items**
Story-related items required for progression

**Examples**:
- Ancient Map
- Fire Crystal
- Ice Crystal
- Thunder Crystal

---

## Item System

### Base Item Class

```python
class Item:
    """Base item class."""
    
    def __init__(self, item_id, name, description, item_type, rarity):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.item_type = item_type  # weapon, armor, consumable, quest
        self.rarity = rarity        # common, uncommon, rare, legendary
        self.value = 0
        self.is_stackable = False
        self.max_stack = 1
```

---

## Weapon Examples

```python
WEAPONS = {
    "wooden_sword": {
        "name": "Wooden Sword",
        "attack": 5,
        "rarity": "common",
        "value": 10
    },
    "iron_sword": {
        "name": "Iron Sword",
        "attack": 15,
        "rarity": "uncommon",
        "value": 100
    },
    "fire_blade": {
        "name": "Fire Blade",
        "attack": 30,
        "element": "fire",
        "rarity": "rare",
        "value": 500
    },
    "excalibur": {
        "name": "Excalibur",
        "attack": 100,
        "rarity": "legendary",
        "value": 9999
    }
}
```

---

## Armor Examples

```python
ARMOR = {
    "leather_armor": {
        "name": "Leather Armor",
        "defense": 5,
        "rarity": "common",
        "value": 20
    },
    "iron_armor": {
        "name": "Iron Armor",
        "defense": 15,
        "rarity": "uncommon",
        "value": 150
    },
    "dragon_scale": {
        "name": "Dragon Scale Armor",
        "defense": 40,
        "rarity": "rare",
        "value": 800
    }
}
```

---

## Consumables

```python
CONSUMABLES = {
    "health_potion": {
        "name": "Health Potion",
        "effect": "heal",
        "value": 50,
        "price": 25
    },
    "mana_potion": {
        "name": "Mana Potion",
        "effect": "mana",
        "value": 30,
        "price": 20
    },
    "elixir": {
        "name": "Elixir",
        "effect": "full_restore",
        "rarity": "rare",
        "price": 500
    }
}
```

---

## Inventory System

```python
class Inventory:
    """Player inventory system."""
    
    def __init__(self, max_slots=20):
        self.max_slots = max_slots
        self.items = []
        self.gold = 0
        
    def add_item(self, item, quantity=1):
        """Add item to inventory."""
        if len(self.items) < self.max_slots:
            self.items.append((item, quantity))
            return True
        return False
    
    def remove_item(self, item_id, quantity=1):
        """Remove item from inventory."""
        for i, (item, qty) in enumerate(self.items):
            if item.item_id == item_id:
                if qty <= quantity:
                    self.items.pop(i)
                else:
                    self.items[i] = (item, qty - quantity)
                return True
        return False
```

---

## Equipment System

```python
class Equipment:
    """Character equipment."""
    
    def __init__(self):
        self.weapon = None
        self.armor = None
        self.shield = None
        
    def equip_weapon(self, weapon):
        old = self.weapon
        self.weapon = weapon
        return old
    
    def get_total_attack(self):
        return self.weapon.attack_power if self.weapon else 0
    
    def get_total_defense(self):
        defense = 0
        if self.armor:
            defense += self.armor.defense
        if self.shield:
            defense += self.shield.defense
        return defense
```

---

## Rarity System

```python
RARITY = {
    "common": {
        "color": (255, 255, 255),  # White
        "drop_rate": 0.60
    },
    "uncommon": {
        "color": (0, 255, 0),      # Green
        "drop_rate": 0.25
    },
    "rare": {
        "color": (0, 0, 255),      # Blue
        "drop_rate": 0.10
    },
    "legendary": {
        "color": (255, 165, 0),    # Orange
        "drop_rate": 0.01
    }
}
```

---

## Loot System

```python
class LootSystem:
    """Manages item drops."""
    
    def generate_loot(self, enemy_type, enemy_level):
        """Generate loot drops."""
        gold = random.randint(10, 50) * enemy_level
        
        # 30% chance for item drop
        if random.random() < 0.3:
            rarity = self._roll_rarity()
            item = self._get_random_item(rarity)
            return gold, [item]
        
        return gold, []
```

---

## Quest Items

```python
QUEST_ITEMS = {
    "fire_crystal": {
        "name": "Fire Crystal",
        "description": "Crystal of fire energy",
        "quest_id": "gather_crystals"
    },
    "ice_crystal": {
        "name": "Ice Crystal",
        "description": "Crystal of ice energy",
        "quest_id": "gather_crystals"
    },
    "thunder_crystal": {
        "name": "Thunder Crystal",
        "description": "Crystal of thunder energy",
        "quest_id": "gather_crystals"
    }
}
```

---

## Item Checklist

- [ ] Base Item class
- [ ] Weapon system
- [ ] Armor system
- [ ] Consumable system
- [ ] Inventory system
- [ ] Equipment system
- [ ] Loot drops
- [ ] Quest items

---

*Created: 2025-12-19*
*All items go in this directory*
