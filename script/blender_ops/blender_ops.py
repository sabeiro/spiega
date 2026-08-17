#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for SVG to 3D conversion.

Run with:
    blender --background --batch main.py <svg_file>
"""

import sys
import os
from svg_to_3d_model_steps import parse_and_convert_svg

if __name__ == "__main__":
    if len(sys.argv) > 1:
        svg_path = sys.argv[1]
        result = parse_and_convert_svg(svg_path)
        print(f"Created {len(result)} objects.")
    else:
        print("Usage: blender --background --batch main.py <svg_file>")
