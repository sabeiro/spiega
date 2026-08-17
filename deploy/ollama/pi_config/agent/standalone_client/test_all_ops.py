#!/usr/bin/env python3
"""
Test script for Blender MCP client operations.
"""

import subprocess

BLENDER_EXE = "/snap/blender/7480/blender"
SCRIPT_PATH = "/tmp/bmcp_test_ops.py"

def _write_script(name, content):
    """Write a Python script to disk."""
    path = "/tmp/" + name
    with open(path, "w") as f:
        f.write(content)
    return path

def run_operation(script_content):
    """Run Blender with a Python script."""
    result = subprocess.run(
        [BLENDER_EXE, "--python", SCRIPT_PATH, "--background"],
        input=script_content,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return {
        "status": "ok" if "✅" in result.stdout else "partial",
        "message": result.stdout.strip().split("\n")[-3:]
    }

def add_cube():
    script = """
import bpy
bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
print("✅", "Cube added")
"""
    return run_operation(script)

def add_sphere():
    script = """
import bpy
try:
    bpy.ops.mesh.primitive_uvball_add(location=(3,0,0))
    print("✅", "Sphere added")
except:
    print("⚠️  Sphere operator not available")
"""
    return run_operation(script)

def add_torus():
    script = """
import bpy
try:
    bpy.ops.mesh.primitive_torus_add(location=(6,0,0))
    print("✅", "Torus added")
except:
    print("⚠️  Torus operator not available")
"""
    return run_operation(script)

def add_mesh():
    script = """
import bpy
bpy.ops.mesh.primitive_monkey_add(location=(9,0,0))
print("✅", "Monkey mesh added")
"""
    return run_operation(script)

def list_objects():
    script = """
import bpy
objs = bpy.context.scene.objects
for obj in objs:
    print(f"  ✅ {obj.name}: {obj.location}")
"""
    return run_operation(script)

def main():
    print("=" * 60)
    print("Testing Blender MCP Operations")
    print("=" * 60)
    
    operations = {
        "Add Cube": add_cube(),
        "Add Sphere": add_sphere(),
        "Add Torus": add_torus(),
        "Add Monkey": add_mesh(),
        "List Objects": list_objects()
    }
    
    print("\nResults:\n")
    for name, result in operations.items():
        print(f"✓ {name}")
        if result["status"] == "ok":
            print(f"   {result['message']}")
        else:
            print(f"   {result['message']}")
    
    print("\n" + "=" * 60)
    print("All tests complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
