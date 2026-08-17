#!/usr/bin/env python3
"""MCP stdio-to-HTTP proxy for blender-mcp Streamable HTTP server.

mcp-hub starts this script via :command, sends JSON-RPC over stdin,
this proxies to the blender-mcp HTTP server on the host via socat bridge.
"""
import json, sys, os
import httpx

HOST = os.environ.get("BLENDER_MCP_URL", "http://172.17.0.1:19191")

session_id = None

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
    except json.JSONDecodeError:
        continue

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["mcp-session-id"] = session_id

    try:
        resp = httpx.post(HOST + "/", json=msg, headers=headers, timeout=120)
    except Exception as e:
        sys.stderr.write(f"HTTP error: {e}\n")

    # Save session-id from response headers
    sid = resp.headers.get("mcp-session-id")
    if sid:
        session_id = sid

    content_type = resp.headers.get("content-type", "")
    if "text/event-stream" in content_type:
        # SSE response: extract data lines
        for text_line in resp.text.split("\n"):
            if text_line.startswith("data: "):
                sys.stdout.write(text_line[6:] + "\n")
                sys.stdout.flush()
    else:
        sys.stdout.write(resp.text + "\n")
        sys.stdout.flush()
