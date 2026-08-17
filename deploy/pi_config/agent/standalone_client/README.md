# Blender MCP Client

## Overview

This client integrates with a **running Blender instance** (PID: 9811) via the MCP protocol. It allows LLMs (like Ollama's pi) to add and manipulate 3D objects in Blender.

## Running Blender Instance

```bash
ps aux | grep blender | grep -v grep
```

Expected output:
```
sabeiro     9811  0.0  974328 ?      Sl   Jun10 78:57 /snap/blender/7480/blender
```

## How It Works

1. **Connect to running Blender** via subprocess
2. **Execute Python ops** to add objects:
   - `bpy.ops.mesh.primitive_cube_add()`
   - `bpy.ops.mesh.primitive_uvball_add()`
   - `bpy.ops.mesh.primitive_grid_add()`
3. **MCP protocol** allows LLM to request operations

## Usage

### Add a Cube
```json
{
  "message": "Add a cube to Blender"
}
```

### Add a Sphere
```json
{
  "message": "Add a sphere to Blender" 
}
```

### View Scene Objects
The client can also:
- List current scene objects
- Get object locations
- Export scene data

## Configuration

### MCP Server Config (`mcp.json`)
```json
{
  "mcpServers": {
    "blender-mcp": {
      "command": "python3",
      "args": ["-m", "blender_mcp_client"],
      "cwd": "/home/sabeiro/lav/src/blender_twin/deploy/ollama/pi_config/agent/standalone_client"
    }
  }
}
```

## Limitations

- Requires running Blender instance
- Works via background subprocess
- Some Blender add-ons may not be available

## License

MIT License
