# Emacs Configuration Overview

:::info {name="Configuration Location"}
File: `~/.emacs.d/init.el` (or `mcp_server/emacs/emacs.el`)
:::

## System Configuration

```mermaid
flowchart TB
    A[Emacs Startup] --> B[Custom Style]
    A --> C[Environment Setup]
    A --> D[Package Management]
    
    B --> B1[Misterioso Theme]
    B --> B2[Dark Colors #110428]
    B --> B3[Alpha Transparency 95]
    B --> B4[Font Scaling Functions]
    
    C --> C1[PATH + LAV_DIR/bin]
    C --> C2[UTF-8 Encoding]
    C --> C3[Temp Directory ~/lav/tmp]
    C --> C4[Desktop Save Enabled]
    
    D --> D1[Melpa Archives]
    D --> D2[GNU Archives]
    D --> D3[Nongnu Archives]
    D --> D4[Package-on-demand Loading]
```

## Org-mode Configuration

```mermaid
flowchart TD
    subgraph OrgMode [Org-mode Features]
        A1[Visual Line Mode]
        A2[Agenda Custom Commands]
        A3[Export with Publishing]
        A4[Inlin Images Display]
        A5[Src Fontify Native]
        
        subgraph Agenda ["Custom Agendas"]
            B1[Today's Agenda 'r']
            B2[Week's Agenda 'w']
            B3[Week's Deadlines 'q']
        end
    end
    
    A1 --> A2
    A2 --> A3
    A3 --> A4
```

## LLM Integration (Ollama)

```mermaid
flowchart LR
    subgraph Ollama [Ollama Backend]
        A[http://127.0.0.1:11434]
        B[MY_OLLAMA_URL Env Var]
        C[CORS Allow Headers]
    end
    
    subgraph Clients [Emacs Clients]
        D[Ellama Client]
        E[Pi Coding Agent]
        F[GPTel/MCP Client]
    end
    
    subgraph Models [Available Models]
        G[qwen2.5:7b]
        H[qwen3.5:9b]
        I[qwen2.5-coder:3b]
        J[qwen2.5-coder:7b]
        K[qwen2.5-coder:14b]
        L[llama3.2:latest]
        M[gemma4:latest]
    end
    
    A --> D
    A --> E
    A --> F
    subgraph Context["Context Window Config"]
        C1[Code Provider 32768]
        C2[Naming Provider 900]
        C3[Translation Provider 8192]
    end
    C1 --> G & H & K
    C2 --> L
    C3 --> M
```

## Interactive Agents

```mermaid
flowchart TB
    subgraph Agents [Intelligent Agents]
        Pi[Pi Coding Agent]
        GPT[GPTel Agent]
        Ellama[Ellama Chat]
    end
    
    Pi -->|C-c f a| Questions[Ask About]
    Pi -->|C-c f c| Code[Code Complete]
    Pi -->|C-c f r| Review[Code Review]
    Pi -->|C-c f p| Providers[Model Select]
    
    GPT -->|C-c C-g| Send[Send Prompt]
    GPT -->|C-c C-b| Blender[Blender Mode]
    GPT -->|MCP| Tools[GitHub/CLI Tools]
    GPT -->|MCP| Ollama[Ollama Backend]
    
    Ellama -->|C-c C-c| Chat[Chat History]
    Ellama -->|Summarize| Text[Summarize Text]
    Ellama -->|Translate| Lang[Translate]
```

## Keybindings Structure

```mermaid
mindmap
  root(Emacs Keybindings)
    C-c f[a] ellama-ask-about
    C-c f[c] ellama-code-complete
    C-c f[r] ellama-code-review
    C-c f[g] ellama-improve-grammar
    C-c f[w] ellama-improve-wording
    C-c f[i] ellama-chat
    C-c f[p] ellama-provider-select
    C-c f[s] ellama-summarize
    C-c f[t] ellama-translate
    C-c C-g gptel-load-and-call
    C-c C-b gptel-blender-prompt
    C-c C-c gptel-send
    M-x econky-start
    M-x econky-stop
```

## PlatformIO Integration

```mermaid
graph TD
    A[PlatformIO Mode] --> B[platformio.ini Detection]
    B --> C[Build Commands C-c i b]
    B --> D[Upload Commands C-c i u]
    B --> E[Serial Commands C-c i s]
    B --> F[Clean Commands C-c i c]
    C --> G[Native Makefile Use]
    D --> G
    E --> G
    F --> G
```

## Spell Checking

```mermaid
flowchart LR
    A[Flyspell Mode] --> B[Text Mode Hook]
    A --> C[Markdown Mode Hook]
    C --> D[Skip Code Blocks]
    C --> E[Skip URLs]
    
    A --> F[Hunspell Check]
    A --> G[Aspell Check]
    A --> H[English Dictionary en_US]
    
    suborg[Org Mode]
    org --> A
```

## Backup & Version Control

```mermaid
flowchart TD
    A[Backup Configuration] --> B[backup-by-copying]
    B --> C[Directories '~/emacs.d/saves/']
    A --> D[Delete Old Versions]
    D --> E[ kept-new-versions 6]
    D --> F[kept-old-versions 2]
    D --> G[Version Control t]
    
    subgraph DesktopSave [Desktop Save Settings]
        H[desktop-save t]
        I[desktop-restore-eager 0]
        J[confirm-kill-processes nil]
    end
    
    subgraph AutoSave [Auto-save Paths]
        K[Home Directory]
        L[Temporary File Directory]
    end
```

:::info {name="Note"}
This configuration enables AI-assisted coding with multiple LLM backends, platform-specific tools (Blender, PlatformIO), and sophisticated file organization.
:::
