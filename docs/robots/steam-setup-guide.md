# Steam Store Launch Configuration Guide

## Overview
This guide covers the essential configuration needed to launch a game on the Steam store.

## Prerequisites

### 1. Steam Partner Account
- Register at [Steamworks](https://partner.steamgames.com/)
- Pay the $100 USD Steam Direct fee per game
- Complete company/tax verification

### 2. Steam App Configuration
- Create your app in Steamworks
- Note your **App ID** and **Depot ID**
- Configure store page, pricing, and release date

## Configuration Files

### Steam Configuration (`src/steam/steam_config.json`)
Contains your game's Steam-specific settings:
- App ID and depot configuration
- Platform-specific executables
- Branch configuration (default, beta, etc.)

### Required Secrets
Set these in GitHub repository settings:
- `STEAM_USERNAME`: Your Steamworks build account username
- `STEAM_PASSWORD`: Your Steamworks build account password
- `STEAM_APP_ID`: Your game's Steam App ID
- `STEAM_DEPOT_ID`: Your game's depot ID
- `STEAM_CONFIG_VDF`: Optional Steam config for automation

## CI/CD Workflows

### 1. Build and Test (`build-test.yml`)
- Runs on every push/PR to main/develop
- Builds for Windows, Linux, and macOS
- Runs automated tests
- Stores build artifacts

### 2. Steam Deploy (`steam-deploy.yml`)
- Triggers on version tags (e.g., v1.0.0)
- Builds game for all platforms
- Uploads to Steam using SteamCMD
- Supports beta and production branches

## Steam Store Requirements

### Technical Requirements
- **Depots**: Separate builds for each platform
- **Launch Options**: Correct executables for each OS
- **DRM**: Optional Steamworks DRM integration
- **Cloud Saves**: Configure via Steamworks
- **Achievements**: Define in Steamworks portal

### Store Page Requirements
- Game description (min 200 characters)
- At least 5 screenshots (1920x1080 or 3840x2160)
- Capsule images (various sizes)
- Header image (460x215)
- Trailer video (recommended)
- System requirements (min and recommended)
- Age rating
- Content descriptors

### Pre-Launch Checklist
- [ ] Complete store page
- [ ] Upload builds to all required depots
- [ ] Test builds on all platforms
- [ ] Configure pricing and regions
- [ ] Set release date
- [ ] Enable Steam Cloud (if used)
- [ ] Test achievements (if used)
- [ ] Configure Steam Workshop (if used)
- [ ] Set up community features
- [ ] Submit for review

## Steamworks SDK Integration

### Basic Integration
```cpp
// Initialize Steam API
if (!SteamAPI_Init()) {
    // Handle error
    return false;
}

// Your game loop
while (running) {
    SteamAPI_RunCallbacks();
    // Your game logic
}

// Shutdown
SteamAPI_Shutdown();
```

### Key Features to Implement
1. **Steam Overlay**: Enabled by default
2. **Achievements**: Track and unlock via Steam API
3. **Cloud Saves**: Sync player progress
4. **Leaderboards**: Competitive features
5. **Stats**: Track player metrics
6. **Rich Presence**: Show what player is doing

## Deployment Process

### Manual Deployment
1. Build game for all platforms
2. Use SteamCMD or Steamworks GUI
3. Upload to appropriate branch
4. Set build live after testing

### Automated Deployment (GitHub Actions)
1. Tag release: `git tag v1.0.0 && git push --tags`
2. Workflow builds and tests
3. Automatically uploads to Steam
4. Set live on specified branch

## Testing

### Beta Testing
- Use "beta" branch with password
- Share password with testers
- Gather feedback before public release

### Steam Playtest
- Free program for limited-time testing
- Get feedback from players
- Build community before launch

## Post-Launch

### Updates
- Push updates to beta branch first
- Test thoroughly
- Promote to default branch
- Communicate with players via Steam news

### Analytics
- Use Steamworks analytics dashboard
- Track sales, wishlists, and player behavior
- Monitor reviews and feedback

## Resources
- [Steamworks Documentation](https://partner.steamgames.com/doc/home)
- [Steam Direct FAQ](https://partner.steamgames.com/doc/gettingstarted)
- [SteamCMD Documentation](https://developer.valvesoftware.com/wiki/SteamCMD)
- [Steamworks SDK](https://partner.steamgames.com/doc/sdk)

---
*Created: 2025-12-18*
*Last Updated: 2025-12-18*
