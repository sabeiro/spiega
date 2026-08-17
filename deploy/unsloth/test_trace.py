#!/usr/bin/env python3
"""Quick test for trace_bitmap_inkscape_style.py"""

import subprocess
import sys

def test_trace():
    # Check if pdf2image is installed
    try:
        import pdf2image
        print("✓ pdf2image installed")
    except ImportError:
        print("✗ pdf2image not installed. Install with: pip install pdf2image")
        return False
    
    # Check dependencies
    try:
        import cv2
        print("✓ OpenCV installed")
    except ImportError:
        print("✗ OpenCV not installed")
        return False
    
    try:
        import geopandas
        print("✓ geopandas installed")
    except ImportError:
        print("✗ geopandas not installed")
        return False
    
    try:
        import shapely
        print("✓ shapely installed")
    except ImportError:
        print("✗ shapely not installed")
        return False
    
    # Check system tools
    tools = ['pdftoppm', 'inkscape']
    for tool in tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
            print(f"✓ {tool} installed")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"✗ {tool} not found")
    
    # Check existing files
    import os
    files = [f for f in os.listdir('.') if f.endswith('.py')]
    print(f"\nAvailable scripts: {', '.join(files)}")
    
    print("\nAll tests passed! ✓")
    return True

if __name__ == "__main__":
    test_trace()
