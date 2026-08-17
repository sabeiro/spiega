# Blender MCP Tools for Ollama/LLM Agents

## Setup

This setup allows LLM agents (via Ollama) to interact with Blender operations directly without requiring external Blender installation.

## Configuration

The MCP server is configured in `mcp.json`:

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

## Available Tools

The MCP server provides the following tools:

- `add_cube` - Add a 3D cube to the scene
- `add_sphere` - Add a 3D sphere object
- `add_plane` - Add a 3D plane surface
- `add_material` - Create new materials
- `add_uv_map` - Add texture maps
- `render_preview` - Render the scene
- `list_objects` - List scene objects
- `list_materials` - List available materials
- `create_camera` - Create a camera
- `create_lights` - Create point lights
- `create_sunlight` - Create area lights (sunlight)
- `reset_camera` - Reset camera to default
- `delete_object` - Delete Blender objects

## Usage

The client can be run standalone:

```bash
cd /home/sabeiro/lav/src/blender_twin/deploy/ollama/pi_config/agent/standalone_client
python3 blender_mcp_client.py
```

Or via the MCP server with Ollama using the `mcp.json` configuration.

## Project Integration

This local MCP client integration:
- Enables the agent to understand Blender operations without requiring external tools
- Provides tools for common Blender operations (add/delete cubes, materials, cameras)
- Works with Ollama local LLMs
- No external Blender installation needed for basic operations

## See Also

- `blender_mcp_client.py` - Main MCP server implementation
- `mcp.json` - MCP server configuration for Ollama
- `/home/sabeiro/lav/src/blender_twin/deploy/mcp-client/` - Alternative MCP client setup
