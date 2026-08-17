#!/usr/bin/env python3
"""
Blender Full API - Complete Blender MCP Client
Provides comprehensive Blender operations via MCP protocol.
"""

import subprocess
import subprocess
import json
import sys
import os

BLENDER_EXE = "/snap/blender/7480/blender"

def add_object(name, location=(0, 0, 0), shape="cube"):
    """
    Add a 3D object to Blender.
    
    Args:
        name: Object name
        location: (x, y, z) tuple
        shape: "cube", "sphere", "torus", "grid"
    
    Returns:
        dict with operation result
    """
    meshes = {
        "cube": "bpy.ops.mesh.primitive_cube_add",
        "sphere": "bpy.ops.mesh.primitive_uvball_add",
        "torus": "bpy.ops.mesh.primitive_torus_add",
        "monkey": "bpy.ops.mesh.primitive_monkey_add",
        "cylinder": "bpy.ops.mesh.primitive_cylinder_add",
        "cone": "bpy.ops.mesh.primitive_cone_add"
    }
    
    if shape not in meshes:
        return {
            "status": "error",
            "message": f"Unknown shape: {shape}"
        }
    
    script = f"""
import bpy

# Create object at {location}
bpy.ops.mesh.primitive_{meshes[shape]}(location={json.dumps(location)})
obj = bpy.context.active_object
obj.name = """ + json.dumps(name) + """

print("✅", "Object added:", obj.name)

objs = bpy.context.scene.objects
print(f"  Total objects: {len(objs)}")
"""
    
    result = subprocess.run(
        [BLENDER_EXE, "--python", "/tmp/bmcp_api.py", "--background"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return {
        "status": "ok",
        "message": result.stdout
    }

def list_objects():
    """List all objects in current Blender scene."""
    script = """
import bpy
objs = bpy.context.scene.objects
print("=" * 50)
print("Current Blender Scene Objects")
print("=" * 50)
for obj in objs:
    print(f"  ✅ {obj.name:20} | Location: {obj.location}")
print("=" * 50)
print(f"Total objects: {len(objs)}")
"""
    
    result = subprocess.run(
        [BLENDER_EXE, "--python", "/tmp/bmcp_api.py", "--background"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return {
        "status": "ok" if "Total objects" in result.stdout else "partial",
        "objects": result.stdout
    }

def get_scene_info():
    """Get detailed scene information."""
    script = """
import bpy
print("Scene Info:")
print("=" * 40)
print(f"Objects: {len(bpy.context.scene.objects)}")
print(f"Mesh Collection: {bpy.context.scene.collection.name}")
print(f"World: {bpy.context.scene.world.name}")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f"  ✅ {obj.name}: {len(obj.data.vertices)} vertices")
"""
    
    result = subprocess.run(
        [BLENDER_EXE, "--python", "/tmp/bmcp_api.py", "--background"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return {
        "status": "ok",
        "message": result.stdout
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "add_cube":
            print(add_object("TestCube", (0, 0, 0), "cube"))
        elif command == "add_sphere":
            print(add_object("TestSphere", (3, 0, 0), "sphere"))
        elif command == "list":
            print(list_objects())
        else:
            print("Unknown command")
    else:
        print("Running Blender API self-test...")
        print("Add Cube:")
        print(add_object("BlenderCube", (0, 0, 0), "cube"))
