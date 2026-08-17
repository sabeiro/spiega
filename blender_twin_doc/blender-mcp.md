# BlenderMCP - Blender Model Context Protocol Integration

## Overview

BlenderMCP connects Blender to AI assistants (like Claude) through the Model Context Protocol (MCP), enabling prompt-assisted 3D modeling, scene creation, and manipulation.

## Architecture

### Components

1. **Blender Addon (`addon.py`)**: Creates a socket server within Blender to receive and execute commands
2. **MCP Server (`src/blender_mcp/server.py`)**: Python server implementing MCP protocol connecting to Blender addon

### Communication Protocol

- JSON-based protocol over TCP sockets
- Commands: JSON objects with `type` and optional `params`
- Responses: JSON objects with `status` and `result` or `message`

## Features

- **Two-way communication**: Connect AI to Blender through socket-based server
- **Object manipulation**: Create, modify, and delete 3D objects
- **Material control**: Apply and modify materials and colors
- **Scene inspection**: Get detailed information about current Blender scene
- **Code execution**: Run arbitrary Python code in Blender from AI
- **Asset integration**: Poly Haven assets, Hyper3D Rodin model generation
- **Remote execution**: Run Blender MCP on remote hosts

## Installation

### Prerequisites

- Blender 3.0 or newer
- Python 3.10 or newer
- uv package manager

### Environment Variables

