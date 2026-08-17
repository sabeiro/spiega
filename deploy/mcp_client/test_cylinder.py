#!/usr/bin/env python3
import asyncio, sys
sys.path.insert(0, '/home/sabeiro/lav/src/blender_twin/deploy/mcp_client')
from blender_mcp_client import BlenderMCPClient
async def test():
    client = BlenderMCPClient(url="http://172.18.0.1:19191")
    await client.call_tool("execute_blender_code", {
        "code": "c = bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(3,0,0))\n"
                 "c = bpy.context.active_object\n"
                 'result = {"status": "ok", "name": c.name}'
    })
asyncio.run(test())
