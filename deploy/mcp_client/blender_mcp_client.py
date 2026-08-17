#!/usr/bin/env python3
"""
MCP client for blender-mcp using the standard MCP protocol (streamable-http).

Usage:
  blender_mcp_client.py tools
  blender_mcp_client.py call execute_blender_code '{"code":"import bpy; print(bpy.data.objects.values())"}'
  blender_mcp_client.py --http http://localhost:9191 tools
"""

import argparse
import asyncio
import json
import re
import sys

import httpx


def _parse_sse(text: str) -> list[dict]:
    """Parse SSE text into a list of {event, data, id} dicts."""
    events = []
    # Normalize CRLF to LF
    text = text.replace("\r\n", "\n")
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        ev = {"event": "message", "data": "", "id": None}
        for line in block.split("\n"):
            if line.startswith("event: "):
                ev["event"] = line[7:]
            elif line.startswith("data: "):
                ev["data"] = line[6:]
            elif line.startswith("id: "):
                ev["id"] = line[4:]
        events.append(ev)
    return events


class BlenderMCPClient:
    """Minimal MCP client for blender-mcp over streamable-http."""

    def __init__(self, url: str = "http://localhost:9191"):
        self.url = url.rstrip("/")
        self._session_id: str | None = None
        self._protocol_version: str | None = None
        self._initialized = False

    async def _post(self, body: dict) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self._session_id:
            headers["mcp-session-id"] = self._session_id
        if self._protocol_version:
            headers["mcp-protocol-version"] = self._protocol_version

        request_id = body.get("id")

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(self.url, json=body, headers=headers)
            if sid := resp.headers.get("mcp-session-id"):
                self._session_id = sid
            resp.raise_for_status()
            text = resp.text

        # Parse SSE events from the response body
        for ev in _parse_sse(text):
            if ev["event"] != "message" or not ev["data"]:
                continue
            msg = json.loads(ev["data"])
            if request_id is not None and msg.get("id") != request_id:
                continue
            if "error" in msg:
                raise RuntimeError(f"JSON-RPC error: {msg['error']}")
            return msg.get("result", {})

        return {}

    async def initialize(self):
        result = await self._post({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "blender-mcp-client", "version": "0.1.0"},
            },
        })
        self._protocol_version = result.get("protocolVersion")
        await self._post({
            "jsonrpc": "2.0", "method": "notifications/initialized",
        })
        self._initialized = True
        return result

    async def list_tools(self) -> list:
        if not self._initialized:
            await self.initialize()
        result = await self._post({
            "jsonrpc": "2.0", "id": 2, "method": "tools/list",
        })
        return result.get("tools", [])

    async def call_tool(self, name: str, arguments: dict | None = None):
        if not self._initialized:
            await self.initialize()
        body = {
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": name},
        }
        if arguments:
            body["params"]["arguments"] = arguments
        return await self._post(body)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

async def cmd_tools(client: BlenderMCPClient):
    tools = await client.list_tools()
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


async def cmd_call(client: BlenderMCPClient, name: str, args_json: str):
    args = json.loads(args_json) if args_json else None
    result = await client.call_tool(name, args)
    for item in result.get("content", []):
        t = item.get("type", "")
        if t == "text":
            print(item.get("text", ""))
        elif t == "image":
            print(f"[image: {item.get('mimeType', '?')} - {len(item.get('data', ''))}B]")
        else:
            print(f"[{t}]")
    if result.get("isError"):
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="blender-mcp client")
    p.add_argument("--http", default="http://localhost:9191")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("tools", help="list tools")
    cp = sub.add_parser("call", help="call a tool")
    cp.add_argument("name")
    cp.add_argument("args", nargs="?", default="{}")

    args = p.parse_args()
    client = BlenderMCPClient(url=args.http)
    if args.command == "tools":
        asyncio.run(cmd_tools(client))
    elif args.command == "call":
        asyncio.run(cmd_call(client, args.name, args.args))


if __name__ == "__main__":
    main()
