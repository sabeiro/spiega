# Emacs → Blender via MCP-Hub: Topology Diagram

<!-- The SVG diagram can be embedded directly in markdown using: -->
<!-- ![Blender-MCP Topology](./BLENDER_MCP_TOPLOGY.svg) -->

## Diagram Description

The diagram shows how to connect **Emacs** to **Blender** through **MCP-Hub** and **Blender-MCP**.

## Data Flow:

```
┌─────────────┐     ┌─────────┐     ┌─────────┐     ┌───────────┐
│    Emacs     │ →   │ GPTel   │ →   │ MCP-Hub │ →   │Blender    │
│   Editor     │     │ Client  │     │ Server  │     │   Engine  │
│              │     │         │     │         │     │           │
└─────────────┘     └─────────┘     └─────────┘     └───────────┘
```

## Connection Steps:

1. **Emacs** → **GPTel**: User prompts in Emacs buffer
2. **GPTel** → **MCP-Hub**: JSON-RPC protocol (tools calls)
3. **MCP-Hub** → **Blender-MCP**: Routes to appropriate server
4. **Blender-MCP** → **Blender**: TCP socket to Python addon

## Quick Commands:

```bash
# Start Blender-MCP
uvx blender-mcp &

# Start MCP-Hub with Blender
mcp-hub start --servers blender

# Test connection
curl http://localhost:8001/mcp/api/health
```

## See also:

- [BLENDER_MCP_USAGE.md](./BLENDER_MCP_USAGE.md) - Complete usage guide
- [AGENTIC_USAGE.md](./AGENTIC_USAGE.md) - Agentic usage patterns
