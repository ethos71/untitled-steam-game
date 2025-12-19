#!/usr/bin/env python3
"""
Asset downloader for NES-style roguelike game
Downloads free assets from OpenGameArt.org and other free sources
"""

import os
import urllib.request
import zipfile
import json
from pathlib import Path

# Asset sources with direct download links
ASSET_SOURCES = {
    "kenney_pixel_platformer": {
        "url": "https://kenney.nl/content/3-assets/96/roguelikeindoortileset-1.0.zip",
        "type": "sprites",
        "description": "Kenney Roguelike Indoor Tileset"
    },
    "kenney_roguelike_characters": {
        "url": "https://kenney.nl/content/3-assets/11/roguelikecharacterpack-1.1.zip",
        "type": "sprites",
        "description": "Kenney Roguelike Character Pack"
    },
    "pixelart_tileset": {
        "url": "https://opengameart.org/sites/default/files/DungeonTilesetII_0.png",
        "type": "tilesets",
        "description": "Dungeon Tileset from OpenGameArt"
    }
}

def download_file(url, destination):
    """Download a file from URL to destination"""
    print(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"✓ Downloaded to {destination}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract a zip file to destination"""
    print(f"Extracting {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✓ Extracted to {extract_to}")
        os.remove(zip_path)
        return True
    except Exception as e:
        print(f"✗ Failed to extract {zip_path}: {e}")
        return False

def main():
    """Main asset download process"""
    base_path = Path(__file__).parent.parent
    downloads_path = base_path / "downloads"
    downloads_path.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("FREE ASSET DOWNLOADER FOR NES-STYLE ROGUELIKE")
    print("=" * 60)
    print()
    
    # Create asset type directories
    asset_types = ["sprites", "tilesets", "sound", "music"]
    for asset_type in asset_types:
        (base_path / asset_type).mkdir(exist_ok=True)
    
    # Download assets
    for asset_name, asset_info in ASSET_SOURCES.items():
        print(f"\n📦 Processing: {asset_info['description']}")
        
        url = asset_info['url']
        asset_type = asset_info['type']
        
        # Determine file extension
        if url.endswith('.zip'):
            file_path = downloads_path / f"{asset_name}.zip"
            if download_file(url, file_path):
                extract_zip(file_path, base_path / asset_type / asset_name)
        else:
            # Direct file download
            extension = url.split('.')[-1]
            file_path = base_path / asset_type / f"{asset_name}.{extension}"
            download_file(url, file_path)
    
    # Create asset manifest
    manifest = {
        "sources": ASSET_SOURCES,
        "attribution": [
            "Kenney.nl - CC0 License (Public Domain)",
            "OpenGameArt.org - Various CC licenses"
        ],
        "integration_notes": "All assets are free to use. Check individual licenses."
    }
    
    manifest_path = base_path / "asset_manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✓ Asset download complete!")
    print(f"✓ Manifest saved to: {manifest_path}")
    print("=" * 60)
    print("\nFREE ASSET RESOURCES TO EXPLORE:")
    print("  • OpenGameArt.org - Massive collection of CC-licensed assets")
    print("  • Kenney.nl - High-quality CC0 game assets")
    print("  • itch.io/game-assets - Many free and paid asset packs")
    print("  • Freesound.org - Sound effects library")
    print("  • incompetech.com - Royalty-free music by Kevin MacLeod")
    print("  • openpixelproject.com - Pixel art sprites")
    print()

if __name__ == "__main__":
    main()
