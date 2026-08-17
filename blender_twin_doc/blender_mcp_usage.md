# Using Blender via Emacs + Blender-MCP + MCP-Hub

This guide explains how to connect Emacs (with GPTel + MCP-Hub) to Blender through the Model Context Protocol (MCP), and how to visualize the connections.

---

## Architecture Overview

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────────────┐
│    Emacs Editor  │ ────│  GPTel MCP   │ ────│   MCP-Hub Server     │
│    (MCP Client)  │     │  Client      │      │ (Tool Router)        │
└─────────────────┘      └──────────────┘      └─────────────────────┘
                                                           │
                                                           │ (JSON-RPC)
                                                           ▼
┌────────────────────────────────┐      ┌────────────────────────────────┐
│           Blender-MCP          │      │        Blender Addon           │
│    (MCP-to-Blender Bridge)     │      │     (3D Scene Controller)      │
└────────────────────────────────┘      └────────────────────────────────┘
```

**Data Flow**:
1. **Emacs** (your editor) → GPTel sends prompts with tool calls
2. **GPTel MCP client** → Requests tools from **MCP-Hub**
3. **MCP-Hub** → Routes to **Blender-MCP server** (or other tools)
4. **Blender-MCP** → Executes in **Blender addon** (Python socket)
5. **Blender** → Returns result → **Back through chain** → Emacs response

---

## 1. Setting Up the Connection

### Step 1: Install MCP Servers

**Emacs-side** (`~/.emacs.d/.../init.el`):

```elisp
;; Add Blender-MCP to your mcp-hub-servers config
(mcp-hub-register-server
 :name "blender"
 :type "stdio"           ;; or "stdio/stdio" for local
 :command "bash"
 :args (list "-c" "uvx blender-mcp")
 :env (alist
       `((PYTHONPATH ,blender-mcp-path)
         (UVX_EXE ,uv-path)))
)

;; For remote Jetson:
(mcp-hub-register-server
 :name "jetson-ollama"
 :type "stdio/stdio"
 :url "https://ollama.jetson/mcp"
)
```

**Terminal-side**:

```bash
# Start MCP-Hub with Blender-MCP
mcp-hub start --servers blender

# Or with multiple servers (Git, Filesystem, Blender, Ollama):
mcp-hub start --servers git,blender,fetch,filesystem
```

### Step 2: Verify Connection

**From Emacs**:

```elisp
;; List available tools
M-x gptel-load-tools
;; Or
M-x mcp-list-tools

;; Expected output should include:
;; - blender_* tools
;; - git_* tools
;; - fetch_* tools
;; - file_* tools
```

**From Terminal**:

```bash
# Check which servers are running
netstat -tlnp | grep mcp

# Or use MCP-Hub's built-in endpoint:
curl http://localhost:8001/mcp/api/tools/list

# Expected response:
# [
#   {"name": "blender_describe_scene", ...},
#   {"name": "blender_create_object", ...},
#   {"name": "git_log", ...},
#   ...
# ]
```

---

## 2. How to Use Blender Tools from Emacs

### Workflow: Ask Blender for Scene Info

```
1. In Emacs: Type your prompt
2. GPTel sends request: "What objects are in the Blender scene?"
3. MCP-Hub routes to blender_mcp
4. Blender-MCP calls Blender addon via socket
5. Blender returns: List of objects
6. Response comes back through GPTel → Emacs buffer
```

**Example Commands**:

| Prompt | MCP Tool | Effect |
|--------|----------|--------|
| "Create a cube" | `blender_create_object` | Adds a cube to scene |
| "Show scene objects" | `blender_describe_scene` | Returns current scene data |
| "Apply red material to selected" | `blender_apply_material` | Changes material |
| "Run Python code in Blender" | `blender_run_code` | Executes custom logic |

### Workflow: Use Python Code in Blender

```
1. In Emacs buffer: Write Python code for Blender
2. Prompt: "Create this scene"
3. GPTel sends code + prompt to MCP-Hub
4. MCP-Hub → Blender-MCP
5. Blender-MCP parses code, sends to Blender addon
6. Blender addon executes Python code
7. Result (created objects, materials, etc.) → back to Emacs
```

---

## 3. Visualizing the Connection

### Option 1: Using `mcp-hub status` Command

Terminal:

```bash
# Check running servers
mcp-hub status

# Expected output:
# Running servers:
#   - git
#   - blender
#   - filesystem
#   - fetch
#   - ollama
```

### Option 2: Using `curl` to Inspect

```bash
# List MCP tools available

curl http://localhost:8001/mcp/api/tools/list \
  -H "Content-Type: application/json"

# Expected JSON response:
# [
#   {"name": "blender_create_object", "description": ...},
#   {"name": "blender_describe_scene", "description": ...},
#   {"name": "blender_apply_material", "description": ...},
#   {"name": "git_log", "description": ...},
#   ...
# ]

# Check which server is responding

curl http://localhost:8001/mcp/api/health -v 2>&1 | grep -E "transfer|response"
```

### Option 3: Using `mcp-client` Python Script

Create a visual explorer:

```python
#!/usr/bin/env python3
"""mcp_tool_explorer.py – Visualize MCP connections"""

import json
import urllib.request

def list_tools(endpoint="http://localhost:8001/mcp/api/tools/list"):
    try:
        with urllib.request.urlopen(endpoint) as response:
            tools = json.loads(response.read().decode())
            for tool in tools:
                print(f"  • {tool['name']}: {tool.get('description', '')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Available MCP Tools:")
    list_tools()
```

Run:

```bash
python3 mcp_tool_explorer.py
```

### Option 4: Using `mcp_hub` with Port Monitoring

```bash
# Start with logging and monitoring
mcp-hub start \
  --servers blender,git,filesystem \
  --port 8001 \
  --log-file /tmp/mcp-hub.log \
  --monitor

# View logs:
tail -f /tmp/mcp-hub.log
```

---

## 4. Common Workflows

### Workflow 1: Generate a 3D Scene

```
1. Emacs: "Create a cyberpunk cityscape in Blender"
2. GPTel → Tool call: blender_create_object (multiple objects)
3. MCP-Hub → Blender-MCP
4. Blender-MCP → Blender addon
5. Blender:
   - Creates buildings, streets, lighting
6. Response: Scene description
7. Emacs: Shows result, offers to export
```

### Workflow 2: Refine Existing Scene

```
1. Emacs: "Add more lighting to this scene"
2. GPTel → Tool call: blender_add_light
3. Blender: Modifies light sources
4. Response: Description of changes
```

### Workflow 3: Export to Filesystem

```
1. Emacs: "Export the scene as .blend file"
2. GPTel → Tool call: blender_save_file (via Blender)
3. MCP-Hub → Blender-MCP
4. Blender: Saves file to disk
5. Path returned via filesystem tool
```

---

## 5. Debugging Tips

### Issue: "Connection refused"

```bash
# Check if MCP-Hub server is running
netstat -tlnp | grep 8001

# Test endpoint
curl -v http://localhost:8001/mcp/api/health

# Check logs
tail -f /tmp/mcp-hub.log

# Restart server
mcp-hub restart
```

### Issue: "Tool not found"

1. Verify MCP-Hub is running
2. Check `mcp-settings.json` includes the tool
3. Restart MCP-Hub to reload config

### Issue: "Blender not responding"

```bash
# Check Blender is running
ps aux | grep blender

# Check Blender MCP socket
ss -tlnp | grep 8080

# Verify socket exists
ls -la ~/blender-mcp/socket
```

### Issue: "Invalid Python code"

1. Ensure Blender has Python
2. Test with simple code:
   ```python
   print("Hello from Blender")
   ```
3. Check Blender console for errors

---

## 6. Advanced: Using MCP with Remote Blender

### Remote Setup

```bash
# Start MCP with remote Blender

mcp-hub start \
  --servers blender,git \
  --blender-url "ssh://user@remote:8080" \
  --port 8001
```

### Security: SSL/TLS

```bash
# Use HTTPS for remote
mcp-hub start \
  --servers blender \
  --ssl-cfg /path/to/server.crt
```

---

## 7. MCP Hub Commands Summary

| Command | Description |
|---------|-------------|
| `mcp-hub start` | Start MCP-Hub server |
| `mcp-hub stop` | Stop all servers |
| `mcp-hub status` | Check running servers |
| `mcp-hub restart` | Reload config |
| `mcp-hub add server` | Add new tool |
| `mcp-hub remove server` | Remove tool |
| `mcp-hub list tools` | List all tools |
| `mcp-hub log` | View logs |

---

## 8. Summary

### Connection Flow

```
Emacs ──┬── GPTel ──┬── MCP-Hub ──┬── Blender-MCP ──┬── Blender
         |           |             |             |
         |           |             |             └── Socket
         |           |             |                 |
         └── MCP Client ──┴── Tool Router ──┴── HTTP
```

### Key Files

- `~/.emacs.d/mcp-hub-servers.el` – Emacs MCP config
- `mcp-server/mcp-settings.json` – MCP tools config
- `mcp-server/blender_mcp/*` – Blender MCP code
- `~/.mcp-hub/servers.json` – MCP server list

### Quick Commands

```bash
# Start everything
mcp-hub start --servers blender,git,filesystem

# Check connection
curl http://localhost:8001/mcp/api/health

# List tools
mcp-list-tools

# From Emacs
M-x gptel-load-tools
```

---

For more details, see `README.md` and `AGENTIC_USAGE.md`.
