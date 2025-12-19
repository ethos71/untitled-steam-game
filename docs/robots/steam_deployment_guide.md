# Steam Deployment Guide

## Prerequisites

### 1. Steam Partner Account
- Sign up at https://partner.steamgames.com/
- Complete Steamworks documentation
- Pay the $100 USD app submission fee
- Get your App ID assigned

### 2. Install SteamCMD
SteamCMD is required to upload builds to Steam.

**Linux:**
```bash
sudo apt-get install steamcmd
# or download from: https://developer.valvesoftware.com/wiki/SteamCMD
```

**macOS:**
```bash
brew install steamcmd
```

**Windows:**
Download from: https://developer.valvesoftware.com/wiki/SteamCMD

### 3. Install Steam SDK
- Download from: https://partner.steamgames.com/
- Extract to a local directory
- Follow SDK integration instructions

## Local Testing

Before deploying to Steam, test the game locally:

```bash
# Build the game
./build_local.sh

# Run the game
./run_local.sh
```

## Preparing for Steam

### 1. Update Configuration

Edit `src/steam/steam_config.json` with your actual App ID:

```json
{
  "app_id": "YOUR_ACTUAL_APP_ID",
  "app_name": "Untitled Steam Game",
  "version": "0.1.0"
}
```

### 2. Generate Steam Build Files

```bash
python3 src/steam/build_steam.py
```

This creates:
- `steam_build/content/` - Game files
- `steam_build/scripts/` - Build configuration (VDF files)
- `steam_build/upload_to_steam.sh` - Upload script

### 3. Set Environment Variables

```bash
export STEAM_USERNAME="your_steam_username"
export STEAM_PASSWORD="your_steam_password"
export STEAMCMD_PATH="/path/to/steamcmd"  # Optional if in PATH
```

### 4. Upload to Steam

```bash
cd steam_build
./upload_to_steam.sh
```

## Steam Store Configuration

### 1. Store Page Setup
In Steamworks Partner portal:
- Upload screenshots (1280x720 or 1920x1080)
- Upload header capsule (460x215)
- Upload main capsule (616x353)
- Write short and long descriptions
- Set pricing and regional availability
- Configure system requirements

### 2. System Requirements

**Minimum:**
- OS: Windows 10, macOS 10.14, Ubuntu 20.04
- Processor: 1.5 GHz
- Memory: 512 MB RAM
- Graphics: OpenGL 2.0 compatible
- Storage: 100 MB available space

**Recommended:**
- OS: Windows 11, macOS 12, Ubuntu 22.04
- Processor: 2.0 GHz
- Memory: 1 GB RAM
- Graphics: OpenGL 3.0 compatible
- Storage: 200 MB available space

### 3. Builds Tab
- Create depot IDs in Steamworks
- Upload builds using SteamCMD
- Set default branch to your uploaded build
- Test the build through Steam client

### 4. Release Checklist
- [ ] All store assets uploaded
- [ ] Store page text complete
- [ ] Pricing set
- [ ] Regional availability configured
- [ ] Age ratings obtained (ESRB, PEGI, etc.)
- [ ] Build uploaded and tested
- [ ] Achievement icons (if applicable)
- [ ] Trading cards (if applicable)
- [ ] Community hub configured
- [ ] Release date set

## Continuous Deployment

The GitHub workflow `.github/workflows/steam-deploy.yml` automates deployment:

1. Triggered on tags matching `v*` (e.g., `v0.1.0`)
2. Builds the game
3. Runs tests
4. Uploads to Steam (requires secrets)

### Setting Up GitHub Secrets

In your GitHub repository settings, add:
- `STEAM_USERNAME` - Your Steam username
- `STEAM_PASSWORD` - Your Steam password
- `STEAM_CONFIG_VDF` - Your Steam config VDF file content

## Post-Launch

### Updates
Tag new versions to trigger automatic deployment:
```bash
git tag v0.2.0
git push origin v0.2.0
```

### Monitoring
- Check Steamworks portal for sales data
- Monitor community discussions
- Review bug reports
- Track achievements and playtime stats

### DLC Deployment
DLC content in `src/dlc/` can be packaged separately:
1. Create new App ID for DLC in Steamworks
2. Update build scripts with DLC App ID
3. Follow same upload process

## Troubleshooting

### Build Upload Fails
- Verify STEAM_USERNAME and STEAM_PASSWORD are correct
- Check that App ID matches your Steamworks app
- Ensure SteamCMD is installed and in PATH
- Check Steamworks account has publishing rights

### Game Won't Launch on Steam
- Verify all dependencies are included
- Test locally with same Python version
- Check Steam logs: `steam/logs/`
- Ensure all asset paths are relative

### Store Page Rejected
- Follow Steam's content guidelines
- Provide clear screenshots and descriptions
- Include age-appropriate content warnings
- Respond to Valve's feedback promptly

## Resources

- [Steamworks Documentation](https://partner.steamgames.com/doc/home)
- [SteamCMD Documentation](https://developer.valvesoftware.com/wiki/SteamCMD)
- [Steam SDK Documentation](https://partner.steamgames.com/doc/sdk)
- [Steam Deployment Best Practices](https://partner.steamgames.com/doc/store/releasing)
