#!/usr/bin/env python3
import asyncio, sys
sys.path.insert(0, '/home/sabeiro/lav/src/blender_twin/deploy/mcp_client')
from blender_mcp_client import BlenderMCPClient
async def test():
    client = BlenderMCPClient(url="http://172.18.0.1:19191")
    await client.call_tool("execute_blender_code", {
        "code": "s = bpy.ops.mesh.primitive_uv_sphere_add(sections=32, rings=32, location=(2,0,0))\n"
                 "s = bpy.context.active_object\n"
                 'result = {"status": "ok", "name": s.name}'
    })
asyncio.run(test())
