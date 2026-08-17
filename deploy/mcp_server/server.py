#!/usr/bin/env python3
"""
MCP server on the Jetson: exposes tools that talk to Ollama and run on the Jetson.
Emacs (gptel + MCP) can connect to this server and use these tools when chatting with Ollama.
"""
from __future__ import annotations
import base64, json, os
import cv2
import httpx
import numpy as np
from datetime import datetime, timezone
from typing import Any
import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")
# Camera: index 0 = /dev/video0 (RPi camera on Jetson cam0). Vision model for describing the scene.
CAMERA_INDEX = int(os.environ.get("CAMERA_INDEX", "0"))
OLLAMA_VISION_MODEL = os.environ.get("OLLAMA_VISION_MODEL", "llava")
MCP_NAME = "jetson-ollama"
mcp = FastMCP(MCP_NAME,
              transport_security=TransportSecuritySettings(
                  enable_dns_rebinding_protection=False,
                  # Add your specific gateway or domain here
                  # enable_dns_rebinding_protection=True,
                  # allowed_hosts=["localhost:*", "127.0.0.1:*", "your-gateway-host:*"],
                  # allowed_origins=["http://localhost:*", "http://your-gateway-host:*"],
              ))

@mcp.tool()
def mcp_tools_to_ollama(mcp_tools) -> list[dict]:
    """Convert MCP tool schemas to Ollama/OpenAI format."""
    ollama_tools = []
    for tool in mcp_tools:
        ollama_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema,
            },
        })
    return json.dumps({"ollama_tools":ollama_tools})

# @mcp.tool()
# def hello(ctx: Context = None):
#     """Say hello"""
#     if ctx:
#         ctx.info("in Hello!")
#     return {"Response": "Hello!"} 

# @mcp.resource("config://version")
# def get_version(ctx: Context):
#     ctx.info("Sono in get_version!")
#     return "2.0.1"


@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool()
def ciaet():
    """Say ciaet"""
    return {"Response": "EnKület!"}  

@mcp.tool()
def hello():
    """Say ciaet"""
    return {"Response": "EnKület!"}  

@mcp.tool()
def ollama_list_models() -> str:
    """List available Ollama model names on the Jetson. Returns a JSON list of model names and details."""
    try:
        r = httpx.get(f"{OLLAMA_HOST}/api/tags", timeout=10.0)
        r.raise_for_status()
        data = r.json()
        models = data.get("models", [])
        names = [m.get("name", m.get("model", "?")) for m in models]
        return json.dumps({"models": names, "count": len(names)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def ollama_show_model(name: str) -> str:
    """Show details for an Ollama model by name (e.g. qwen2.5-coder:3b)."""
    try:
        r = httpx.post(
            f"{OLLAMA_HOST}/api/show",
            json={"name": name},
            timeout=30.0,
        )
        r.raise_for_status()
        return json.dumps(r.json(), indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def ollama_chat(model: str, message: str, stream: bool = False) -> str:
    """Send a single user message to an Ollama model and return the assistant reply.
    model: e.g. qwen2.5-coder:3b
    message: the user message
    stream: if false, returns the full reply; if true, returns until first chunk (for testing).
    """
    try:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "stream": stream,
            "options": {"num_gpu": int(os.environ.get("OLLAMA_NUM_GPU", "20"))},
        }
        r = httpx.post(
            f"{OLLAMA_HOST}/api/chat",
            json=payload,
            timeout=120.0,
        )
        r.raise_for_status()
        data = r.json()
        reply = (data.get("message") or {}).get("content", "")
        return reply.strip() or json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Current date / time
# ---------------------------------------------------------------------------


@mcp.tool()
def current_date(include_time: bool = True, iso_only: bool = True) -> str:
    """Return the current date (and optionally time) on the server.
    include_time: if True, include time; if False, date only.
    iso_only: if True, return ISO 8601 format (e.g. 2026-02-16T14:30:00+00:00); if False, return a readable string.
    """
    now = datetime.now(timezone.utc)
    if iso_only:
        s = now.isoformat() if include_time else now.date().isoformat()
    else:
        s = now.strftime("%Y-%m-%d %H:%M:%S %Z") if include_time else now.strftime("%A, %B %d, %Y")
    return s


# ---------------------------------------------------------------------------
# NumPy math (whitelisted operations, no eval)
# ---------------------------------------------------------------------------

_NUMPY_AGG = {"sum", "mean", "std", "min", "max", "prod", "median"}
_NUMPY_BINARY = {"add", "subtract", "multiply", "divide", "power", "remainder"}
_NUMPY_UNARY = {"sqrt", "sin", "cos", "tan", "log", "log10", "exp", "abs", "floor", "ceil"}


@mcp.tool()
async def echo(message: str) -> str:
    """Echo back the message."""
    return message

@mcp.prompt()
async def greeting_prompt(name: str) -> str:
    """A simple greeting prompt."""
    return f"Greet {name} kindly."

@mcp.resource("file://./tool.txt")
def publish_file() -> str:
    """The greeting text file."""
    with open("greeting.txt", "r", encoding="utf-8") as file:
        return file.read()

@mcp.tool()
def numpy_array_op(operation: str, values: list[float]) -> str:
    """Apply a NumPy aggregation to a list of numbers.
    operation: one of sum, mean, std, min, max, prod, median.
    values: list of numbers (e.g. [1.0, 2.0, 3.0]).
    Returns the result as a string (number or JSON with error).
    """
    if operation not in _NUMPY_AGG:
        return json.dumps({"error": f"Unknown operation. Use one of: {sorted(_NUMPY_AGG)}"})
    try:
        arr = np.array(values, dtype=float)
        if arr.size == 0:
            return json.dumps({"error": "Empty list"})
        fn = getattr(np, operation)
        out = float(fn(arr))
        return str(out) if operation != "std" else str(round(out, 10))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def numpy_binary_op(operation: str, a: float, b: float) -> str:
    """Apply a binary math operation to two numbers using NumPy.
    operation: one of add, subtract, multiply, divide, power, remainder.
    a, b: two numbers.
    """
    if operation not in _NUMPY_BINARY:
        return json.dumps({"error": f"Unknown operation. Use one of: {sorted(_NUMPY_BINARY)}"})
    try:
        fn = getattr(np, operation)
        out = float(fn(a, b))
        return str(out)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def numpy_unary_op(operation: str, x: float) -> str:
    """Apply a unary math function to one number using NumPy (radians for trig).
    operation: one of sqrt, sin, cos, tan, log, log10, exp, abs, floor, ceil.
    x: input number (angles in radians for sin/cos/tan).
    """
    if operation not in _NUMPY_UNARY:
        return json.dumps({"error": f"Unknown operation. Use one of: {sorted(_NUMPY_UNARY)}"})
    try:
        fn = getattr(np, operation)
        out = float(fn(x))
        return str(out)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Camera: capture and describe scene with YOLO (lightweight, no Ollama vision needed)
# ---------------------------------------------------------------------------

from vision import describe_scene_yolo

@mcp.tool()
def camera_describe_scene(prompt: str = "List the main objects you see in this image. Be concise.") -> str:
    """Take a picture from the camera and return a text description of the objects in the scene (YOLO).
    Use this when the user asks what you see, what is in the room, describe the scene, etc.
    prompt: ignored; kept for API compatibility.
    """
    try:
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened():
            return json.dumps({"error": f"Could not open camera index {CAMERA_INDEX} (e.g. /dev/video0). Check device."})
        ok, frame = cap.read()
        cap.release()
        if not ok or frame is None:
            return json.dumps({"error": "Could not read a frame from the camera."})
        return describe_scene_yolo(frame)
    except Exception as e:
        return json.dumps({"error": f"Camera capture failed: {e}"})


def main() -> None:
    # Bind to 0.0.0.0 so nginx (other container) can reach this server.
    host = os.environ.get("MCP_HTTP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_HTTP_PORT", "8000"))
    mcp.settings.host = host
    mcp.settings.port = port
    mcp.run(transport="streamable-http")
    
if __name__ == "__main__":
    main()
