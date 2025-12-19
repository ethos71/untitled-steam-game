# Sound Directory

This directory contains all sound effects and music for the NES-style roguelike.

## Organization

```
sound/
├── sfx/              # Sound effects
│   ├── walk.wav
│   ├── pickup.wav
│   ├── attack.wav
│   └── hurt.wav
├── music/            # Background music
│   ├── title.ogg
│   ├── dungeon.ogg
│   └── victory.ogg
└── README.md         # This file
```

## Sound Specifications

### Format
- **Sound Effects**: WAV or OGG
- **Music**: OGG (for smaller file size)
- **Sample Rate**: 22050 Hz (retro/8-bit quality)
- **Bit Depth**: 16-bit
- **Channels**: Mono preferred (stereo for music)

### Naming Convention
- Lowercase with underscores
- Descriptive names: `hero_walk.wav`, `enemy_hit.wav`
- Action-based: `pickup_coin.wav`, `door_open.wav`

## 8-Bit Sound Effects

### Generating Retro Sounds

You can generate NES-style sounds programmatically:

```python
import pygame.mixer
import numpy as np

def generate_square_wave(frequency=440, duration=0.1):
    """Generate NES-style square wave."""
    sample_rate = 22050
    samples = int(sample_rate * duration)
    wave = np.zeros(samples)
    
    for i in range(samples):
        wave[i] = 1 if (i // (sample_rate // frequency // 2)) % 2 == 0 else -1
    
    # Convert to 16-bit
    wave = (wave * 32767).astype(np.int16)
    sound = pygame.sndarray.make_sound(wave)
    return sound

# Generate common game sounds
jump_sound = generate_square_wave(600, 0.1)
hit_sound = generate_square_wave(200, 0.05)
pickup_sound = generate_square_wave(800, 0.08)
```

## Implementation

```python
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        
    def load_sound(self, name, filepath):
        """Load a sound effect."""
        try:
            self.sounds[name] = pygame.mixer.Sound(filepath)
            self.sounds[name].set_volume(self.sfx_volume)
        except:
            print(f"Could not load sound: {filepath}")
    
    def play_sound(self, name):
        """Play a sound effect."""
        if name in self.sounds:
            self.sounds[name].play()
    
    def play_music(self, filepath, loops=-1):
        """Play background music (loops=-1 for infinite)."""
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)
        except:
            print(f"Could not load music: {filepath}")

# Usage
sound_mgr = SoundManager()
sound_mgr.load_sound('walk', 'sound/sfx/walk.wav')
sound_mgr.play_sound('walk')
sound_mgr.play_music('sound/music/dungeon.ogg')
```

## Sound Effect Types

### Essential Sounds (Priority 1)
- [ ] walk.wav - Player movement
- [ ] pickup.wav - Item collection
- [ ] hurt.wav - Take damage
- [ ] menu_select.wav - UI navigation

### Important Sounds (Priority 2)
- [ ] attack.wav - Combat action
- [ ] hit.wav - Successful attack
- [ ] door_open.wav - Environment interaction
- [ ] level_up.wav - Player progression

## Tools for Creating 8-Bit Sounds

### Free Tools
- **sfxr / jsfxr** - https://sfxr.me/
- **ChipTone** - https://sfbgames.itch.io/chiptone
- **Audacity** - Free audio editor
- **BeepBox** - https://beepbox.co/

## Free Sound Resources

- **OpenGameArt.org** - CC-licensed sounds
- **Freesound.org** - Various licenses
- **Kenney.nl** - CC0 game assets
- **itch.io** - Free sound packs

---

*Created: 2025-12-19*
*All sound files should be placed in this directory*
