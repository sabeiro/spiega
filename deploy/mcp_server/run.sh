#!/bin/sh
# Single container, two processes (hence two ports):
# - 8000: MCP protocol server (server.py) for Emacs/gptel MCP client.
# - 8001: FastAPI agent (control UI, /api/chat with tools, health, vision). uvicorn --reload for live edits.
# Nginx exposes both under one path prefix: /mcp and /mcp/*
set -e
python3 -u server.py &
exec python3 -u -m uvicorn agent:app --host 0.0.0.0 --port 8001 --reload --reload-dir /app
