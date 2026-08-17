#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Blender MCP tools for pi-coding-agent.

This module provides MCP server tools for Blender operations that can be
called directly by the pi-coding-agent without needing external Blender.
"""

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("blender-mcp")


# ------ Blender MCP Tool Implementations ------


@server.list_tools()
async def list_tools() -> Any:
    """List available tools for Blender operations."""
    return [
        {
            "name": "add_cube",
            "description": "Add a 3D cube to the Blender scene with specified width and depth in Blender units.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "width": {"type": "number", "description": "Cube width (default: 1.0)"},
                    "depth": {"type": "number", "description": "Cube depth (default: 1.0)"},
                    "height": {"type": "number", "description": "Cube height (default: 1.0)"},
                    "location_x": {"type": "number", "description": "X position (default: 0.0)"},
                    "location_y": {"type": "number", "description": "Y position (default: 0.0)"},
                    "location_z": {"type": "number", "description": "Z position (default: 0.0)"},
                    "rotation_y": {"type": "number", "description": "Y-axis rotation (default: 0.0)"},
                    "object_name": {"type": "string", "description": "Object name (default: 'Cube')"},
                },
                "required": [],
            },
        },
        {
            "name": "add_sphere",
            "description": "Add a 3D sphere to the Blender scene.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "radius": {"type": "number", "description": "Sphere radius (default: 1.0)"},
                    "location_x": {"type": "number", "description": "X position (default: 0.0)"},
                    "location_y": {"type": "number", "description": "Y position (default: 0.0)"},
                    "location_z": {"type": "number", "description": "Z position (default: 0.0)"},
                    "object_name": {"type": "string", "description": "Object name (default: 'Sphere')"},
                },
                "required": [],
            },
        },
        {
            "name": "add_plane",
            "description": "Add a 3D plane (flat surface) to the Blender scene.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "width": {"type": "number", "description": "Plane width (default: 2.0)"},
                    "depth": {"type": "number", "description": "Plane depth (default: 2.0)"},
                    "location_x": {"type": "number", "description": "X position (default: 0.0)"},
                    "location_y": {"type": "number", "description": "Y position (default: 0.0)"},
                    "location_z": {"type": "number", "description": "Z position (default: 0.0)"},
                    "rotation_y": {"type": "number", "description": "Y-axis rotation (default: 0.0)"},
                    "object_name": {"type": "string", "description": "Object name (default: 'Plane')"},
                },
                "required": [],
            },
        },
        {
            "name": "list_objects",
            "description": "List all objects currently in the Blender scene.",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "delete_object",
            "description": "Delete a Blender object from the scene by name.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "object_name": {"type": "string", "description": "Name of the object to delete"},
                },
                "required": ["object_name"],
            },
        },
        {
            "name": "list_materials",
            "description": "List all materials currently used in the scene objects.",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "add_material",
            "description": "Add a new material to the shader.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "material_name": {"type": "string", "description": "Name for the new material"},
                    "base_color": {"type": "string", "description": "Base color in hex (e.g., '#FF0000')"},
                    "metallic": {"type": "number", "description": "Metallic factor (0-1, default: 0)"},
                    "roughness": {"type": "number", "description": "Roughness factor (0-1, default: 1)"},
                    "ao_factor": {"type": "number", "description": "Ambient occlusion (0-1, default: 0.5)"},
                    "subsurface": {"type": "number", "description": "Subsurface scattering (0-1, default: 0)"},
                    "wireframe":  {"type": "boolean", "description": "Wireframe toggle (default: False)"},
                },
                "required": ["material_name", "base_color"],
            },
        },
        {
            "name": "add_uv_map",
            "description": "Add/update texture maps on existing materials.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "material_name": {"type": "string", "description": "Name of material to update"},
                    "texture_map": {"type": "string", "description": "Texture image path or filename"},
                    "uv_channel": {"type": "number", "description": "UV channel index (default: 1)"},
                },
            },
        },
        {
            "name": "render_preview",
            "description": "Render the current Blender scene as JPEG or PNG.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "format": {"type": "string", "description": "Image format: jpeg/png (default: jpeg)"},
                    "width": {"type": "number", "description": "Render width in pixels (default: 1280)"},
                    "height": {"type": "number", "description": "Render height in pixels (default: 720)"},
                },
            },
        },
        {
            "name": "reset_camera",
            "description": "Reset the camera to default view position.",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
    ]


# ------ Main entry point ------

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Any:
    """Handle tool calls for Blender operations."""
    # In real implementation, this would talk to Blender via addon or subprocess
    # For now, simulate the tool calls

    # Simulated results for demonstration
    results = {
        "add_cube": lambda args: {
            "status": "ok",
            "message": f"Created cube: '{args.get('object_name', 'Cube')}'",
            "message_details": {
                "object": "Cube",
                "location": [args.get("location_x", 0), args.get("location_y", 0), args.get("location_z", 0)],
                "rotation_y": args.get("rotation_y", 0),
            },
            "dimensions": {
                "width": args.get("width", 1.0),
                "depth": args.get("depth", 1.0),
                "height": args.get("height", 1.0),
            },
        },
        "add_sphere": lambda args: {
            "status": "ok",
            "message": f"Created sphere: '{args.get('object_name', 'Sphere')}'",
            "message_details": {
                "object": "Sphere",
                "location": [args.get("location_x", 0), args.get("location_y", 0), args.get("location_z", 0)],
                "radius": args.get("radius", 1.0),
            },
        },
        "add_plane": lambda args: {
            "status": "ok",
            "message": f"Created plane: '{args.get('object_name', 'Plane')}'",
            "message_details": {
                "object": "Plane",
                "location": [args.get("location_x", 0), args.get("location_y", 0), args.get("location_z", 0)],
                "rotation_y": args.get("rotation_y", 0),
            },
            "dimensions": {
                "width": args.get("width", 2.0),
                "depth": args.get("depth", 2.0),
            },
        },
        "list_objects": lambda args: {
            "status": "ok",
            "message": "Scene contains the following objects:",
            "objects": [
                {"type": "Cube", "location": [0, 0, 0]},
                {"type": "Cube", "location": [5, 5, 5]},
            ],
        },
        "delete_object": lambda args: {
            "status": "ok",
            "message": f"Deleted object: '{args.get('object_name', 'object')}'",
        },
        "list_materials": lambda args: {
            "status": "ok",
            "message": "Scene contains the following materials:",
            "materials": [
                {"name": "Red-Matte", "base_color": "#FF0000"},
                {"name": "Gold-Metal", "base_color": "#FFD700"},
                {"name": "Wood", "base_color": "#8B4513"},
            ],
        },
        "add_material": lambda args: {
            "status": "ok",
            "message": f"Created material: '{args.get('material_name', 'Material')}'",
            "message_details": args,
        },
        "add_uv_map": lambda args: {
            "status": "ok",
            "message": f"Added UV map to '{args.get('material_name', 'Material')}'",
            "uv_map": {
                "texture_map": args.get("texture_map"),
                "uv_channel": args.get("uv_channel", 1),
            },
        },
        "render_preview": lambda args: {
            "status": "ok",
            "message": f"Rendered image: '{args.get('format', 'jpeg')}' at {args.get('width', 1280)}x{args.get('height', 720})",
            "output": {
                "path": f"render.{args.get('format', 'jpeg')}",
                "format": args.get("format", "jpeg"),
                "width": args.get("width", 1280),
                "height": args.get("height", 720),
            },
        },
        "reset_camera": lambda args: {
            "status": "ok",
            "message": "Camera reset to default position",
        },
    }

    if name not in results:
        return {
            "status": "error",
            "message": f"Unknown tool: '{name}'",
        }

    return results[name](arguments)


async def main() -> None:
    """Run the MCP server using stdio protocol."""
    async with stdio_server() as (read, write):
        await server.run(read, write)


if __name__ == "__main__":
    asyncio.run(main())

"""
Usage Notes:
----------

This script implements a MCP server for Blender tools that can be called
by the pi-coding-agent. When the agent needs to create or modify Blender
objects, it can call tools through this client.

To use with pi-coding-agent, update mcp.json:

    {
      "mcpServers": {
        "blender-mcp": {
          "command": "python3",
          "args": [
            "-m",
            "blender_mcp_tool"
          ],
          "cwd": "/home/sabeiro/lav/src/blender_twin/deploy/ollama/pi_config/agent/tools"
        }
      }
    }

Or create a standalone script at:

    /home/sabeiro/lav/src/blender_twin/deploy/ollama/pi_config/agent/tools/blender_mcp_tool.py

"""
