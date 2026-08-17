# Blender MCP Server - HTTP Client

A simple HTTP-based client for interacting with Blender operations.

## Setup

The server runs in the background on `localhost:9876`. If needed, check if it's running:

```bash
# Check if port 9876 is open
ss -tlnp | grep 9876

# If not running, start the server
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/blender_http_server.py &

# Or use the existing Blender process if available
```

## Usage

### One-shot commands

```bash
# Test the server
curl http://localhost:9876/command/info

# Add a cube
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/simple_client.py cube

# Add a sphere
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/simple_client.py sphere

# Add multiple objects
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/simple_client.py cube
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/simple_client.py sphere

# List all objects
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/simple_client.py list

# Clear the scene
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/simple_client.py clear

# Setup basic scene
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/simple_client.py setup

# Export scene (OBJ format)
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/simple_client.py export
```

### Interactive mode

```bash
python3 /home/sabeiro/lav/src/blender_twin/mcp_server/mcp-server/simple_client.py
> cube
> sphere
> list
> clear
> export
> /quit
```

## Available Operations

### 1. Info
Get server information about available endpoints.

```bash
python3 simple_client.py info
```

### 2. Add Cube
Create a new cube in the Blender scene.

```bash
python3 simple_client.py cube
```

### 3. Add Sphere
Create a new sphere with radius=1.0.

```bash
python3 simple_client.py sphere
```

### 4. Add Cylinder
Create a new cylinder.

```bash
python3 simple_client.py cylinder
```

### 5. List Objects
List all objects currently in the scene.

```bash
python3 simple_client.py list
```

### 6. Clear Scene
Remove all objects from the scene.

```bash
python3 simple_client.py clear
```

### 7. Setup Basic Scene
Create a basic scene with a cube and sphere.

```bash
python3 simple_client.py setup
```

### 8. Export Scene
Export the current scene to OBJ format.

```bash
python3 simple_client.py export
```

## Server Endpoints

The HTTP server runs at `http://localhost:9876/command` with these endpoints:

- `GET /command/info` - Server info
- `GET /command/cube` - Add a cube
- `GET /command/sphere` - Add a sphere
- `GET /command/cylinder` - Add a cylinder
- `GET /command/material` - Apply material
- `GET /command/move` - Move object
- `GET /command/scale` - Scale object
- `GET /command/rotate` - Rotate object
- `GET /command/list` - List objects
- `GET /command/clear` - Clear scene
- `GET /command/setup` - Setup basic scene
- `GET /command/export` - Export scene

## Example Usage with curl

```bash
# Get server info
curl http://localhost:9876/command/info | python3 -m json.tool

# Add a cube
curl -s http://localhost:9876/command/cube | python3 -m json.tool

# List objects after adding a cube
curl -s http://localhost:9876/command/list | python3 -m json.tool
```

## Requirements

- Python 3.10+
- Blender (system-wide installation)
- `curl` for command-line testing

## Troubleshooting

### Port already in use

If port 9876 is already in use, check what process is using it:

```bash
fuser 9876/tcp
ss -tlnp | grep 9876
# Or check the existing Blender MCP server
```

### No response from server

If the server doesn't respond:

1. Check if Blender is installed: `which blender`
2. Check if port 9876 is bound: `fuser 9876/tcp`
3. Try connecting directly: `curl http://localhost:9876/`
4. Check server logs: Look for error messages in Blender console

### Connection timeout

If you get connection errors:

1. Ensure no firewall is blocking port 9876
2. Check if the existing server is still running
3. Test with a simple curl: `curl -v http://localhost:9876/command/info`

## Contact

For issues or questions, please check the server error logs or contact the system admin.

