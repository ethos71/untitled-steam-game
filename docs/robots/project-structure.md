# Project Structure

## Overview
Complete directory structure for the NES-style roguelike Steam game.

---

## Root Structure

```
untitled-steam-game/
├── .github/
│   ├── agents/
│   │   └── @idunno.json          # AI agent configuration
│   ├── prompts/
│   │   └── @idunno.md            # AI agent prompts
│   └── workflows/
│       ├── build-test.yml        # CI/CD build pipeline
│       └── steam-deploy.yml      # Steam deployment workflow
│
├── docs/
│   └── robots/                   # AI agent documentation
│       ├── agent-setup.md
│       ├── ascii-game-options.md
│       ├── game-implementation.md
│       ├── github-secrets-setup.md
│       ├── migration-guide.md
│       ├── nes-style-conversion.md
│       ├── project-structure.md
│       ├── pygame-example.md
│       ├── python-setup-guide.md
│       ├── quick-start-nes.md
│       └── steam-setup-guide.md
│
├── dlc/                          # DLC content (extra PAID content)
│   ├── expansion_1/              # First expansion DLC
│   ├── expansion_2/              # Second expansion DLC
│   ├── character_pack_1/         # Character DLC
│   └── README.md                 # DLC documentation
│
└── src/                          # All source code (base game)
    ├── assets/
    │   ├── tiles/                # 16x16 tile graphics
    │   └── sprites/              # Character sprites
    │
    ├── engine/
    │   ├── game_nes.py           # Main NES-style game engine
    │   ├── game_simple.py        # ASCII version (tcod, simple)
    │   └── main.py               # ASCII version (tcod, custom font)
    │
    ├── hero/
    │   └── hero.py               # Player character class
    │
    ├── enemy/
    │   ├── enemy.py              # Base enemy class
    │   ├── goblin.py             # Goblin enemy
    │   ├── ai.py                 # Enemy AI behaviors
    │   └── README.md             # Enemy documentation
    │
    ├── boss/
    │   ├── boss.py               # Base boss class
    │   ├── goblin_king.py        # Goblin King boss
    │   ├── dragon.py             # Dragon boss
    │   ├── phases.py             # Multi-phase system
    │   └── README.md             # Boss documentation
    │
    ├── villain/
    │   ├── villain.py            # Base villain class
    │   ├── dark_lord.py          # The Dark Lord (main villain)
    │   ├── cutscenes.py          # Dialogue and story scenes
    │   ├── story.py              # Story progression system
    │   └── README.md             # Villain documentation
    │
    ├── legendary/
    │   ├── legendary.py          # Base legendary class
    │   ├── phoenix.py            # Phoenix legendary creature
    │   ├── hydra.py              # Hydra legendary
    │   ├── legendary_items.py    # Legendary weapons/items
    │   ├── encounters.py         # Legendary encounters
    │   └── README.md             # Legendary documentation
    │
    ├── story/
    │   ├── story.py              # Main story system
    │   ├── dialogue.py           # Dialogue system
    │   ├── cutscenes.py          # Cutscene manager
    │   ├── quests.py             # Quest system
    │   ├── relationships.py      # Character relationships
    │   ├── scripts/              # Story scripts
    │   └── README.md             # Story documentation
    │
    ├── scenery/
    │   └── terrain.py            # Terrain elements
    │
    ├── sound/                    # All audio files
    │   ├── sfx/                  # Sound effects
    │   ├── music/                # Background music
    │   └── README.md
    │
    ├── steam/
    │   └── steam_config.json     # Steam deployment config
    │
    ├── world/
    │   └── world_generator.py    # Procedural world generation
    │
    ├── requirements.txt          # Python dependencies
    └── README.md                 # Source code documentation
```

---

## Key Directories

### `.github/`
GitHub-specific configuration

- **agents/**: AI agent definitions
- **prompts/**: AI agent instructions
- **workflows/**: CI/CD automation

### `docs/robots/`
Documentation for AI agents and developers

- Setup guides
- Migration guides
- Feature documentation
- Quick start guides

### `dlc/` (Downloadable Content)
**Extra PAID content** - Expansions and DLC

- **expansion_1/**: First major expansion
- **expansion_2/**: Second major expansion
- **character_pack_1/**: New playable characters
- **dungeon_pack_1/**: New dungeons
- **cosmetic_pack_1/**: Visual upgrades

### `src/` (Source Code)
All **base game** code and assets

#### `src/assets/`
- **tiles/**: 16x16 PNG tile graphics
- **sprites/**: Character and entity sprites

#### `src/engine/`
- **game_nes.py**: Main NES-style pygame engine

#### `src/hero/`
- **hero.py**: Player character implementation

#### `src/enemy/`
**All enemy code goes here**
- **enemy.py**: Base enemy class
- **AI systems**: Chase, patrol, ranged behaviors
- **Enemy types**: Goblins, skeletons, etc.

#### `src/boss/`
**All boss code goes here**
- **boss.py**: Base boss class with phases
- **Multi-phase battles**: HP-based transitions
- **Boss types**: Goblin King, Dragon, Necromancer
- **Special abilities**: Unique boss attacks

#### `src/villain/`
**All main villain code goes here**
- **villain.py**: Base villain/antagonist class
- **Story integration**: Main plot and narrative
- **Multiple forms**: Epic transformations
- **Final battle**: End-game encounter
- **Cutscenes**: Dialogue and story progression

#### `src/legendary/`
**All legendary content goes here**
- **legendary.py**: Base legendary enemy class
- **Ultra-rare encounters**: 0.1-5% spawn chance
- **Unique mechanics**: Special gimmicks per legendary
- **Epic loot**: Best items in game
- **Optional challenges**: Not required for story

#### `src/story/`
**All story content goes here**
- **story.py**: Main story progression system
- **dialogue.py**: Character dialogue and conversations
- **cutscenes.py**: Cutscene manager for story events
- **quests.py**: Quest and objective system
- **relationships.py**: Character relationship tracking
- **Narrative hub**: Connects hero, enemy, villain, legendary

#### `src/scenery/`
- **terrain.py**: Terrain types (grass, trees, rocks, water)

#### `src/sound/`
**All audio files go here**
- **sfx/**: Sound effects (.wav)
- **music/**: Background music (.ogg)

#### `src/steam/`
- **steam_config.json**: Steam deployment configuration

#### `src/world/`
- **world_generator.py**: Procedural world generation

---

## File Purposes

### Game Versions

| File | Engine | Description |
|------|--------|-------------|
| `src/engine/game_nes.py` | pygame | NES-style with pixel graphics |
| `src/engine/game_simple.py` | tcod | ASCII with default font |
| `src/engine/main.py` | tcod | ASCII with custom font |

### Core Game Systems

| File | Purpose |
|------|---------|
| `src/hero/hero.py` | Player character class |
| `src/enemy/` | Regular enemy types and AI |
| `src/boss/` | Boss enemies and multi-phase battles |
| `src/villain/` | Main antagonist and story elements |
| `src/legendary/` | Legendary enemies and ultra-rare encounters |
| `src/story/` | Dialogue, cutscenes, quests, and narrative |
| `src/scenery/terrain.py` | World terrain types |
| `src/world/world_generator.py` | Procedural generation |

### Configuration

| File | Purpose |
|------|---------|
| `src/requirements.txt` | Python dependencies |
| `src/steam/steam_config.json` | Steam deployment |
| `.github/agents/@idunno.json` | AI agent config |

---

## Asset Locations

### Graphics
- **Tiles**: `src/assets/tiles/*.png`
- **Sprites**: `src/assets/sprites/*.png`

### Audio
- **Sound Effects**: `src/sound/sfx/*.wav`
- **Music**: `src/sound/music/*.ogg`

### Configuration
- **Steam**: `src/steam/steam_config.json`

---

## Adding New Files

### New Base Game Code
→ Place in `src/` directory
- Use subdirectories for organization
- Follow existing patterns:
  - **hero/**: Player character code
  - **enemy/**: Regular enemy types and AI
  - **boss/**: Boss enemies and multi-phase battles
  - **villain/**: Main antagonist and story
  - **legendary/**: Legendary enemies and rare encounters
  - **story/**: Dialogue, cutscenes, and narrative
  - **scenery/**: Environment and terrain
  - **world/**: World generation
  - **engine/**: Game engines

### New DLC Content
→ Place in `dlc/` directory
- **Extra PAID content only**
- Create expansion folder (e.g., `dlc/expansion_1/`)
- Include content, assets, and README
- Set up Steam DLC integration

### New Tiles
→ Place in `src/assets/tiles/`
- 16x16 PNG format
- NES color palette
- Transparent background

### New Sprites
→ Place in `src/assets/sprites/`
- 16x16 PNG format
- Animation frames as separate files
- Descriptive naming (hero_walk_01.png)

### New Sounds
→ Place in `src/sound/`
- **Sound effects**: `src/sound/sfx/*.wav`
- **Music**: `src/sound/music/*.ogg`
- 22050 Hz sample rate
- See `src/sound/README.md`

### New Documentation
→ Place in `docs/robots/`
- Markdown format
- AI agent readable
- Include creation date

---

## Build Artifacts

### Generated (Not in Git)

```
build/              # Build output
dist/               # Distribution packages
venv/               # Python virtual environment
__pycache__/        # Python cache
*.pyc               # Compiled Python
.DS_Store           # macOS metadata
```

---

## Environment Files

### Required
- `src/requirements.txt` - Python packages

### Optional
- `.env` - Environment variables (not in git)
- `.gitignore` - Git ignore patterns
- `pyproject.toml` - Python project config

---

## Current Status

### ✅ Implemented
- [x] NES-style game engine
- [x] Procedural world generation
- [x] ASCII tcod versions
- [x] CI/CD workflows
- [x] Documentation
- [x] Project structure

### 📁 Empty Directories (Ready for Content)

#### Base Game
- [ ] `src/enemy/` - Add enemy types and AI
- [ ] `src/boss/` - Add boss enemies with phases
- [ ] `src/villain/` - Add main villain and story
- [ ] `src/legendary/` - Add legendary encounters and items
- [ ] `src/story/` - Add dialogue, cutscenes, and quests
- [ ] `src/assets/tiles/` - Add PNG tiles
- [ ] `src/assets/sprites/` - Add character sprites
- [ ] `src/sound/sfx/` - Add sound effects
- [ ] `src/sound/music/` - Add background music

#### DLC (Paid Content)
- [ ] `dlc/expansion_1/` - First major expansion
- [ ] `dlc/character_pack_1/` - New playable characters
- [ ] `dlc/cosmetic_pack_1/` - Visual upgrades

### 🎯 Next Steps

#### Phase 1: Base Game (Priority)
1. **Implement enemies** (src/enemy/)
   - Create base Enemy class
   - Add Goblin with chase AI
   - Integrate with world generator
2. **Implement bosses** (src/boss/)
   - Create base Boss class with phases
   - Add Goblin King (first boss)
   - Add boss HP bar
3. **Implement villain** (src/villain/)
   - Create Dark Lord with multiple forms
   - Create final battle arena
4. **Implement legendary** (src/legendary/)
   - Create base Legendary class
   - Add Phoenix with rebirth mechanic
   - Implement spawn system with rarities
5. **Implement story** (src/story/)
   - Create story progression system
   - Add dialogue system
   - Create cutscenes (prologue, ending)
   - Add main quest line
6. Create basic tile assets
7. Add sound effects
8. Add items/inventory
9. **Release base game on Steam**

#### Phase 2: DLC Development (Post-Launch)
1. Set up DLC infrastructure
2. Plan Expansion 1 content
3. Develop character pack
4. Create cosmetic options
5. Release DLC on Steam store

---

*Created: 2025-12-19*
*Last Updated: 2025-12-19*
