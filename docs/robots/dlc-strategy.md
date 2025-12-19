# DLC Strategy Guide

## Overview

This document outlines the DLC (Downloadable Content) strategy for the NES-style roguelike.

---

## DLC Philosophy

### Core Principles
1. **Base game is complete** - Players don't need DLC to enjoy the game
2. **Fair pricing** - DLC offers good value for money
3. **Quality content** - Each DLC adds meaningful content
4. **Optional** - No pay-to-win mechanics
5. **Integration** - DLC feels natural, not tacked on

---

## DLC Types

### Major Expansions ($9.99 - $14.99)
- 10-20 hours of new content
- New story chapters
- New areas/dungeons
- New bosses and enemies
- 20-30 new items
- New game mechanics

**Examples**:
- Expansion 1: "The Frozen Wastes"
- Expansion 2: "Shadow Realm"

### Content Packs ($4.99 - $7.99)
- 3-5 hours of new content
- Focused additions
- New character classes
- New dungeon types
- 10-15 new items

**Examples**:
- Character Pack 1: "Heroes of Legend"
- Dungeon Pack 1: "Lost Temples"

### Cosmetic Packs ($1.99 - $4.99)
- Purely visual
- Character skins
- Weapon skins
- Tile set themes
- Sound packs

**Examples**:
- Cosmetic Pack 1: "Pixel Perfect"

---

## DLC Release Timeline

### Pre-Launch (Month 0)
- Plan first year DLC roadmap
- Set up Steam DLC infrastructure
- Begin concept art for Expansion 1

### Post-Launch

**Month 1**: Character Pack 1
- 3 new playable characters
- Quick win for engaged players
- $4.99

**Month 3**: Expansion 1 - "The Frozen Wastes"
- First major expansion
- Ice-themed content
- 15+ new floors
- $9.99

**Month 6**: Dungeon Pack 1
- 3 new dungeon types
- Mid-year content drop
- $5.99

**Month 9**: Expansion 2 - "Shadow Realm"
- Second major expansion
- Shadow-themed content
- Alternate ending
- $12.99

**Month 12**: Cosmetic Pack 1
- Visual upgrades
- Holiday content
- $2.99

---

## Revenue Model

### Base Game
- **Price**: $19.99
- **Sales Goal**: 10,000 copies Year 1
- **Revenue**: $199,900

### DLC Revenue (30% attach rate)
- Character Pack 1: 3,000 × $4.99 = $14,970
- Expansion 1: 3,000 × $9.99 = $29,970
- Dungeon Pack 1: 3,000 × $5.99 = $17,970
- Expansion 2: 3,000 × $12.99 = $38,970
- Cosmetic Pack 1: 3,000 × $2.99 = $8,970
- **Total DLC**: $110,850

### Year 1 Total
- **Combined Revenue**: ~$310,750

---

## Season Pass Strategy

### Bundle Offer
**Season Pass**: $24.99 (30% savings)

**Includes**:
- Expansion 1 ($9.99)
- Expansion 2 ($12.99)
- Character Pack 1 ($4.99)
- Dungeon Pack 1 ($5.99)
- **Total Value**: $33.96
- **Savings**: $8.97

### Benefits
- Upfront revenue
- Committed player base
- Predictable income
- Player loyalty

---

## Technical Implementation

### DLC Detection
```python
class DLCManager:
    def check_dlc_ownership(self):
        """Check Steam for owned DLC."""
        owned = steam_api.get_owned_dlc()
        return owned
```

### Content Gating
```python
def access_dlc_area(area_name):
    """Check if player owns required DLC."""
    if not dlc_manager.owns_dlc(area_name):
        show_purchase_prompt()
        return False
    return True
```

---

## Marketing Strategy

### Pre-Release
- Announce DLC roadmap with base game
- Show teaser art for first expansion
- Build anticipation

### Launch
- Release trailer
- Steam store page
- Community announcement
- Press release

### Post-Launch
- Discount base game when DLC launches
- Bundle deals (base + DLC)
- Steam sales events

---

## Community Engagement

### Feedback Loop
- Listen to player requests
- Community polls for DLC ideas
- Beta testing DLC with engaged players
- Discord/forum discussions

### Free Updates
- Alongside paid DLC, release free updates
- Bug fixes and balance
- Small content additions
- Shows commitment to all players

---

## DLC Content Quality Standards

### Checklist for Each DLC
- [ ] 10+ hours content per $10 spent
- [ ] Integrates seamlessly with base game
- [ ] Tested thoroughly
- [ ] No game-breaking bugs
- [ ] Worth the asking price
- [ ] Positive player reception expected

---

## Legal & Platform Requirements

### Steam DLC Setup
1. Create DLC app ID in Steamworks
2. Set price and release date
3. Upload DLC build
4. Create store page with:
   - Description
   - Screenshots
   - Trailer
   - System requirements

### Ownership Verification
- Use Steam API to check DLC ownership
- Prevent access without purchase
- Handle refunds properly

---

## Risks & Mitigation

### Risk: Low Attach Rate
- **Mitigation**: High quality DLC, fair pricing
- **Target**: 30% attach rate minimum

### Risk: Negative Reception
- **Mitigation**: Community feedback, beta testing
- **Response**: Quick patches, listen to feedback

### Risk: Split Player Base
- **Mitigation**: DLC is optional side content
- **Design**: Multiplayer not affected by DLC

---

## Success Metrics

### Key Performance Indicators (KPIs)
- **DLC Attach Rate**: Target 30-50%
- **Revenue per Player**: Target $30+ lifetime
- **Review Score**: Maintain positive (>80%)
- **Refund Rate**: Keep below 5%

---

## Future DLC Ideas (Year 2+)

### Expansion 3: "The Final Chapter"
- Ultimate endgame content
- New true final boss
- New max level cap
- Price: $14.99

### Character Pack 2: "Legendary Heroes"
- 3 more playable characters
- Advanced difficulty
- Price: $4.99

### Soundtrack DLC
- Full OST for game + DLC
- Wallpapers included
- Price: $4.99

---

*Created: 2025-12-19*
*DLC is optional paid content that extends the game*
