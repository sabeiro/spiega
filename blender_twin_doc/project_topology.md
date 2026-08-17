# Blender-MCP to Blender: Connection Diagrams

Mermaid diagrams for easy editing and markdown rendering.

---

## Connection Topology (Flow Chart)

```mermaid
graph LR
  A[Emacs Editor] -->|prompts & tool calls| B[GPTel MCP Client]
  B -->|JSON-RPC| C[MCP-Hub Server <br/>localhost:8001]
  C -->|MCP Protocol| D[Blender-MCP Server <br/>TCP 8080]
  D -->|Python socket| E[Blender Addon <br/>3D Engine]
  
  style A fill:#e8f4f8,stroke:#2d8ac2
  style B fill:#fdf2d9,stroke:#d69c1e
  style C fill:#e8dff5,stroke:#8b6cb3
  style D fill:#daf5e8,stroke:#3a9c4e
  style E fill:#f5e8d9,stroke:#c2702d
```

---

## Data Flow Sequence

```mermaid
sequenceDiagram
  participant Emacs as Emacs User
  participant GPTel as GPTel MCP Client
  participant MCPHub as MCP-Hub Server
  participant BlenderMCP as Blender-MCP Server
  participant Blender as Blender Engine

  Note over Emacs,Blender: 1. User types prompt in Emacs
  Emacs->>GPTel: Sends prompt: "Create a cube"
  Emacs->>GPTel: Tool call needed
  GPTel->>MCPHub: Request tools
  Note over MCPHub,BlenderMCP: MCP-Hub routes to Blender-MCP
  MCPHub->>BlenderMCP: Forward tool call
  BlenderMCP->>Blender: TCP socket call to 8080
  Note over Blender,BlenderMCP: Execute in Blender
  Blender-->>BlenderMCP: Return result
  BlenderMCP-->>MCPHub: Response
  MCPHub-->>GPTel: Tool response
  GPTel-->>Emacs: Display result in Emacs buffer
```

---

## Tool Call Flow

```mermaid
graph TB
  subgraph Emacs Layer
    A[User Prompt<br/>Create a cube]
    B[GPTel Tool Call<br/>blender_create_object]
  end
  subgraph MCP Layer
    C[MCP-Hub Route]
    D[Tool Router]
  end
  subgraph Blender Layer
    E[Blender-MCP<br/>Python]
    F[TCP Socket<br/>8080]
    G[Blender Addon<br/>Python code]
  end

  A --> B
  B --> C
  C --> D
  D --> E
  E --> F
  F --> G

  style A fill:#e8f4f8
  style B fill:#fdf2d9
  style C fill:#e8dff5
  style D fill:#e8dff5
  style E fill:#daf5e8
  style F fill:#daf5e8
  style G fill:#f5e8d9
```

---

## Full Topology with All Components

```mermaid
graph TD
    subgraph Client Layer["Client Layer"]
        Emcs[Emacs Editor<br/>User Interface]
        Gptel[GPTel MCP Client<br/>MCP Protocols]
    end

    subgraph Router Layer["Router Layer"]
        MHub["MCP-Hub Server<br/>localhost:8001"]
        Git["Git Server"]
        FS["Filesystem Server"]
        Fetch["Fetch Server<br/>uvx mcp-server-fetch"]
    end

    subgraph Blender Layer["Blender Layer"]
        BMCP["Blender-MCP Server<br/>TCP 8080"]
        Socket["Python Socket<br/>TCP Connection"]
    end

    subgraph Execution Layer["Execution Layer"]
        BEngine[Blender Engine<br/>3D Scene]
        Scripts[Blender Scripts<br/>Python]
    end

    Emcs --> Gptel
    Gptel -->|tools routing| MHub
    MHub -->|git tools| Git
    MHub -->|file tools| FS
    MHub -->|fetch tools| Fetch
    MHub -->|blender tools| BMCP
    BMCP -->|TCP socket| Socket
    Socket --> BEngine
    BEngine --> Scripts

    style Emcs fill:#e8f4f8,stroke:#2d8ac2,stroke-width:2px
    style Gptel fill:#fdf2d9,stroke:#d69c1e,stroke-width:2px
    style MHub fill:#e8dff5,stroke:#8b6cb3,stroke-width:2px
    style Git fill:#d5e8d4,stroke:#4e9a06,stroke-width:2px
    style FS fill:#d5e8d4,stroke:#4e9a06,stroke-width:2px
    style Fetch fill:#d5e8d4,stroke:#4e9a06,stroke-width:2px
    style BMCP fill:#daf5e8,stroke:#3a9c4e,stroke-width:2px
    style Socket fill:#daf5e8,stroke:#3a9c4e,stroke-width:2px
    style BEngine fill:#f5e8d9,stroke:#c2702d,stroke-width:2px
    style Scripts fill:#f5e8d9,stroke:#c2702d,stroke-width:2px
```

---

## Setup Commands

```mermaid
flowchart TD
    subgraph Installation["Installation"]
        A[Install Blender MCP] --> B[Install MCP-Hub]
    end
    subgraph Configuration["Configuration"]
        C[Edit ~/.emacs.d/config.el]
        D[Edit mcp-settings.json]
        E[Start MCP-Hub with Blender]
    end
    subgraph Testing["Testing"]
        F[curl localhost:8001/health]
        G[M-x gptel-load-tools]
    end

    A --> C --> D --> E
    E --> F --> G

    style Installation fill:#e8f4f8
    style Configuration fill:#fdf2d9
    style Testing fill:#daf5e8
```

---

## Rendering


```mermaid
graph LR
  A[Emacs] --> B[GPTel] --> C[MCP-Hub] --> D[Blender]
```

---

## Customization Tips

### Change colors:

```mermaid
graph TD
  A[Emacs Editor] --> B[GPTel MCP Client]
  
  style A fill:#e8f4f8,stroke:#2d8ac2
  style B fill:#fdf2d9,stroke:#d69c1e
```

### Add labels:

```mermaid
graph LR
  A[User] -->|prompts| B[Emacs]
  B -->|tool call| C[GPTel]
  C -->|JSON-RPC| D[MCP-Hub]
  
  style A fill:#fff8dc
  style B fill:#f0fff0
```

### Use subgraphs for layers:

```mermaid
graph TD
  subgraph Client
    Emcs[Emacs]
  end
  
  subgraph Server
    MCPHub[MCP-Hub]
  end
  
  Emcs --> MCPHub
```

---

## Quick Commands

```bash
# Render mermaid to HTML
mmd-markdown diagrams.md > diagrams.html

# Or use mmdc
npx mmdc -i diagrams.md -o diagrams.html
```

---

## Summary

Mermaid diagrams are **easy to edit**, **version control friendly**, and **render in most markdown editors**. Just copy the code blocks above into your markdown files!

---

*Created for Blender-MCP Emacs integration*
