#!/usr/bin/env python3
"""
Simple script to add a cube to running Blender.
"""

import subprocess
import tempfile

BLENDER_EXE = "/snap/blender/7480/blender"

def add_cube():
    """Add a single cube to the running Blender instance."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
import bpy
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
print("Cube added!")
objs = bpy.context.scene.objects
print(f"Objects before: {len(objs)}")
for obj in objs:
    print(f"  - {obj.name} at {obj.location}")
""")
    
    file_path = f.name
    
    try:
        result = subprocess.run(
            [BLENDER_EXE, "--python=", file_path, "--background"],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout
        
        if "Cube added" in output:
            return {"status": "ok"}
        elif "objects" in output.lower():
            return {"status": "partial"}
        return {"status": "error", "message": output[:500]}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        import os
        if os.path.exists(file_path):
            os.unlink(file_path)

if __name__ == "__main__":
    result = add_cube()
    print(result)
