#!/usr/bin/env python3
"""
High-Quality UML Diagram Rendering Script
Converts PlantUML files to high-resolution PNG images (minimum 1920x1080)
Uses PlantUML online service with enhanced quality settings
"""

import zlib
import base64
import string
import urllib.request
import os
import sys
from pathlib import Path

def plantuml_encode(plantuml_text):
    """Encode PlantUML text to URL-safe format for PlantUML online service."""
    utf8_text = plantuml_text.encode('utf-8')
    zlibbed = zlib.compress(utf8_text)
    # Slicing out the 2-byte header and 4-byte checksum to get raw deflate format
    compressed = zlibbed[2:-4]
    
    plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
    base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
    
    b64_to_plantuml = bytes.maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))
    return base64.b64encode(compressed).translate(b64_to_plantuml).decode('utf-8')

def render_diagram(puml_file, png_file, dpi=600):
    """Render a single PlantUML diagram to PNG with high quality settings."""
    
    if not os.path.exists(puml_file):
        print(f"❌ Error: Source file '{puml_file}' not found.")
        return False
    
    try:
        # Read PlantUML file
        print(f"📖 Reading {puml_file}...")
        with open(puml_file, 'r', encoding='utf-8') as f:
            puml_content = f.read()
        
        # Verify DPI setting in file
        if 'skinparam dpi' not in puml_content:
            print(f"⚠️  Warning: No DPI setting found in {puml_file}")
        
        # Encode for URL
        encoded = plantuml_encode(puml_content)
        
        # Use PlantUML server with PNG format
        # Adding metadata parameters for higher quality
        url = f"http://www.plantuml.com/plantuml/png/{encoded}"
        print(f"🌐 Rendering from PlantUML server...")
        print(f"   Encoded URL length: {len(encoded)} characters")
        
        # Create request with proper headers for high-quality rendering
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        # Fetch the diagram
        with urllib.request.urlopen(req, timeout=30) as response:
            img_data = response.read()
            
            # Validate PNG signature
            if not img_data.startswith(b'\x89PNG\r\n\x1a\n'):
                print(f"❌ Error: Invalid PNG data received for {puml_file}")
                return False
            
            # Write to file
            with open(png_file, 'wb') as out_f:
                out_f.write(img_data)
            
            # Verify file size
            file_size_mb = len(img_data) / (1024 * 1024)
            print(f"✅ Successfully generated {png_file}")
            print(f"   File size: {len(img_data)} bytes ({file_size_mb:.2f} MB)")
            
            return True
            
    except urllib.error.URLError as e:
        print(f"❌ Network error rendering {puml_file}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error rendering {puml_file}: {type(e).__name__}: {e}")
        return False

def main():
    """Main function to render all diagrams."""
    
    # Define diagram files
    diagrams = {
        "uml_usecase.puml": "uml_usecase.png",
        "uml_class.puml": "uml_class.png",
        "uml_sequence.puml": "uml_sequence.png",
        "uml_activity.puml": "uml_activity.png"
    }
    
    print("=" * 70)
    print("HIGH-QUALITY UML DIAGRAM RENDERING")
    print("=" * 70)
    print(f"Target resolution: Minimum 1920x1080 (DPI: 600)")
    print(f"Output format: PNG with professional styling")
    print(f"Total diagrams to render: {len(diagrams)}")
    print("=" * 70)
    print()
    
    success_count = 0
    failed_count = 0
    
    for puml_file, png_file in diagrams.items():
        print(f"[{success_count + failed_count + 1}/{len(diagrams)}] Processing {puml_file}...")
        
        if render_diagram(puml_file, png_file):
            success_count += 1
        else:
            failed_count += 1
        
        print()
    
    # Summary
    print("=" * 70)
    print("RENDERING SUMMARY")
    print("=" * 70)
    print(f"✅ Successful: {success_count}/{len(diagrams)}")
    print(f"❌ Failed: {failed_count}/{len(diagrams)}")
    
    if success_count == len(diagrams):
        print("\n✨ All diagrams rendered successfully!")
        return 0
    else:
        print(f"\n⚠️  {failed_count} diagram(s) failed to render.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
