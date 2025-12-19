#!/usr/bin/env python3
"""
Steam build preparation script
Prepares the game for Steam deployment using SteamCMD and Steam SDK
"""

import json
import os
import sys
import shutil
from pathlib import Path

def create_steam_build_scripts():
    """Create Steam build configuration files"""
    
    # Load steam config
    config_path = Path(__file__).parent / "steam_config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    app_id = config['app_id']
    
    # Create build directory
    build_dir = Path(__file__).parent.parent.parent / "steam_build"
    build_dir.mkdir(exist_ok=True)
    
    # Create content directory
    content_dir = build_dir / "content"
    content_dir.mkdir(exist_ok=True)
    
    # Create scripts directory
    scripts_dir = build_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    
    # Copy game files to content directory
    src_dir = Path(__file__).parent.parent
    for item in ['assets', 'characters', 'dlc', 'engine', 'environment', 'mods', 'story']:
        src_path = src_dir / item
        if src_path.exists():
            dst_path = content_dir / item
            if dst_path.exists():
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
    
    # Copy main files
    shutil.copy(src_dir.parent / "main.py", content_dir / "main.py")
    shutil.copy(src_dir.parent / "requirements.txt", content_dir / "requirements.txt")
    
    # Create app build VDF
    app_build_vdf = scripts_dir / f"app_build_{app_id}.vdf"
    vdf_content = f'''"AppBuild"
{{
    "AppID" "{app_id}"
    "Desc" "Build for Untitled Steam Game"
    "ContentRoot" "../content/"
    "BuildOutput" "../output/"
    "SetLive" "default"
    
    "Depots"
    {{
        "{app_id + 1}"
        {{
            "FileMapping"
            {{
                "LocalPath" "*"
                "DepotPath" "."
                "Recursive" "1"
            }}
        }}
    }}
}}
'''
    
    with open(app_build_vdf, 'w') as f:
        f.write(vdf_content)
    
    # Create depot build VDF
    depot_build_vdf = scripts_dir / f"depot_build_{app_id + 1}.vdf"
    depot_content = f'''"DepotBuildConfig"
{{
    "DepotID" "{app_id + 1}"
    "ContentRoot" "../content/"
    "FileMapping"
    {{
        "LocalPath" "*"
        "DepotPath" "."
        "Recursive" "1"
    }}
    "FileExclusion" "*.pdb"
}}
'''
    
    with open(depot_build_vdf, 'w') as f:
        f.write(depot_content)
    
    # Create upload script
    upload_script = build_dir / "upload_to_steam.sh"
    upload_content = f'''#!/bin/bash
# Upload build to Steam using SteamCMD
# Prerequisites:
# 1. Install SteamCMD: https://developer.valvesoftware.com/wiki/SteamCMD
# 2. Set STEAMCMD_PATH environment variable or install to /usr/local/bin/steamcmd
# 3. Set STEAM_USERNAME and STEAM_PASSWORD environment variables

STEAMCMD="${{STEAMCMD_PATH:-steamcmd}}"
USERNAME="${{STEAM_USERNAME}}"
PASSWORD="${{STEAM_PASSWORD}}"

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
    echo "Error: STEAM_USERNAME and STEAM_PASSWORD environment variables must be set"
    exit 1
fi

echo "Uploading to Steam..."
$STEAMCMD +login "$USERNAME" "$PASSWORD" \\
    +run_app_build "$(pwd)/scripts/app_build_{app_id}.vdf" \\
    +quit

echo "Upload complete!"
'''
    
    with open(upload_script, 'w') as f:
        f.write(upload_content)
    
    os.chmod(upload_script, 0o755)
    
    print(f"Steam build files created in: {build_dir}")
    print(f"\\nNext steps:")
    print(f"1. Test the game locally: ./run_local.sh")
    print(f"2. Set up Steam Partner account and get App ID")
    print(f"3. Update app_id in src/steam/steam_config.json")
    print(f"4. Install SteamCMD: https://developer.valvesoftware.com/wiki/SteamCMD")
    print(f"5. Set environment variables: STEAM_USERNAME, STEAM_PASSWORD")
    print(f"6. Run: cd steam_build && ./upload_to_steam.sh")

if __name__ == "__main__":
    create_steam_build_scripts()
