"""
Treasure chest system with random item generation
"""

import random
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class ItemType(Enum):
    """Types of items"""
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"


class ItemRarity(Enum):
    """Item rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class Item:
    """Game item"""
    name: str
    type: ItemType
    rarity: ItemRarity
    description: str
    stats: dict = None
    
    def __post_init__(self):
        if self.stats is None:
            self.stats = {}


class TreasureChest:
    """Treasure chest with random loot"""
    
    def __init__(self, x: int, y: int, shell_level: int = 1):
        self.x = x
        self.y = y
        self.shell_level = shell_level
        self.opened = False
        self.item: Optional[Item] = None
        self.char = '□'  # Closed chest
        self.opened_char = '■'  # Opened chest
        self.color = (218, 165, 32)  # Gold
        
        # Generate item when chest is created
        self._generate_item()
    
    def _generate_item(self):
        """Generate random item based on shell level"""
        # Rarity chances increase with shell level
        rarity_chances = {
            ItemRarity.COMMON: max(60 - self.shell_level * 5, 10),
            ItemRarity.UNCOMMON: min(25 + self.shell_level * 2, 40),
            ItemRarity.RARE: min(10 + self.shell_level * 2, 30),
            ItemRarity.EPIC: min(4 + self.shell_level, 15),
            ItemRarity.LEGENDARY: min(1 + self.shell_level // 2, 5),
        }
        
        # Choose rarity
        rarities = list(rarity_chances.keys())
        weights = list(rarity_chances.values())
        rarity = random.choices(rarities, weights=weights)[0]
        
        # Choose item type
        item_type = random.choice(list(ItemType))
        
        # Generate item based on type and rarity
        self.item = self._create_item(item_type, rarity)
    
    def _create_item(self, item_type: ItemType, rarity: ItemRarity) -> Item:
        """Create specific item"""
        rarity_multiplier = {
            ItemRarity.COMMON: 1,
            ItemRarity.UNCOMMON: 1.5,
            ItemRarity.RARE: 2,
            ItemRarity.EPIC: 3,
            ItemRarity.LEGENDARY: 5,
        }[rarity]
        
        base_power = (5 + self.shell_level * 3) * rarity_multiplier
        
        if item_type == ItemType.WEAPON:
            weapons = [
                "Sword", "Axe", "Spear", "Dagger", "Staff", "Bow", 
                "Hammer", "Mace", "Katana", "Scythe"
            ]
            name = f"{rarity.value.title()} {random.choice(weapons)}"
            stats = {
                "attack": int(base_power),
                "accuracy": random.randint(80, 100)
            }
            desc = f"A {rarity.value} weapon found in Shell {self.shell_level}"
            
        elif item_type == ItemType.ARMOR:
            armor_pieces = [
                "Helmet", "Chestplate", "Boots", "Gauntlets", "Shield"
            ]
            name = f"{rarity.value.title()} {random.choice(armor_pieces)}"
            stats = {
                "defense": int(base_power * 0.8),
                "hp_bonus": int(base_power * 2)
            }
            desc = f"Protective {rarity.value} armor from Shell {self.shell_level}"
            
        elif item_type == ItemType.ACCESSORY:
            accessories = [
                "Ring", "Amulet", "Pendant", "Bracelet", "Talisman"
            ]
            name = f"{rarity.value.title()} {random.choice(accessories)}"
            stats = {
                "magic_power": int(base_power * 0.6),
                "mp_bonus": int(base_power * 3)
            }
            desc = f"A mystical {rarity.value} accessory"
            
        else:  # CONSUMABLE
            consumables = [
                "Potion", "Elixir", "Remedy", "Tonic", "Ether"
            ]
            name = f"{rarity.value.title()} {random.choice(consumables)}"
            stats = {
                "hp_restore": int(base_power * 10),
                "mp_restore": int(base_power * 5)
            }
            desc = f"Restores HP and MP"
        
        return Item(
            name=name,
            type=item_type,
            rarity=rarity,
            description=desc,
            stats=stats
        )
    
    def open(self) -> Optional[Item]:
        """Open the chest and get the item"""
        if not self.opened:
            self.opened = True
            return self.item
        return None
    
    def render_char(self) -> str:
        """Get display character"""
        return self.opened_char if self.opened else self.char


def place_treasure_chest(width: int, height: int, occupied_positions: set, shell_level: int = 1) -> Optional[TreasureChest]:
    """Place a treasure chest in a random walkable location"""
    max_attempts = 100
    for _ in range(max_attempts):
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        
        if (x, y) not in occupied_positions:
            return TreasureChest(x, y, shell_level)
    
    return None


if __name__ == "__main__":
    # Test treasure generation
    print("=== Treasure Chest System Test ===\n")
    
    for shell in range(1, 6):
        print(f"\nShell Level {shell}:")
        chest = TreasureChest(0, 0, shell)
        item = chest.open()
        print(f"  Item: {item.name}")
        print(f"  Type: {item.type.value}")
        print(f"  Rarity: {item.rarity.value}")
        print(f"  Stats: {item.stats}")
        print(f"  Description: {item.description}")
