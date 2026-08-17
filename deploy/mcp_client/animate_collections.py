#!/usr/bin/env python3
import asyncio
import sys

from blender_mcp_client import BlenderMCPClient

MCP_URL = "http://172.18.0.1:19191"


async def setup_animated_collections(client: BlenderMCPClient):
    await client.call_tool("execute_blender_code", {
        "code": (
            "import bpy\n"
            "import math\n"
            "\n"
            "# Disable automatic keyframe generation for smoother animation\n"
            "bpy.context.scene.use_nodes = True\n"
            "node_tree = bpy.context.scene.view_layers['View1'].node_tree\n"
            "nodes = node_tree.nodes\n"
            "links = node_tree.links\n"
            "\n"
            "# Create a new Geometry Nodes modifier for each collection\n"
            "collections = ['even', 'odd', 'text', 'task']\n"
            "\n"
            "for col_name in collections:\n"
            "    col = bpy.data.collections.get(col_name)\n"
            "    if col:\n"
            "        # Add Geometry Nodes modifier\n"
            "        mod = col.modifiers.new(name=\"AnimateVertical\",\n"
            "                                  type='GEOMETRY_NODES')\n"
            "        # Create new node tree\n"
            "        node_tree = bpy.data.node_groups.get(\"AnimatedCollection\") or \\\n"
            "        bpy.ops.node.new('GEOMETRY_NODES', name=\"AnimatedCollection\")\n"
            "        bpy.context.scene.view_layers['View1'].node_tree.nodes.new(\n"
            "            type='NewMesh').links.new(nodes['NewMesh'].outputs['Geometry'],\n"
            "            to_node=nodes['Geometry Nodes'], to_socket='Geometry')\n"
            "\n"
            "# Create animated script\n"
            "script = '''\n"
            "import bpy\n"
            "import math\n"
            "\n"
            "def animate_collection(collection_name):\n"
            "    col = bpy.data.collections.get(collection_name)\n"
            "    if not col:\n"
            "        return\n"
            "\n"
            "    frame = bpy.context.scene.frame_current\n"
            "    # Create cyclic wave animation (0-2pi)\n"
            "    offset = cycle_offset = cycle_amount = cycle_speed = cycle_type\n"
            "\n"
            "    for obj in col.objects:\n"
            "        if obj.type == 'MESH':\n"
            "            # Calculate vertical offset based on sine wave\n"
            "            offset = math.sin(frame * 0.1) * 0.5\n"
            "            obj.location.z += offset\n"
            "\n"
            "animate_collection('even')\n"
            "animate_collection('odd')\n"
            "animate_collection('text')\n"
            "animate_collection('task')\n"
            "''' \n"
            "\n"
            "with open('/tmp/animation_script.py', 'w') as f:\n"
            f.write(script)\n"
            "open('/tmp/animation_script.py').read()\n"
        )
    })


async def check_current_frame(client: BlenderMCPClient) -> int:
    result = await client.call_tool("execute_blender_code", {
        "code": "import bpy\n"
            "result = {'frame': bpy.context.scene.frame_current}\n"
            'return result'
    })
    for item in result.get("content", []):
        if item.get("type") == "text":
            import ast
            return ast.literal_eval(item["text"])
    return 1


async def main():
    client = BlenderMCPClient(url=MCP_URL)
    current_frame = await check_current_frame(client)
    print(f"Current frame: {current_frame}")
    await setup_animated_collections(client)
    print("Setup complete - collections will now animate")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"FAILED: {e}", file=sys.stderr)
        sys.exit(1)
