#!/usr/bin/env python3
import asyncio
import sys

"""Create a cube in the Blender scene."""

from blender_mcp_client import BlenderMCPClient

MCP_URL = "http://172.18.0.1:19191"

async def add_cube(client: BlenderMCPClient):
    await client.call_tool("execute_blender_code", {
        "code": (
            "import bpy\n"
            "bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))\n"
            "cube = bpy.context.active_object\n"
            'result = {"status": "ok", "name": cube.name}'
        )
    })


async def verify(client: BlenderMCPClient) -> list:
    result = await client.call_tool("execute_blender_code", {
        "code": (
            "import bpy\n"
            "cubes = [o.name for o in bpy.data.objects "
            "if o.type == 'MESH' and 'Cube' in o.name]\n"
            'result = {"cube": cubes}'
        )
    })
    for item in result.get("content", []):
        if item.get("type") == "text":
            import json
            return json.loads(item["text"]).get("cubes", [])
    return []


async def main():
    client = BlenderMCPClient(url=MCP_URL)
    await add_cube(client)
    cubes = await verify(client)
    print(f"OK — cubes in scene: {cubes}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"FAILED: {e}", file=sys.stderr)
        sys.exit(1)




# ============= SCRIPT WRAPPER FOR CUSTOM BlenderMCPClient =============

# Script that takes a Blender operation (as string or dict) and executes it
# with proper JSON error handling.
async def script_wrapper(operation: str | dict) -> dict:
    """
    Execute a Blender script and return proper JSON result.
    
    Args:
        operation: Either a string Blender script or a dict with 'code' key
        
    Returns:
        dict with 'status': 'ok' | 'error', and 'result' or 'message'
    """
    code = operation if isinstance(operation, str) else operation.get("code")
    
    result = await client.call_tool("execute_blender_code", {"code": code})
    
    content = [item["text"] for item in result["content"] if item["type"] == "text"]
    
    if content and "error" in content[0]:
        import json
        try:
            return json.loads(content[0])
        except json.JSONDecodeError:
            return {"status": "error", "message": content[0]}
    
    if content:
        return {"status": "ok", "result": content[0]}
    return {"status": "ok", "result": "No result returned"}


async def test_operation(blender_code: str) -> dict:
    """Test a Blender operation and return result."""
    return await script_wrapper(blender_code)
