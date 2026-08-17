#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Blender Extension for Emacs + Ollama/pi-coding-agent

Provides simple Blender tools: add_cube, add_sphere, add_plane
"""

import sys

# Check if we're in Blender's context
BLENDER_AVAILABLE = 'bge.logic' in sys.modules or 'bpy' in sys.modules


def add_cube(
    width=1.0, depth=1.0, height=1.0,
    x=0.0, y=0.0, z=0.0,
    rotation=0.0, name=None
):
    """Add a cube."""
    try:
        import bpy
        
        # Use Blender API
        if name is None:
            name = f"Cube_{len(bpy.data.objects)}"
        
        # Add cube
        obj = bpy.data.objects.new(name, bpy.types.Undefined)
        bpy.context.collection.objects.link(obj)
        
        # Set cube properties
        obj.dimensions = (width, depth, height)
        obj.location = (x, y, z)
        obj.rotation_euler = (rotation, 0, 0)
        
        # Select cube
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_object(action='SELECT', object=obj)
        
        return {
            "status": "ok",
            "type": "real",
            "object": obj,
            "name": name,
            "message": f"Blender: Cube '{name}' added at ({x}, {y}, {z})"
        }
    
    except ImportError:
        return {
            "status": "ok", 
            "type": "simulated",
            "message": "EMACS: Simulation mode (not in Blender)"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Error adding cube: {e}"
        }


def add_sphere(radius=1.0, x=0.0, y=0.0, z=0.0, name=None):
    """Add a sphere."""
    try:
        import bpy
        
        if name is None:
            name = f"Sphere_{len(bpy.data.objects)}"
        
        obj = bpy.data.objects.new(name, bpy.types.Undefined)
        bpy.context.collection.objects.link(obj)
        
        obj.dimensions = (radius, radius, radius)
        obj.type = 'SPHERE'
        obj.location = (x, y, z)
        
        return {
            "status": "ok",
            "type": "real",
            "object": obj,
            "name": name,
            "message": f"Blender: Sphere '{name}' added"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Error adding sphere: {e}"
        }


def add_plane(width=10.0, depth=10.0, x=0.0, y=0.0, z=2.0, rotation_y=0.0, name=None):
    """Add a plane."""
    try:
        import bpy
        
        if name is None:
            name = f"Plane_{len(bpy.data.objects)}"
        
        obj = bpy.data.objects.new(name, bpy.types.Undefined)
        bpy.context.collection.objects.link(obj)
        
        obj.dimensions = (width, depth, depth)
        obj.location = (x, y, z)
        
        # Rotate Y
        obj.rotation_euler = (0, rotation_y, 0)
        
        return {
            "status": "ok",
            "type": "real",
            "object": obj,
            "name": name,
            "message": f"Blender: Plane '{name}' added at ({x}, {y}, {z}) rotated {rotation_y}° Y"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Error adding plane: {e}"
        }


def show_all_objects():
    """Show all objects."""
    try:
        import bpy
        
        objects = [
            {
                "name": obj.name,
                "type": obj.type,
                "location": list(obj.location),
                "dimensions": list(obj.dimensions)
            }
            for obj in bpy.data.objects
        ]
        
        return {
            "status": "ok",
            "type": "real",
            "objects": objects,
            "count": len(objects)
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Error showing objects: {e}"
        }


def demo():
    """Run demo."""
    result = add_cube(width=2.0, depth=2.0, height=2.0, x=5.0, y=5.0, z=5.0, rotation=45.0, name="MyCube")
    print(f"{result}")
    
    result = add_sphere(radius=1.5, x=0.0, y=0.0, z=0.0, name="MySphere")
    print(f"{result}")
    
    result = add_plane(width=8.0, depth=8.0, x=0.0, y=0.0, z=2.0, rotation_y=45.0, name="MyPlane")
    print(f"{result}")
    
    return show_all_objects()


if __name__ == "__main__":
    import json
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true', help='Run demo')
    parser.add_argument('--add-cube', action='store_true', help='Add cube')
    parser.add_argument('--add-sphere', action='store_true', help='Add sphere')
    parser.add_argument('--add-plane', action='store_true', help='Add plane')
    parser.add_argument('--width', type=float, default=1.0)
    parser.add_argument('--depth', type=float, default=1.0)
    parser.add_argument('--height', type=float, default=1.0)
    parser.add_argument('--radius', type=float, default=1.0)
    parser.add_argument('--location-x', type=float, default=0.0)
    parser.add_argument('--location-y', type=float, default=0.0)
    parser.add_argument('--location-z', type=float, default=0.0)
    parser.add_argument('--rotation', type=float, default=0.0)
    parser.add_argument('--rotation-y', type=float, default=0.0)
    parser.add_argument('--name', default=None)
    parser.add_argument('--show', action='store_true', help='Show objects')
    parser.add_argument('--clear', action='store_true', help='Clear')
    
    args = parser.parse_args()
    
    if args.add_cube:
        result = add_cube(width=args.width, depth=args.depth, height=args.height,
                         x=args.location_x, y=args.location_y, z=args.location_z,
                         rotation=args.rotation, name=args.name)
        print(json.dumps(result, indent=2))
    
    elif args.add_sphere:
        result = add_sphere(radius=args.radius,
                           x=args.location_x, y=args.location_y, z=args.location_z,
                           name=args.name)
        print(json.dumps(result, indent=2))
    
    elif args.add_plane:
        result = add_plane(width=args.width, depth=args.depth,
                          x=args.location_x, y=args.location_y, z=args.location_z,
                          rotation_y=args.rotation_y, name=args.name)
        print(json.dumps(result, indent=2))
    
    elif args.show:
        result = show_all_objects()
        print(json.dumps(result, indent=2))
    
    elif args.demo:
        result = demo()
        print(json.dumps(result, indent=2))
    
    elif args.clear:
        try:
            import bpy
            for obj in bpy.data.objects:
                bpy.data.objects.unlink(obj)
            result = {"status": "ok", "message": "Cleared all objects"}
        except:
            result = {"status": "error", "error": "Blender not available"}
        print(json.dumps(result, indent=2))
    
    else:
        print("--demo, --help")
        parser.print_help()
