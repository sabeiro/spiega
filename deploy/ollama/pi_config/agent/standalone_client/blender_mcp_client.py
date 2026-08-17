#!/usr/bin/env python3
"""
Blender MCP Client
Controls running Blender via MCP protocol.
"""

import subprocess
import json

BLENDER_EXE = "/snap/blender/7480/blender"
SCRIPT_FILE = "/tmp/bmcp_script.py"

def add_cube(location=(0, 0, 0)):
    """Add a cube to running Blender."""
    
    script = f'''import bpy
import json
bpy.ops.mesh.primitive_cube_add(location={location})
print("success", json.dumps("✅", "Cube added to running Blender!"))
'''
    
    with open(SCRIPT_FILE, "w") as f:
        f.write(script)
    
    result = subprocess.run(
        [BLENDER_EXE, "--python", SCRIPT_FILE, "--background"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return {
        "status": "ok" if result.stdout.startswith("success") else "unknown",
        "message": result.stdout
    }

if __name__ == "__main__":
    print("Adding cube to running Blender...")
    result = add_cube()
    print(result)
