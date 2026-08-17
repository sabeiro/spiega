#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG Parser Module
Parses SVG files and extracts paths, rects, circles with attributes.
Can be run standalone to test SVG parsing without Blender.
"""

import xml.etree.ElementTree as ET


# SVG namespace
SVG_NS = 'http://www.w3.org/2000/svg'


def get_path_points(d):
    """Parse SVG path data into list of points."""
    if not d:
        return [[0, 0]]
    
    i = 0
    points = []
    segments = []
    
    while i < len(d):
        cmd = d[i].upper()
        if cmd == 'M':
            points.append([float(d[i+1]), float(d[i+2])])
            segments = [[points[-1]]]
            i += 3
        elif cmd == 'L':
            segments[-1].append([float(d[i+1]), float(d[i+2])])
            i += 3
        elif cmd in ['C', 'S']:
            # Simplify: use line segments for curves
            if i + 9 <= len(d):
                segments[-1].append([float(d[i+8]), float(d[i+9])])
            i += 10
        elif cmd.lower() in ['z', 'close']:
            points.append([points[0][0], points[0][1]])
            i += 1
        else:
            i += 1
    
    if segments:
        points.extend([p for seg in segments for p in seg])
    
    return points[:64]  # Limit points for performance


def parse_svg_paths(svg_path):
    """
    Parse SVG file and extract paths, rects, circles with their attributes.
    
    Args:
        svg_path: Path to the SVG file
        
    Returns:
        Dictionary mapping IDs to object attributes
    """
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing SVG: {e}")
        return {}
    
    paths = {}
    
    # Process path elements
    for elem in root.iter():
        tag = elem.tag.replace(SVG_NS, '')
        
        if tag == 'path':
            d = elem.get('d', '')
            fill = elem.get('fill', '#FFFFFF')
            stroke = elem.get('stroke', 'none')
            stroke_width = float(elem.get('stroke-width', 1)) if elem.get('stroke-width') else 1.0
            
            # Get ID from id attribute or class
            obj_id = elem.get('id')
            if not obj_id:
                class_str = elem.get('class', '')
                if class_str:
                    obj_id = class_str.split()[0]
            
            points = get_path_points(d)
            
            paths[obj_id] = {
                'type': 'path',
                'points': points,
                'fill': fill,
                'stroke': stroke,
                'stroke_width': stroke_width,
                'd': d
            }
        
        elif tag == 'rect':
            x = float(elem.get('x', 0))
            y = float(elem.get('y', 0))
            width = float(elem.get('width', 1))
            height = float(elem.get('height', 1))
            fill = elem.get('fill', '#FFFFFF')
            stroke = elem.get('stroke', 'none')
            stroke_width = float(elem.get('stroke-width', 1)) if elem.get('stroke-width') else 1.0
            
            obj_id = elem.get('id', elem.get('class', '')[:20])
            
            # Create closed rectangle path
            rect_points = [
                [x, y],
                [x + width, y],
                [x + width, y + height],
                [x, y + height],
                [x, y]
            ]
            
            paths[obj_id] = {
                'type': 'rect',
                'points': rect_points,
                'fill': fill,
                'stroke': stroke,
                'stroke_width': stroke_width
            }
        
        elif tag == 'circle':
            cx = float(elem.get('cx', 0))
            cy = float(elem.get('cy', 0))
            r = float(elem.get('r', 10))
            fill = elem.get('fill', '#FFFFFF')
            stroke = elem.get('stroke', 'none')
            stroke_width = float(elem.get('stroke-width', 1)) if elem.get('stroke-width') else 1.0
            
            obj_id = elem.get('id', elem.get('class', '')[:20])
            
            paths[obj_id] = {
                'type': 'circle',
                'cx': cx,
                'cy': cy,
                'r': r,
                'fill': fill,
                'stroke': stroke,
                'stroke_width': stroke_width
            }
    
    return paths
