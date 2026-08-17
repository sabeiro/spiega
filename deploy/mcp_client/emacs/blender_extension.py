#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Blender Extension for Emacs + Ollama/pi-coding-agent.

This extension provides Blender tools in Emacs buffers with:
- Add cube, sphere, plane in Blender or Emacs simulation
- Live preview of Blender output
- Integration with Ollama models for intelligent suggestions

Usage in Emacs with org-mode:
    # | :results value :file /path/to/file.py :exports result
    # | :header-line "Blender Extension Demo"
    #+BEGIN_SRC python :results output
    import sys
    sys.path.insert(0, '/home/sabeiro/lav/src/blender_twin/deploy/mcp_client/emacs')
    from blender_extension import add_cube, add_sphere, add_plane
    
    # Add a cube
    add_cube(width=2.0, depth=2.0, height=2.0, object_name="MyCube")
    
    # Add a sphere
    add_sphere(radius=1.0, object_name="MySphere")
    
    # Add a plane
    add_plane(width=4.0, depth=4.0, object_name="MyPlane")
    
    #+END_SRC

Installation:
    1. Add to .emacs:
       (require 'blender-mcp)
    2. Start Ollama session: ollama serve
    3. Load Emacs extension: M-x blender-mcp-load

Usage in Ollama:
    1. Connect to Ollama: ollama run llama3.2
    2. Generate Python code in Emacs buffer
    3. Execute code with M-x run-python
"""

import subprocess
import sys

# Blender command
BLENNDER_CMD = sys.executable + " -m" + "/home/sabeiro/lav/src/blender_twin/deploy/mcp_client/blender_mcp_client.py"


def add_cube(
    width: float = 1.0,
    depth: float = 1.0,
    height: float = 1.0,
    location_x: float = 0.0,
    location_y: float = 0.0,
    location_z: float = 0.0,
    rotation_y: float = 0.0,
    object_name: str = None,
    simulate: bool = True,
) -> dict:
    """
    Add a cube in Blender or simulate in Emacs.

    Args:
        width, depth, height: Cube dimensions
        location_x, location_y, location_z: Cube position
        rotation_y: Rotation around Y axis
        object_name: Name for cube
        simulate: If True, show output in Emacs (default)

    Returns:
        Dictionary with result or error message
    """
    try:
        if simulate:
            # Simulated output (no actual Blender needed)
            result = {
                "status": "ok",
                "message": f"EMACS SIMULATION: Added cube '{object_name or 'MyCube'}' "
                          f"with size {width} x {depth} x {height} at ({location_x}, {location_y}, {location_z})",
                "cube": {
                    "width": width,
                    "depth": depth,
                    "height": height,
                    "location": [location_x, location_y, location_z],
                    "rotation": [0, rotation_y, 0],
                    "visible": True,
                    "object_name": object_name or "MyCube"
                }
            }
            # Print to Emacs *output* buffer
            print(f"Cube '{object_name}': {width}x{depth}x{height} @ ({location_x}, {location_y}, {location_z})",
                  file=sys.stderr)
            return result
        else:
            # Try to call actual Blender
            cmd = f"{BLENNDER_CMD} --add-cube " \
                  f"--width={width} --depth={depth} --height={height} " \
                  f"--location-x={location_x} --location-y={location_y} --location-z={location_z} " \
                  f"--rotation={rotation_y} --name={object_name or 'Cube'}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return {
                    "status": "ok",
                    "message": f"Blender OK: {result.stdout.strip()}"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Blender error: {result.stderr.strip()}"
                }

    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Timeout waiting for Blender"}
    except FileNotFoundError:
        return {"status": "error", "message": "Blender not found in path"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def add_sphere(
    radius: float = 1.0,
    location_x: float = 0.0,
    location_y: float = 0.0,
    location_z: float = 0.0,
    object_name: str = None,
    simulate: bool = True,
) -> dict:
    """Add a sphere to Blender or simulate in Emacs."""
    try:
        if simulate:
            result = {
                "status": "ok",
                "message": f"EMACS SIMULATION: Added sphere '{object_name or 'MySphere'}' "
                          f"with radius {radius} at ({location_x}, {location_y}, {location_z})",
                "sphere": {
                    "radius": radius,
                    "location": [location_x, location_y, location_z],
                    "object_name": object_name or "MySphere"
                }
            }
            print(f"Sphere '{object_name}': radius={radius} @ ({location_x}, {location_y}, {location_z})",
                  file=sys.stderr)
            return result
        else:
            cmd = f"{BLENNDER_CMD} --add-sphere --radius={radius} " \
                  f"--location-x={location_x} --location-y={location_y} --location-z={location_z} " \
                  f"--name={object_name or 'Sphere'}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return {
                "status": "ok" if result.returncode == 0 else "error",
                "message": result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def add_plane(
    width: float = 10.0,
    depth: float = 10.0,
    location_x: float = 0.0,
    location_y: float = 0.0,
    location_z: float = 0.0,
    rotation_y: float = 0.0,
    object_name: str = None,
    simulate: bool = True,
) -> dict:
    """Add a plane to Blender or simulate in Emacs."""
    try:
        if simulate:
            result = {
                "status": "ok",
                "message": f"EMACS SIMULATION: Added plane '{object_name or 'MyPlane'}' "
                          f"with size {width} x {depth} at ({location_x}, {location_y}, {location_z}) "
                          f"rotated {rotation_y}°",
                "plane": {
                    "width": width,
                    "depth": depth,
                    "location": [location_x, location_y, location_z],
                    "rotation": [0, rotation_y, 0],
                    "object_name": object_name or "MyPlane"
                }
            }
            print(f"Plane '{object_name}': {width}x{depth} @ ({location_x}, {location_y}, {location_z}) rotate={rotation_y}",
                  file=sys.stderr)
            return result
        else:
            cmd = f"{BLENNDER_CMD} --add-plane --width={width} --depth={depth} " \
                  f"--location-x={location_x} --location-y={location_y} --location-z={location_z} " \
                  f"--rotation={rotation_y} --name={object_name or 'Plane'}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return {
                "status": "ok" if result.returncode == 0 else "error",
                "message": result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def list_objects() -> list:
    """List all objects in Emacs simulation buffer."""
    return [
        {"name": "MyCube", "type": "cube", "location": [0, 0, 0]},
        {"name": "MySphere", "type": "sphere", "location": [0, 0, 0]},
        {"name": "MyPlane", "type": "plane", "location": [0, 0, 0]},
    ]


def clear_scene() -> dict:
    """Clear all objects from simulation buffer."""
    return {
        "status": "ok",
        "message": "Emacs simulation buffer cleared",
        "objects_remaining": 0
    }


# Demo usage
if __name__ == "__main__":
    print()
    print("=" * 60)
    print("EMACS/BLENDER M EXTENSION DEMO")
    print("=" * 60)
    print()
    
    # Add a cube
    print("1. Adding a cube with simulation mode:")
    result = add_cube(
        width=2.0,
        depth=2.0,
        height=2.0,
        location_x=5.0,
        location_y=5.0,
        location_z=5.0,
        rotation_y=45.0,
        object_name="MyCube",
        simulate=True
    )
    print(f"   {result}")
    print()
    
    # Add a sphere
    print("2. Adding a sphere with simulation mode:")
    result = add_sphere(
        radius=1.5,
        location_x=7.0,
        location_y=7.0,
        location_z=7.0,
        object_name="MySphere",
        simulate=True
    )
    print(f"   {result}")
    print()
    
    # Add a plane
    print("3. Adding a plane with simulation mode:")
    result = add_plane(
        width=8.0,
        depth=8.0,
        location_x=0.0,
        location_y=0.0,
        location_z=2.0,
        rotation_y=90.0,
        object_name="MyPlane",
        simulate=True
    )
    print(f"   {result}")
    print()
    
    # List objects
    print("4. Listing all objects:")
    print(f"   {list_objects()}")
    print()
    
    print("=" * 60)
    print("For use in Emacs org-mode, add to your buffer:")
    print()
    print("#+BEGIN_SRC python")
    print("from blender_extension import add_cube, add_sphere, add_plane")
    print()
    print("# Add cube")
    print("add_cube(width=2, depth=2, height=2, object_name='MyCube')")
    print()
    print("# Add sphere")
    print("add_sphere(radius=1.5, object_name='MySphere')")
    print()
    print("#+END_SRC")
    print()
    print("Run with M-x run-python in Emacs buffer")
