#!/usr/bin/env python3
"""Test runner for blender_mcp_client tools."""

import asyncio
import json
import sys

from blender_mcp_client import BlenderMCPClient


async def run_tests():
    """Test all tools and report results."""
    client = BlenderMCPClient()
    result = await client.initialize()
    tools = await client.list_tools()
    print(f"Found {len(tools)} tools:\n")
    
    failed = []
    passed = []
    
    for tool in tools:
        name = tool["name"]
        print(f"Testing: {name}")
        try:
            res = await client.call_tool(name)
            if res.get("isError"):
                print(f"  FAILED: {res.get('error', {}).get('message', 'unknown')}")
                failed.append(name)
            else:
                print(f"  OK")
                passed.append(name)
        except Exception as e:
            print(f"  ERROR: {e}")
            failed.append(name)
        print()
    
    print(f"\nSummary:")
    print(f"  Passed: {len(passed)}")
    print(f"  Failed: {len(failed)}")
    if failed:
        print(f"  Failed tools: {', '.join(failed)}")
    
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(run_tests()))
