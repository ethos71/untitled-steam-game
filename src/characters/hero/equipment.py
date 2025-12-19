"""
Equipment System for Hero
Manages equippable items and stats bonuses
"""

from enum import Enum
from typing import Optional, Dict
from dataclasses import dataclass


class EquipmentSlot(Enum):
    """Available equipment slots"""
    HEAD = "head"
    BODY = "body"
    HANDS = "hands"
    LEGS = "legs"
    FEET = "feet"
    WEAPON = "weapon"
    SHIELD = "shield"
    ACCESSORY_1 = "accessory_1"
    ACCESSORY_2 = "accessory_2"


@dataclass
class EquipmentStats:
    """Stats provided by equipment"""
    attack: int = 0
    defense: int = 0
    magic_attack: int = 0
    magic_defense: int = 0
    speed: int = 0
    hp_bonus: int = 0
    mp_bonus: int = 0
    evasion: int = 0
    accuracy: int = 0
    
    def __add__(self, other):
        """Allow adding stats together"""
        return EquipmentStats(
            attack=self.attack + other.attack,
            defense=self.defense + other.defense,
            magic_attack=self.magic_attack + other.magic_attack,
            magic_defense=self.magic_defense + other.magic_defense,
            speed=self.speed + other.speed,
            hp_bonus=self.hp_bonus + other.hp_bonus,
            mp_bonus=self.mp_bonus + other.mp_bonus,
            evasion=self.evasion + other.evasion,
            accuracy=self.accuracy + other.accuracy
        )


@dataclass
class Equipment:
    """An equippable item"""
    name: str
    slot: EquipmentSlot
    stats: EquipmentStats
    description: str = ""
    special_effect: Optional[str] = None
    required_level: int = 1
    
    def __str__(self):
        return f"{self.name} ({self.slot.value})"


class EquipmentManager:
    """Manages equipped items for a character"""
    
    def __init__(self):
        self.equipped: Dict[EquipmentSlot, Optional[Equipment]] = {
            slot: None for slot in EquipmentSlot
        }
    
    def equip(self, equipment: Equipment, auto_equip: bool = False) -> Optional[Equipment]:
        """
        Equip an item, returns previously equipped item if any
        If auto_equip is True, only equips if slot is empty
        """
        slot = equipment.slot
        
        # If auto_equip mode and slot is not empty, don't equip
        if auto_equip and not self.is_slot_empty(slot):
            return None
            
        previous = self.equipped[slot]
        self.equipped[slot] = equipment
        return previous
    
    def unequip(self, slot: EquipmentSlot) -> Optional[Equipment]:
        """
        Unequip an item from a slot, returns the unequipped item
        """
        equipment = self.equipped[slot]
        self.equipped[slot] = None
        return equipment
    
    def get_equipped(self, slot: EquipmentSlot) -> Optional[Equipment]:
        """Get currently equipped item in a slot"""
        return self.equipped[slot]
    
    def get_total_stats(self) -> EquipmentStats:
        """Calculate total stats from all equipped items"""
        total = EquipmentStats()
        for equipment in self.equipped.values():
            if equipment:
                total = total + equipment.stats
        return total
    
    def get_all_equipped(self) -> Dict[EquipmentSlot, Optional[Equipment]]:
        """Get all equipped items"""
        return self.equipped.copy()
    
    def is_slot_empty(self, slot: EquipmentSlot) -> bool:
        """Check if a slot is empty"""
        return self.equipped[slot] is None


# Example equipment items
def create_starter_equipment():
    """Create some starter equipment"""
    return {
        "rusty_sword": Equipment(
            name="Rusty Sword",
            slot=EquipmentSlot.WEAPON,
            stats=EquipmentStats(attack=5),
            description="An old, rusty blade. Better than nothing.",
            required_level=1
        ),
        "leather_armor": Equipment(
            name="Leather Armor",
            slot=EquipmentSlot.BODY,
            stats=EquipmentStats(defense=3),
            description="Basic leather protection.",
            required_level=1
        ),
        "wooden_shield": Equipment(
            name="Wooden Shield",
            slot=EquipmentSlot.SHIELD,
            stats=EquipmentStats(defense=2, evasion=5),
            description="A simple wooden shield.",
            required_level=1
        ),
        "iron_sword": Equipment(
            name="Iron Sword",
            slot=EquipmentSlot.WEAPON,
            stats=EquipmentStats(attack=12),
            description="A well-forged iron blade.",
            required_level=5
        ),
        "steel_helmet": Equipment(
            name="Steel Helmet",
            slot=EquipmentSlot.HEAD,
            stats=EquipmentStats(defense=5, hp_bonus=10),
            description="Protects your head from harm.",
            required_level=3
        ),
        "magic_ring": Equipment(
            name="Magic Ring",
            slot=EquipmentSlot.ACCESSORY_1,
            stats=EquipmentStats(magic_attack=8, mp_bonus=15),
            description="A ring imbued with magical energy.",
            special_effect="Increases MP regeneration",
            required_level=4
        ),
    }


if __name__ == "__main__":
    # Example usage
    print("=== Equipment System Demo ===\n")
    
    # Create equipment manager
    manager = EquipmentManager()
    
    # Create equipment
    equipment = create_starter_equipment()
    
    # Equip items
    print("Equipping starter gear...")
    manager.equip(equipment["rusty_sword"])
    manager.equip(equipment["leather_armor"])
    manager.equip(equipment["wooden_shield"])
    
    print("\nCurrently Equipped:")
    for slot, item in manager.get_all_equipped().items():
        if item:
            print(f"  {slot.value}: {item.name}")
    
    print("\nTotal Stats from Equipment:")
    stats = manager.get_total_stats()
    print(f"  Attack: +{stats.attack}")
    print(f"  Defense: +{stats.defense}")
    print(f"  Evasion: +{stats.evasion}")
    
    # Upgrade weapon
    print("\n--- Upgrading to Iron Sword ---")
    old_weapon = manager.equip(equipment["iron_sword"])
    print(f"Removed: {old_weapon.name}")
    print(f"Equipped: {equipment['iron_sword'].name}")
    
    print("\nNew Total Stats:")
    stats = manager.get_total_stats()
    print(f"  Attack: +{stats.attack}")
    print(f"  Defense: +{stats.defense}")
    print(f"  Evasion: +{stats.evasion}")
