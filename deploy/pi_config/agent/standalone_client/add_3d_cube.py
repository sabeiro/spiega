#!/usr/bin/env python3
"""
Script to add a cube to running Blender instance.
"""

import subprocess

BLENDER_EXE = "/snap/blender/7480/blender"

# Python code to add a cube
CODE = """
import bpy

print(f"📦 Blender {bpy.context.blender_version}")

# Add a cube
bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
print("✅ Cube added")

# Add a sphere
bpy.ops.mesh.primitive_uvball_add(location=(3,0,0))
print("✅ Sphere added")

# Add a plane
bpy.ops.mesh.primitive_circle_add(location=(6,0,0))
bpy.context.object.rotation_euler[2] = 1.57
print("✅ Plane added")

# List all objects
objs = bpy.context.scene.objects
print(f"📋 Objects: {[o.name for o in objs]}")

print("✅ Done!")
"""

print("Adding 3D cubes to Blender...")
print("-" * 50)

result = subprocess.run(
    [BLENDER_EXE, "--python=", "-", "--background"],
    input=CODE,
    capture_output=True,
    text=True,
    timeout=30
)

print("Output:")
print(result.stdout)
if result.stderr:
    print("Errors:")
    print(result.stderr[:2000])
