#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG to 3D Blender Model Converter - Step-by-Step Version

This script breaks down the conversion into separate, testable steps.
Each module can be tested independently.

Usage:
    Step 1: Test only SVG parsing
        blender --background --python svg_parser.py -- --svg-path=diagram.svg
    
    Step 2-5: Combine all steps
    
    Save all steps:
    blender --background --batch svg_to_3d_model_steps.py
"""

import bpy
import sys

# Import individual modules
from svg_parser import parse_svg_paths, SVG_NS
from mesh_exuder import extrude_simple_object, prepare_mesh_for_extrude
from material_applier import apply_material_to_object


def clear_scene():
    """Clear existing scene objects, meshes, and lights."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Clear unused materials
    for mat in list(bpy.data.materials):
        if mat not in bpy.data.objects:
            bpy.data.materials.remove(mat)


def parse_and_convert_svg(svg_path, output_file=None, verbose=True):
    """
    Combined function running all steps.
    Call each step separately for debugging.
    
    Args:
        svg_path: Path to SVG file
        output_file: Output BLEND file path
        verbose: Print debug information
        
    Returns:
        Dictionary mapping object IDs to created objects
    """
    results = {}
    
    if verbose:
        print("Step 1: Parsing SVG file...")
    
    # Step 1: Parse SVG
    paths = parse_svg_paths(svg_path)
    
    if not paths:
        if verbose:
            print("No paths found in SVG file.")
        return {}
    
    if verbose:
        print(f"Step 1 complete. Found {len(paths)} objects in SVG.")
    
    if verbose:
        print("Step 2: Clearing scene...")
    
    # Step 2: Clear scene
    clear_scene()
    
    if verbose:
        print("Step 3: Creating meshes...")
    
    # Step 3: Create meshes from parsed data
    created_objects = {}
    for obj_id, attributes in paths.items():
        # Create mesh
        try:
            from mesh_creator import create_mesh_from_dict
            obj = create_mesh_from_dict(attributes)
        except Exception as e:
            print(f"Error creating mesh for {obj_id}: {e}")
            continue
        
        if obj:
            # Step 4: Extrude mesh
            try:
                extrude_simple_object(
                    obj,
                    depth=attributes.get('extrude_depth', 0.01),
                    segments=2
                )
            except Exception as e:
                print(f"Error extruding {obj_id}: {e}")
                continue
            
            # Step 5: Apply material
            try:
                material = f"svg_material_{obj_id}"
                mat = apply_material_to_object(
                    obj,
                    material,
                    attributes.get('fill', '#333333'),
                    stroke=attributes.get('stroke', '') != 'none',
                    stroke_width=attributes.get('stroke_width', 1.0)
                )
                if mat:
                    obj.data.materials.append(mat)
            except Exception as e:
                print(f"Error applying material to {obj_id}: {e}")
                continue
            
            # Add custom properties
            obj["id"] = obj_id
            created_objects[obj_id] = obj
            
            if verbose:
                print(f"Step 4 complete. Created object: {obj_id}")
    
    # Save if output specified
    if output_file:
        bpy.ops.wm.save_as_mainfile(filepath=str(output_file))
        print(f"Saved to: {output_file}")
    
    return created_objects


if __name__ == "__main__":
    import os
    
    # Check if running from command line
    if os.path.exists('/dev/shm/svg_to_3d_model_steps.py'):
        print("SVG to 3D Model Converter - Step-by-Step")
        print("=" * 50)
        
        # Get SVG path from argument or default
        import sys
        
        if len(sys.argv) > 1:
            svg_path = sys.argv[1]
        else:
            svg_path = "diagram.svg"
        
        print(f"Processing SVG file: {svg_path}")
        
        # Run conversion
        objects = parse_and_convert_svg(svg_path, verbose=True)
        
        if objects:
            print(f"Successfully converted {len(objects)} objects.")
        else:
            print("No objects were created.")
