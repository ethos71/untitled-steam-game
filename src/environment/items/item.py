"""
Item system for equipment and inventory
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any


class ItemSlot(Enum):
    """Equipment slots"""
    HEAD = "head"
    BODY = "body"
    LEGS = "legs"
    WEAPON = "weapon"
    RING = "ring"


@dataclass
class Item:
    """Game item that can be equipped"""
    name: str
    slot: ItemSlot
    stats: Dict[str, Any]
    
    def __post_init__(self):
        if self.stats is None:
            self.stats = {}
