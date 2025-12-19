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
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'hero': {
                'x': game_state['hero'].x,
                'y': game_state['hero'].y,
                'hp': game_state['hero'].hp,
                'max_hp': game_state['hero'].max_hp,
                'inventory': [self._serialize_item(item) for item in game_state['hero'].inventory],
                'equipment': {
                    slot: self._serialize_item(item) if item else None
                    for slot, item in game_state['hero'].equipment_manager.equipment.items()
                }
            },
            'terrain': {
                f"{x},{y}": {'char': tile.char, 'walkable': tile.walkable}
                for (x, y), tile in game_state['terrain'].items()
            },
            'chests': game_state['chests'],
            'world_seed': game_state.get('seed', None),
            'map_size': {
                'width': game_state['width'],
                'height': game_state['height']
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
        return {
            'name': item.name,
            'slot': item.slot,
            'stats': item.stats
        }
