# Blender CV Agent Extension

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A Blender Vision Computer Vision Agent using MCP with local LLM integration.

## 🏗️ Architecture

### Component Roles

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  blender-mcp    │ ----> │  mcp-server     │ ----> │  mcp-client     │
│  (Blender Host) │ tool  │  (LLM + Tools)  │       │  (Test Tool)    │
└─────────────────┘       └─────────────────┘       └─────────────────┘
        ^                                ^
        |                                |
        └────────────────────────────────┘
              Network (stdio/socket)
```

### Key Points

1. **blender-mcp (Host)**
   - Purpose: MCP extension for Blender 3D operations
   - Runs in the Blender application
   - Provides 3D manipulation tools

2. **mcp-server**
   - Purpose: MCP server exposing available LLMs and tools from the network
   - Does NOT necessarily interact with Blender
   - Acts as a bridge between clients and available tools

3. **mcp-client**
   - Purpose: Test tool ONLY for direct connections
   - Used to manually test tools without LLM
   - Not for production agent use

4. **blender_cv_agent**
   - Purpose: Uses blender-mcp via mcp-server
   - Runs locally to interact with Blender

## 📖 Component Details

### 1. blender-mcp (Host Extension)
**Path:** `/home/sabeiro/lav/src/blender_cv/mcp_server/ollama/pi_config/agent/extensions/blender-mcp`

**Purpose:** MCP extension that provides Blender 3D operations to LLMs

**Capabilities:**
- Create 3D objects (cube, sphere, cylinder, etc.)
- Modify object properties (position, scale, rotation)
- Apply materials and textures
- Export scenes to various formats
- Execute Python code in Blender
- Manage scene and camera operations

**How to Use:**
```bash
# Install Blender MCP addon
blender --enable-mcp-addon

# Or enable in Blender:
File > Add-ons > Install > blender-mcp.zip
```

### 2. mcp-server
**Path:** `/home/sabeiro/lav/src/blender_cv/mcp_server/mcp-server.py`

**Purpose:** Connects to available LLMs and tools in the network, exposes them as MCP tools

**Capabilities:**
- Expose LLM capabilities as tools
- Expose available services as tools
- Bridge between MCP clients and backend tools
- Standardize tool calling via MCP protocol

**Note:** This server does NOT necessarily work with Blender. It's a generic MCP server that exposes whatever tools are available.

### 3. mcp-client (Test Tool)
**Path:** `/home/sabeiro/lav/src/blender_cv/mcp_server/mcp-client/`

**Purpose:** Standalone test client to interact directly with blender-mcp

**Usage:**
```bash
# List available tools
python mcp-client.py --members

# Interactive chat
python mcp-client.py --chat
```

**Note:** This is ONLY for testing. Don't use in production agent.

### 4. blender_cv_agent
**Path:** `/home/sabeiro/lav/src/blender_cv/mcp_server/`

**Purpose:** Main agent that uses blender-mcp via mcp-server

**Capabilities:**
- Uses blender-mcp tools through network
- Processes natural language prompts
- Executes Blender operations via MCP
- Integrates with LLM for intelligent operation

## 🔗 Connection Flow

```
┌─────────────────────┐
│   User/LLM Prompt   │
└─────────────────────┘
            │
            ▼
┌──────────────────────┐
│   blender_cv_agent   │  (Agent)
│   uses mcp-server    │
└──────────────────────┘
            │
            ▼ (via mcp-server)
┌──────────────────────┐       ┌──────────────────────┐
│   mcp-server         │ <───> │   Available LLMs     │
│   (Tool Hub)         │ tool  │   and Services       │
└──────────────────────┘       └──────────────────────┘
            │
            ▼ (via mcp-server)
┌──────────────────────┐
│   mcp-client (Test)  │
│   Direct connection  │
└──────────────────────┘

┌──────────────────────┐
│   blender-mcp        │  ← Actually runs inside Blender
│   (3D Operations)    │
└──────────────────────┘
```

## 📋 Available Tools (blender-mcp)

### Object Operations
| Tool | Description |
|------|-------------|
| `create_object` | Create 3D primitive |
| `modify_object` | Modify existing object |
| `delete_object` | Remove object from scene |

### Material Operations
| Tool | Description |
|------|-------------|
| `apply_material` | Apply material to object |
| `get_materials` | List available materials |

### Scene Operations
| Tool | Description |
|------|-------------|
| `get_scene_info` | Get scene metadata |
| `get_objects` | List all objects |
| `export_scene` | Export scene to file |
| `set_camera_view` | Change camera view |

### Code Execution
| Tool | Description |
|------|-------------|
| `run_code` | Execute Python code in Blender |

## 💡 Example Commands

### Create a Cube
```python
{
    "type": "create_object",
    "params": {
        "obj_type": "cube",
        "name": "my_cube",
        "position": {"coordinates": [0, 0, 0]},
        "size": {"coordinates": [1, 1, 1]}
    }
}
```

### Get Scene Info
```python
{
    "type": "get_scene_info"
}
```

### Export Scene
```python
{
    "type": "export_scene",
    "params": {
        "format": "glb",
        "path": "/path/to/export.glb"
    }
}
```

## 🧪 Testing

### Test mcp-client (Direct to blender-mcp)
```bash
cd /home/sabeiro/lav/src/blender_cv/mcp_server/mcp-client
python mcp-client.py --members
python mcp-client.py --chat
```

### Test with LLM via mcp-server
```bash
cd /home/sabeiro/lav/src/blender_cv/mcp_server
python agent.py
```

## ⚙️ Configuration

### Environment Variables
```bash
# Port for mcp-server
export MCP_PORT=9876

# Debug logging
export LOG_LEVEL=DEBUG

# Verbose output
export VERB=verbose
```

### Default Config
```python
{
    'host': '127.0.0.1',
    'port': 9876,
    'timeout': 5.0,
    'max_objects': 50
}
```

## 📝 Error Responses

### Error Format
```json
{
    "status": "error",
    "message": "Error description"
}
```

### Success Format
```json
{
    "status": "ok",
    "result": {...}
}
```

## 🚧 Setup

1. **Install Blender with MCP addon:**
   ```bash
   blender --enable-mcp-addon
   ```

2. **Start mcp-server:**
   ```bash
   python mcp-server.py
   ```

3. **Run agent:**
   ```bash
   python agent.py
   ```

## 📊 Summary

| Component | Purpose | Runs in |
|-----------|---------|---------|
| blender-mcp | 3D operations | Blender |
| mcp-server | Tool hub | Network/Locally |
| mcp-client | Test only | Standalone |
| agent | LLM integration | Locally |

## 🙋 Support

- Check logs: `/home/sabeiro/lav/src/blender_cv/mcp_server/mcp-server.log`
- Test connection: `python tests/agent_connection_test.py`
- MCP docs: https://modelcontextprotocol.io/

---
**IMPORTANT:** blender-mcp runs inside Blender, mcp-server exposes available tools, mcp-client is ONLY for testing.