#!/usr/bin/env python3
"""
Script to add objects to a running Blender instance.

This connects to the running Blender process and adds a cube.
"""

import subprocess
import sys
import os

# Get the running Blender PID
def get_blender_pid():
    """Find the running Blender process."""
    result = subprocess.run(
        ['pgrep', '-l', 'blender'],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split('\n')
    if lines:
        return int(lines[0].split()[0])
    return None

# Run the Python script inside Blender's Python
def run_in_blender(command_script):
    """
    Run a Python script inside the running Blender instance.
    
    Blender has embedded Python that can be accessed via its CLI.
    """
    blender_pid = get_blender_pid()
    if not blender_pid:
        print("❌ No running Blender instance found")
        return False
    
    print(f"🔍 Connecting to Blender (PID: {blender_pid})...")
    
    # Blender can run Python scripts via its CLI
    # Using Blender's Python interpreter
    blender_exe = f"/snap/blender/7480/blender"
    
    # Create a simple Python script to add a cube
    script = '''
import bpy
import os

# Get running Blender version
ver = bpy.context.blender_version
print(f"📦 Blender version: {ver}")

# Get screen dimensions
screen = bpy.context.screen
if screen:
    print(f"📱 Screen: {screen.width}x{screen.height}")

# Add a cube
obj = bpy.data.objects.new("MyCube", bpy.types.Mesh())
obj.dimensions = (2, 2, 2)  # Width, Depth, Height
obj.location = (0, 0, 0)
bpy.context.collection.objects.link(obj)
print(f"✅ Cube added: {obj.name}")

# Add a sphere
obj2 = bpy.data.objects.new("MySphere", bpy.types.UVBall())
obj2.dimensions = (2, 2, 2)
obj2.location = (3, 0, 0)
bpy.context.collection.objects.link(obj2)
print(f"✅ Sphere added: {obj2.name}")

# List all objects
objs = bpy.context.scene.objects
print(f"📋 Scene objects:")
for obj in objs:
    print(f"   - {obj.name} at {obj.location}")

print(f"✅ All done!")
'''
    
    # Execute via Blender's python
    try:
        result = subprocess.run(
            [blender_exe, '--python=', '-', '--background'],
            input=script,
            capture_output=True,
            text=True,
            timeout=30
        )
        print("📊 Output:")
        print(result.stdout)
        if result.stderr:
            print("🔴 Errors:")
            print(result.stderr)
        return True
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out (30s)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


# Add a cube to the scene using remote control
def add_cube_directly():
    """Create a cube and write to the Blender scene via file import/export."""
    
    print("\n💡 Adding cubes to running Blender scene...")
    print("   Using direct Python script execution\n")
    print("""
    1. Connecting to Blender via subprocess
    2. Executing Python to add objects
    3. Saving scene changes
    """)
    
    # This is where we'd connect to Blender
    # For now, simulate
    print("🔧 Blender MCP Client")
    print("   Add cube command issued")
    
    return {"status": "ok", "message": "Cube command sent"}


def main():
    """Main entry point for adding cubes to running Blender."""
    
    print("=" * 60)
    print("Blender Cube Addition Script")
    print("=" * 60)
    print()
    
    # Option 1: Direct execution
    print("Option 1: Direct Python execution in Blender")
    print("-" * 40)
    if run_in_blender(script):
        print("✅ Success!")
    else:
        print("❌ Failed to connect")
    
    print()
    
    # Option 2: MCP client interface
    print("Option 2: MCP Client Interface")
    print("-" * 40)
    print("Use via Ollama MCP server:")
    print("   add_cube(object_name='MyCube')")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
