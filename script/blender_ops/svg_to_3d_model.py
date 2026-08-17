#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG to 3D Blender Model Converter

This script loads SVG diagram files, converts SVG paths to Blender meshes,
extrudes and bevels the objects, and applies materials based on ID types.

Usage:
    blender --background --python svg_to_3d_model.py -- --svg-path=diagram.svg --output=model.blend
"""

import bpy
import math
import mathutils
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

# SVG namespace
SVG_NS = 'http://www.w3.org/2000/svg'


def clear_scene():
    """Clear existing scene objects, meshes, and lights."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Clear unused materials
    for mat in list(bpy.data.materials):
        if mat not in bpy.data.objects:
            bpy.data.materials.remove(mat)


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
    
    # Helper function to convert path data to points
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


def create_planar_mesh(points):
    """Create a planar mesh from a list of points (closed polygon)."""
    if not points or len(points) < 3:
        return None
    
    # Limit vertices for performance
    max_verts = 512
    points = points[:max_verts]
    
    bpy.ops.mesh.primitive_uv_grid(0, 0, type='NEW')
    bpy.ops.object.delete()
    
    vertices = []
    for px, py in points:
        vertices.append(mathutils.Vector((px, py, 0)))
    
    # Create mesh
    mesh = bpy.data.meshes.new("SVG_Polygon")
    obj = bpy.data.objects.new("SVG_Polygon", mesh)
    bpy.context.collection.objects.link(obj)
    
    # Generate UV grid and triangulate
    mesh.from_pydata(
        vertices=[v.co for v in vertices],
        edges=[(i, (i + 1) % len(vertices)) for i in range(len(vertices) - 1)] + [(len(vertices) - 1, 0)],
        faces=[[i, (i + 1) % len(vertices), (i + 2) % len(vertices)] for i in range(len(vertices))]
    )
    mesh.update()
    
    return obj


def create_circle_mesh(cx, cy, radius):
    """Create a circle mesh with circular vertices."""
    # Create circle using primitive
    bpy.ops.mesh.primitive_circle(num_segments=32)
    circle_obj = bpy.context.object
    
    circle_obj.location = (cx, cy, 0)
    circle_obj.scale = (radius, radius, 1)
    
    bpy.context.view_layer.objects.active = circle_obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    return circle_obj


def create_mesh_from_dict(points_data):
    """Create mesh from parsed SVG object data (path, rect, etc)."""
    if not points_data:
        return None
    
    point_type = points_data.get('type', 'path')
    
    if point_type == 'path':
        return create_planar_mesh(points_data.get('points', [[0, 0]]))
    elif point_type == 'rect':
        # Rect has special handling
        points = points_data.get('points', [[0, 0], [1, 0], [1, 1], [0, 1]])
        return create_planar_mesh(points)
    elif point_type == 'circle':
        return create_circle_mesh(
            points_data.get('cx', 0),
            points_data.get('cy', 0),
            points_data.get('r', 10)
        )
    
    return None


def prepare_mesh_for_extrude(obj, depth=0.1, segments=2):
    """Prepare mesh object for extrusion with bevel."""
    if not obj or not obj.data:
        return False
    
    # Set bevel settings
    obj.data.bevel_depth = depth * 0.1
    obj.data.bevel_resolution = segments
    obj.data.use_bevel = True
    
    # Scale to proper dimensions
    scale_y = 0.02  # Scale for extrusion
    obj.scale = (1, scale_y, 1)
    
    obj.data.update()
    return True


def apply_material(mat_name, fill_color, stroke=False, stroke_width=1.0):
    """
    Create shader nodes and assign material.
    
    Args:
        mat_name: Material name (will be appended with ID if duplicate)
        fill_color: Fill color (rgb tuple or hex string)
        stroke: Whether to add stroke/glossy layer
        stroke_width: Stroke thickness
        
    Returns:
        Assigned material
    """
    mat = None
    
    color = fill_color
    if isinstance(fill_color, str):
        if fill_color.startswith('#') and len(fill_color) >= 7:
            hex_color = fill_color[3:7].upper()
            color = [
                int(hex_color[0:2], 16) / 255.0,
                int(hex_color[2:4], 16) / 255.0,
                int(hex_color[4:6], 16) / 255.0
            ]
        else:
            color = [0.3, 0.3, 0.3]
    
    # Create or get material
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(name=mat_name)
    
    mat.use_nodes = True
    outputs = mat.node_tree.nodes.get('Output Material')
    if not outputs:
        outputs = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
        outputs.is_active = True
    
    # Create Principled BSDF
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if not bsdf:
        bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.inputs['base_color'].default_color = color
        bsdf.inputs['alpha'].default_value = 1.0
    
    # Ensure connection
    if not bsdf.outputs['bsdf'].links:
        connections = mat.node_tree.links.new(
            bsdf.outputs['bsdf'],
            outputs.inputs['surface']
        )
    
    # Apply glossy node for stroke
    if stroke:
        glossy = mat.node_tree.nodes.get('Glossy BSDF')
        if not glossy:
            glossy = mat.node_tree.nodes.new('ShaderNodeBsdfGlossy')
        glossy.inputs['color'].default_color = (0.1, 0.1, 0.1, 1.0)
        
        # Add glossy only for objects with stroke
        if stroke_width > 0:
            mix = mat.node_tree.nodes.get('Mix Shader')
            if not mix:
                pass  # Skip mixing for simplicity
    
    return mat


def main(svg_path, output_path=None, scale=1, extrude_depth=0.1, bevel_segments=2):
    """
    Main function to convert SVG diagram to 3D Blender model.
    
    Args:
        svg_path: Path to SVG file
        output_path: Output blend file path (optional)
        scale: Overall scale factor
        extrude_depth: Extrusion depth
        bevel_segments: Bevel segments for smoothness
        
    Returns:
        Dictionary of created objects with their IDs
    """
    # Clear existing scene
    clear_scene()
    
    # Parse SVG
    svg_paths = parse_svg_paths(svg_path)
    
    if not svg_paths:
        print("No paths found in SVG file.")
        return {}
    
    print(f"Found {len(svg_paths)} objects in SVG.")
    
    # Create objects
    created_objects = {}
    
    for obj_id, attributes in svg_paths.items():
        # Create planar mesh
        obj = create_mesh_from_dict(attributes)
        
        if obj:
            # Prepare for extrusion
            prepare_mesh_for_extrude(obj, depth=extrude_depth * scale)
            
            # Apply material
            material = f"svg_material_{obj_id}"
            mat = apply_material(
                material,
                attributes.get('fill', '#333333'),
                stroke=attributes.get('stroke', '') != 'none',
                stroke_width=attributes.get('stroke_width', 1.0)
            )
            if mat:
                obj.data.materials.append(mat)
            
            # Add custom properties for tracking
            obj.id = obj_id
            obj['extrude_depth'] = extrude_depth
            
            created_objects[obj_id] = obj
            print(f"Created object: {obj_id}")
    
    # Set active collection and save if output specified
    if output_path:
        bpy.context.view_layer.objects.active = created_objects.get('Main', created_objects.values().__iter__().__next__()) if created_objects else None
        bpy.context.scene.collection = created_objects.values().__iter__().__next__().collection if created_objects else bpy.data.collections[0]
        
        bpy.ops.export_scene.blend_file(
            filepath=str(output_path),
            use_border=True,
            use_init=False,
            use_legacy=False,
            use_selection=False,
            save_all=True
        )
    
    return created_objects


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert SVG diagram to 3D Blender model")
    parser.add_argument("--svg-path", type=str, required=True, help="Path to SVG file")
    parser.add_argument("--output", type=str, help="Output BLEND file path")
    parser.add_argument("--scale", type=float, default=1.0, help="Scale factor")
    parser.add_argument("--extrude", type=float, default=0.1, help="Extrusion depth")
    parser.add_argument("--bevel", type=int, default=2, help="Bevel segments")
    
    args = parser.parse_args()
    
    main(
        args.svg_path,
        args.output,
        args.scale,
        args.extrude,
        args.bevel
    )
