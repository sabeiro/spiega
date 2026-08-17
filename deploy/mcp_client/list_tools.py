#!/usr/bin/env python3
"""
List all tools from a running blender-mcp HTTP server.

Usage:
  # Run on host (where blender-mcp is listening on :9191)
  ./list_tools.py

  # Or when running inside a source checkout:
  uv run python list_tools.py

  # Specify a different endpoint:
  ./list_tools.py --http http://192.168.1.100:9191
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from blender_mcp_client import BlenderMCPClient, asyncio


async def main():
    url = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--http" else "http://localhost:9191"
    client = BlenderMCPClient(url=url)
    tools = await client.list_tools()

    print(f"Connected to {url}")
    print(f"Total tools: {len(tools)}\n")
    for t in tools:
        print(f"  {t['name']}")
        desc = (t.get("description") or "").strip().split("\n")[0]
        if desc:
            print(f"    {desc}")
        props = t.get("inputSchema", {}).get("properties", {})
        req = set(t.get("inputSchema", {}).get("required", []))
        if props:
            print("    Params:")
            for name, info in props.items():
                opt = "" if name in req else " (opt)"
                print(f"      {name}: {info.get('type', 'any')}{opt}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
