#!/usr/bin/env python3
import asyncio
import sys

from blender_mcp_client import BlenderMCPClient

MCP_URL = "http://172.18.0.1:19191"


async def add_sphere(client: BlenderMCPClient):
    await client.call_tool("execute_blender_code", {
        "code": (
            "import bpy\n"
            "bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=2)\n"
            "sphere = bpy.context.active_object\n"
            'result = {"status": "ok", "name": sphere.name}'
        )
    })


async def verify(client: BlenderMCPClient) -> list:
    result = await client.call_tool("execute_blender_code", {
        "code": (
            "import bpy\n"
            "spheres = [o.name for o in bpy.data.objects "
            "if o.type == 'MESH' and 'UV Sphere' in o.name]\n"
            'result = {"spheres": spheres}'
        )
    })
    for item in result.get("content", []):
        if item.get("type") == "text":
            import json
            return json.loads(item["text"]).get("spheres", [])
    return []


async def main():
    client = BlenderMCPClient(url=MCP_URL)
    await add_sphere(client)
    spheres = await verify(client)
    print(f"OK — spheres in scene: {spheres}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"FAILED: {e}", file=sys.stderr)
        sys.exit(1)
