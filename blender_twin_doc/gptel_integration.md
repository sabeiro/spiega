# GPTel Agent Integration with Blender

:::info {name="Integration Point"}
File: `mcp_server/elmcp/el_mcp_server.py` (lines 5366-5444)
:::

## GPTel Agent Overview

```mermaid
flowchart LR
    subgraph gptel [GPTel System]
        A[Model: gpt-4o]
        B[Role: Assistant]
        C[Temperature: 0.9]
    end
    
    subgraph Tools [Available Tools]
        D[GitHub MCP Client]
        E[CLI Tool Manager]
        F[Ollama MCP Backend]
        G[File Access]
        H[MCP Server]
    end
    
    subgraph Modes [Interactive Modes]
        I[Standard GPTel]
        J[Blender Mode]
        K[Debug Mode]
    end
    
    A --> D & E & F & G & H
    A --> I & J & K
    
    I -->|C-c C-g| Send
    J -->|C-c C-b| BlenderPrompt
    K -->|C-c k k| KillProcess
```

## Blender Mode Workflow

```mermaid
sequenceDiagram
    participant User as User
    participant Emacs as Emacs
    participant GPTel as GPTel
    participant MCP as MCP Server
    
    Note over User,GPTel: C-c C-b to enter Blender mode
    User->>Emacs: C-c C-b (gptel-blender-prompt)
    activate Emacs
    Emacs->>Emacs: Enter Blender Mode
    deactivate Emacs
    
    Note over User,BlenderMode: Describe/Ask about Blender state
    User->>GPTel: C-c C-c (Send Command)
    activate GPTel
    
    Note over GPTel,MCP: Send prompt to Ollama with system prompt
    GPTel->>MCP: Generate Blender-specific prompt
    MCP->>MCP: Access Blender environment
    deactivate GPTel
    
    Note over GPTel,User: Receive response
    MCP->>User: Display in current buffer
    deactivate MCP
```

## Mode Activation

```mermaid
flowchart TB
    start((Start)) --> A[C-c C-g]
    A --> B{Mode Selected?}
    B -->|Standard| C[GPTel Standard]
    B -->|Blender| D[Blender Mode]
    B -->|Debug| E[Debug Mode]
    
    C --> F[Normal conversation]
    D --> G[Blender-specific prompts]
    E --> H[System prompt debugging]
    
    G --> I[C-c C-c Send]
    H --> I
    F --> I
    
    I --> J{Response?}
    J -->|Yes| K[Display Result]
    J -->|No| L[Error/Timeout]
    
    K --> M{Continue?}
    L --> M
    M -->|Yes| G
    M -->|No| end((End))
```

## System Prompt Structure

```mermaid
mindmap
  root(Blender Mode System Prompt)
    System Level
      Role: Assistant
      Capabilities:
        Python Scripts
        3D Geometry
        Animation
        Lighting
        Rendering
      Constraints:
        Blender MCP Limits
        500 Objects Max
        4GB Texture Memory
    Context Level
      Active Project
      Blender Version
      Current Objects
      Scene Setup
    User Query Level
      Intent Analysis
      Context Awareness
      Constraint Checking
```

## Command Structure

```mermaid
flowchart LR
    A[C-c C-c GPTel Send] --> B{Command Type}
    
    B --> B1[Blender Query] --> C1{Query Result?}
    B --> B2[Script Generation] --> C2{Valid Script?}
    B --> B3[Code Review] --> C3{Review Complete}
    B --> B4[Model Select] --> C4[LLM Selection]
    
    C1 --> E[Show Result]
    C2 --> D[Execute Script]
    C3 --> E
    C4 --> F[Switch Model]
    
    subgraph Validation [Input Validation]
        B1 --> V1[Check syntax]
        B2 --> V2[Check Blender compatibility]
        B3 --> V3{Security Check}
    end
    
    V1 --> B
    V2 --> B
    V3 --> B
```

## Response Format

```mermaid
flowchart TD
    A[GPTel Response] --> B{Response Type}
    
    B --> B1[Text Response] --> C1[Markdown/Plain Text]
    B --> B2[Code Output] --> C2[Syntax Highlighted]
    B --> B3[Blender Commands] --> C3[Direct Execution]
    B --> B4[Error Messages] --> C4[Error Details]
    
    C1 --> D[Display in Buffer]
    C2 --> D
    C3 --> E[Execute & Update Scene]
    C4 --> F[Show Error Dialog]
```

## Tool Chain

```mermaid
flowchart TD
    subgraph UserLayer [User Interface]
        A[C-c C-g Load]
        B[C-c C-b Blender Mode]
        C[C-c C-c Send]
        D[M-x C-c C-g gptel-kill]
    end
    
    subgraph EmacsLayer [Emacs Processing]
        E[GPTclient Class]
        F[GPTel Client Manager]
        G[Output Buffer]
        H[Desktop Save]
    end
    
    subgraph MCPLayer [MCP Communication]
        I[McpClientManager]
        J[OllamaBackend]
        K[CorsHeaders]
        L[CORS_ALLOW]
    end
    
    subgraph ModelLayer [Model Inference]
        M[Qwen Models]
        N[Llama3.2]
        O[Gemma4]
    end
    
    E --> I
    I --> J
    J --> K --> L
    A --> E
    E --> F --> C
    F --> G
    G --> D
    C --> M & N & O
```

## Debug Mode

```mermaid
flowchart TD
    A[C-c k k Debug Mode] --> B{Debug Type}
    
    B --> B1[System Prompt Debug] --> C1[Show prompt in buffer]
    B --> B2[Tool Call Debug] --> C2[Log tool calls]
    B --> B3[Error Trace Debug] --> C3[Stack trace display]
    
    C1 --> D[Display Prompt]
    C2 --> E[Log Outputs]
    C3 --> F[Show Errors]
    
    D --> G[Analysis Mode]
    E --> G
    F --> G
    
    G --> H{Fix Needed?}
    H -->|Yes| I[Edit Prompts]
    H -->|No| J[Exit Debug]
```

## MCP Clients

```mermaid
flowchart LR
    A[GPTel Agent] --> B[GPTClient]
    
    B --> C[GitHub MCP]
    B --> D[CLI Tools]
    B --> E[Ollama MCP]
    B --> F[File System]
    
    subgraph GitHub [GitHub Operations]
        C --> G1[Repository Operations]
        C --> G2[Issue Management]
        C --> G3[Fork/Collaboration]
    end
    
    subgraph CLI [Command Line]
        D --> D1[File Operations]
        D --> D2[Process Management]
        D --> D3[System Information]
    end
    
    subgraph Ollama [Model Inference]
        E --> E1[qwen2.5:7b]
        E --> E2[qwen3.5:9b]
        E --> E3[llama3.2:latest]
        E --> E4[gemma4:latest]
    end
```

## Context Management

```mermaid
flowchart TB
    subgraph ContextWindows [Context Window Configuration]
        A[Code Provider: 32768 tokens]
        B[Naming Provider: 900 tokens]
        C[Translation Provider: 8192 tokens]
        D[Memory Management]
    end
    
    A --> E[Large Code Files]
    B --> F[Variable Naming]
    C --> G[Text Translation]
    D --> H[Context Caching]
    
    E --> I[Context Optimization]
    F --> I
    G --> I
    
    subgraph Optimization [Token Optimization]
        I --> J[Prioritize Important Info]
        I --> K[Compress Context]
        I --> L[Remove Irrelevant]
    end
```

## Session Management

```mermaid
flowchart TD
    A[Session Start] --> B[Create Context]
    B --> C{Tool Selection}
    
    C --> C1[GitHub] --> D1[Repo Operations]
    C --> C2[CLI] --> D2[File Operations]
    C --> C3[Ollama] --> D3[Model Inference]
    
    subgraph State [Session State]
        D1 --> E[Tool Call Log]
        D2 --> E
        D3 --> E
        E --> F[Conversation History]
    end
    
    F --> G{Continuation?}
    G -->|Yes| H[Next Command]
    G -->|No| I[Session End]
    
    subgraph Persistence [Desktop Save]
        F --> J[Save to Desktop]
        J --> K[Restore on Exit]
    end
```

## Security & Validation

```mermaid
flowchart TD
    A[Input Received] --> B{Security Check}
    
    B --> B1[Malicious Code?] --> C1[Block & Warn]
    B --> B2[File Access?] --> C2[Permission Check]
    B --> B3[Sudo Required?] --> C3[Permission Denied]
    
    C1 --> D[Error Message]
    C2 --> D
    C3 --> D
    
    B --> B4{Valid?} --> E{Execute}
    
    subgraph Validation [Input Validation]
        B1 --> V1[Pattern Matching]
        B2 --> V2[Path Traversal Check]
        B3 --> V3[Command Injection]
    end
    
    V1 --> B
    V2 --> B
    V3 --> B
```

## Interactive Mode

```mermaid
flowchart TD
    subgraph Interaction [User Interaction]
        A[C-c C-c]
        B[Enter Prompt]
    end
    
    subgraph Processing [Command Processing]
        C{Command Parse}
        D[Execute Command]
    end
    
    subgraph Response [Response Handling]
        E{Response Type}
        F[Display Output]
    end
    
    A --> B --> C --> D --> E --> F
    
    subgraph Advanced [Advanced Features]
        G[Markdown Rendering]
        H[Code Syntax Highlight]
        I[Image Display]
    end
    
    F --> G
    F --> H
    F --> I
```

:::info {name="Best Practices"}
1. Always start with `C-c C-g` to load GPTel
2. Use `C-c C-b` for Blender-specific tasks
3. Keep context windows within limits
4. Use debug mode (`C-c k k`) for troubleshooting
5. Check MCP tools availability before use
:::
