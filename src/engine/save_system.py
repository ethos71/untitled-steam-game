"""Save/Load system for game state persistence."""
import json
import os
from datetime import datetime
from pathlib import Path


class SaveSystem:
    """Handles saving and loading game state."""
    
    def __init__(self, save_dir="saves"):
        """Initialize save system."""
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.autosave_path = self.save_dir / "autosave.json"
        
    def save_game(self, game_state, slot_name="manual_save"):
        """Save current game state."""
        save_path = self.save_dir / f"{slot_name}.json"
        
        # Get hero equipment if available
        equipment_data = {}
        hero = game_state.get('hero')
        if hero and hasattr(hero, 'equipment'):
            if hasattr(hero.equipment, 'equipped'):
                equipment_data = {
                    slot.value: self._serialize_item(item) if item else None
                    for slot, item in hero.equipment.equipped.items()
                }
        
        # Get hero inventory if available
        inventory_data = []
        if hero and hasattr(hero, 'inventory'):
            inventory_data = [self._serialize_item(item) for item in hero.inventory]
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'hero': {
                'x': getattr(hero, 'x', 0),
                'y': getattr(hero, 'y', 0),
                'hp': getattr(hero, 'hp', 100),
                'max_hp': getattr(hero, 'max_hp', 100),
                'inventory': inventory_data,
                'equipment': equipment_data
            },
            'terrain': {
                f"{x},{y}": {'char': getattr(tile, 'char', '?'), 'walkable': getattr(tile, 'is_walkable', True)}
                for (x, y), tile in game_state.get('terrain', {}).items()
            },
            'chests': [
                {
                    'x': chest.get('x') if isinstance(chest, dict) else getattr(chest, 'x', 0),
                    'y': chest.get('y') if isinstance(chest, dict) else getattr(chest, 'y', 0),
                    'opened': chest.get('opened', False) if isinstance(chest, dict) else getattr(chest, 'opened', False),
                    'item': self._serialize_item(chest.get('item') if isinstance(chest, dict) else getattr(chest, 'item', None)) if (chest.get('item') if isinstance(chest, dict) else getattr(chest, 'item', None)) else None
                }
                for chest in (game_state.get('chests', []) if game_state.get('chests') else [])
            ],
            'world_seed': game_state.get('seed', None),
            'map_size': {
                'width': game_state.get('width', 20),
                'height': game_state.get('height', 15)
            }
        }
        
        with open(save_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    
    def load_game(self, slot_name="manual_save"):
        """Load game state from save file."""
        save_path = self.save_dir / f"{slot_name}.json"
        
        if not save_path.exists():
            return None
        
        try:
            with open(save_path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading save: {e}")
            return None
    
    def autosave(self, game_state):
        """Auto-save current game state."""
        return self.save_game(game_state, "autosave")
    
    def load_autosave(self):
        """Load the most recent auto-save."""
        return self.load_game("autosave")
    
    def list_saves(self):
        """List all available save files."""
        saves = []
        for save_file in self.save_dir.glob("*.json"):
            if save_file.name != "autosave.json":
                try:
                    with open(save_file, 'r') as f:
                        data = json.load(f)
                        saves.append({
                            'name': save_file.stem,
                            'timestamp': data.get('timestamp', 'Unknown'),
                            'path': save_file
                        })
                except:
                    pass
        return sorted(saves, key=lambda x: x['timestamp'], reverse=True)
    
    def delete_save(self, slot_name):
        """Delete a save file."""
        save_path = self.save_dir / f"{slot_name}.json"
        if save_path.exists():
            save_path.unlink()
            return True
        return False
    
    def _serialize_item(self, item):
        """Convert item to serializable format."""
        if not item:
            return None
        return {
            'name': getattr(item, 'name', 'Unknown'),
            'slot': getattr(item.slot, 'value', str(item.slot)) if hasattr(item, 'slot') else 'unknown',
            'stats': {
                'attack': getattr(item.stats, 'attack', 0),
                'defense': getattr(item.stats, 'defense', 0),
                'magic_attack': getattr(item.stats, 'magic_attack', 0),
                'magic_defense': getattr(item.stats, 'magic_defense', 0),
                'speed': getattr(item.stats, 'speed', 0),
                'hp_bonus': getattr(item.stats, 'hp_bonus', 0),
                'mp_bonus': getattr(item.stats, 'mp_bonus', 0),
                'evasion': getattr(item.stats, 'evasion', 0),
                'accuracy': getattr(item.stats, 'accuracy', 0),
            } if hasattr(item, 'stats') else {}
        }
