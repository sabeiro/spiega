# Editor Plugins & Packages

:::info {name="Package Management"}
Emacs Package Management System (ELPA)
:::

## Package Sources

```mermaid
flowchart TB
    subgraph packages [Package Sources]
        A[melpa Archives] --> B[Latest Packages]
        C[GNU Archives] --> D[Stable Packages]
        E[Nongnu Archives] --> F[Ported Packages]
    end
    
    subgraph management [Management]
        G[Melpa Mode] --> H[Auto-refresh]
        G --> I[Package List]
        G --> J[Install/Update]
    end
    
    subgraph dependencies [Dependencies]
        K[package-require] --> L[Dependency Check]
        K --> M[Auto Install]
    end
    
    subgraph ondemand [On-demand Loading]
        N[package-on-demand] --> O[Code Completion]
        O --> P["Don't Load Until Needed"]
        O --> Q[Save Performance]
    end
```

## Available Packages

| Package | Purpose | Description |
|---------|---------|-------|
| `ellama` | AI Assistant | Model integration with Ollama |
| `gptel` | GPT Client | LLM client interface |
| `mcp-ebmc` | MCP Client | Model Context Protocol support |
| `platformio-mode` | PlatformIO | Embedded build system |
| `elpy` | Python IDE | Python development |
| `org-mode` | Org-mode | Org files support |
| `misterioso` | Theme | Dark theme |
| `org-agenda` | Agenda | Custom agenda views |
| `flyspell` | Spell Check | In-line spell checking |
| `dash` | Search | File search |
| `company` | Completion | Completion framework |

## Ellama Integration

```mermaid
flowchart LR
    subgraph ellama [Ellama Integration]
        A[https://github.com/zhupeix/ellama.git] --> B[Model Backend]
        B --> C[Ollama Server]
        
        subgraph clients [Emacs Clients]
            D[Ellama Client]
            E[Pi Coding Agent]
            F[GPTel/MCP Client]
        end
        
        subgraph models [Available Models]
            G[qwen2.5:7b]
            H[qwen3.5:9b]
            I[qwen2.5-coder:3b]
            J[qwen2.5-coder:7b]
            K[qwen2.5-coder:14b]
            L[llama3.2:latest]
            M[gemma4:latest]
        end
        
        subgraph providers [Context Providers]
            N[Code Provider] --> O[32768 tokens]
            P[Naming Provider] --> Q[900 tokens]
            R[Translation Provider] --> S[8192 tokens]
        end
    end
    
    style ellama fill:#e1f5fe,stroke:#0277bd
    style clients fill:#f3e5f5,stroke:#7b1fa2
    style models fill:#e8f5e9,stroke:#2e7d32
```

## GPTel Agent

```mermaid
flowchart TB
    subgraph gptel [GPTel Client]
        A[Client Manager] --> B[Output Buffer]
        B --> C[Desktop Save]
        
        subgraph commands [Commands]
            D[C-c C-g] --> E[Load]
            D --> F[Standard Mode]
            D --> G[Blender Mode]
            D --> H[Debug Mode]
        end
        
        subgraph tools [MCP Tools]
            I[GitHub Client]
            J[CLI Tools]
            K[Ollama MCP]
            L[File Access]
        end
        
        subgraph models [Supported Models]
            M[qwen2.5:7b]
            N[qwen3.5:9b]
            O[gemma4:latest]
            P[llama3.2:latest]
        end
    end
    
    B --> C
    F --> I & J & K & L
    G --> I & J & K & L
```

## PlatformIO Mode

```mermaid
flowchart TD
    subgraph pio [PlatformIO Mode]
        A[platformio-mode.el] --> B[platformio.ini Check]
        
        subgraph commands [Build Commands]
            C[C-c i b] --> D[platformio-build]
            E[C-c i u] --> F[platformio-upload]
            G[C-c i s] --> H[platformio-monitor]
            I[C-c i c] --> J[platformio-clean]
        end
        
        subgraph native [Makefile]
            K[use-native-make] --> L[Native Makefile]
        end
    end
    
    style pio fill:#fff3e0,stroke:#e65100
    style commands fill:#e3f2fd,stroke:#1565c0
    style native fill:#efebe9,stroke:#6d4c41
```

## Org-mode Plugins

```mermaid
flowchart TB
    subgraph orgmode [Org-mode Features]
        A[visual-line-mode] --> B[Visual Line Mode]
        
        subgraph agenda [Agenda System]
            C[org-agenda-clocktable] --> D[Daily Agenda]
            C --> E[Calendar View]
            F[org-agenda-custom] --> G[Custom Commands]
            F --> H[Week Deadlines]
        end
        
        subgraph publishing [Publishing]
            I[org-publish] --> J[HTML Export]
            I --> K[PDF Export]
        end
        
        subgraph export [Export Settings]
            L[org-export-with-toc] --> M[Table of Contents]
            L --> N[Directory Prefix]
        end
        
        subgraph images [Inline Images]
            O[org-inlin-images-display] --> P[Inline Display]
            O --> Q[Thumbnail Preview]
        end
        
        subgraph src [Src Blocks]
            R[org-babel-src-block] --> S[Native Fontify]
        end
    end
    
    B --> D & E & G & H
    G --> I & J & K
    I --> J & K
    M --> J & K
    P --> J & K
    S --> J & K
    J --> L & M & O & R
    K --> L & M & O & R
```

## Custom Commands

| Command | Bind Key | Function |
|---------|----------|----------|
| `econky-start` | `M-x` | Start Econky |
| `econky-stop` | `M-x` | Stop Econky |
| `platformio-build` | `C-c i b` | Build project |
| `platformio-upload` | `C-c i u` | Upload firmware |
| `platformio-monitor` | `C-c i s` | Open serial |
| `platformio-clean` | `C-c i c` | Clean build |

## Completion Frameworks

```mermaid
flowchart TD
    subgraph completion [Completion System]
        A[Company Mode] --> B[Multi-source]
        
        subgraph packages [Packages]
            C[Dash] --> D[File Search]
            C --> E[Command Search]
            C --> F[Git Search]
        end
        
        subgraph company [Company Client] --> G[Prompt]
        G --> H[Completions]
        H --> I[Selection]
    end
    
    B --> D & E & F
    D --> G
    E --> G
    F --> G
    I --> J[Suggestions]
    J --> G
```

## Theme Integration

```mermaid
flowchart LR
    subgraph theme [Theme System]
        A[Misterioso] --> B[Dark Colors]
        B --> C[#110428 Background]
        B --> D[95% Alpha]
        
        subgraph functions [Font Functions]
        E[Custom Font] --> F[Scaling Font]
        E --> G[Prompt Font]
    end
    
    subgraph styles [Styling]
        H[Visual Line Mode] --> I[Line Height]
    end
    
    C --> E & H
    D --> E & H
    
    F --> K[Text Display]
    G --> K
    K --> L[Font Rendering]
    I --> L
```

## Org-mode Agenda

```mermaid
flowchart TB
    subgraph agendas [Agenda System]
        A[org-agenda-custom] --> B[Today's Agenda]
        A --> C[Week's Agenda]
        A --> D[Week's Deadlines]
        
        subgraph commands [Custom Commands]
            E['r' Command] --> F[Today Agenda]
            E --> G[Calendar View]
            E --> H[Schedule List]
            E --> I[Deadlines List]
        end
        
        subgraph views [Agenda Views]
            J[Bullet Point Mode]
            K[Day View]
            L[Month View]
            M[Year View]
        end
    end
    
    B --> K
    C --> L
    D --> M
    H --> F
    I --> G
```

## Spell Checking

```mermaid
flowchart TD
    A[Flyspell Mode] --> B{Text Mode Hook}
    B --> C[Spell Check Enabled]
    
    A --> D[Markdown Mode Hook]
    D --> E[Skip Code Blocks]
    D --> F[Skip URLs]
    
    A --> G[Aspell/Hunspell Check]
    G --> H[English Dictionary]
    H --> I[en_US]
    
    suborg[Org-mode Hook]
    Org --> A
    suborg --> J[Enable Spell Check]
    
    style A fill:#e3f2fd,stroke:#1565c0
    style C fill:#c8e6c9,stroke:#388e3c
    style E fill:#ffcdd2,stroke:#c62828
    style F fill:#ffcdd2,stroke:#c62828
    style G fill:#fff9c4,stroke:#f9a825
```

## Package List

```mermaid
mindmap
  root(Editor Packages)
    AI & LLM
      Ellama Client
      GPTel Agent
      MCP Protocol
      Model Inference
    Build Systems
      PlatformIO Mode
      Makefile Support
    Development Tools
      Python IDE
      Org-mode
      Org-agenda
    Themes
      Misterioso
      Dark Colors
      Font Scaling
    Search & Completion
      Dash Mode
      Company Framework
      Multi-source
    Spell Check
      Flyspell
      Hunspell
      Aspell
    Backup & Save
      Desktop Save
      Auto-save
      Version Backups
    Export & Publishing
      Org-publish
      HTML/PDF Export
      TOC Generation
```

## Package Installation

```mermaid
flowchart TD
    subgraph install [Package Installation]
        A[Melpa Archives] --> B[melpa-mode]
        C[GNU Archives] --> D[Standard Packages]
        E[Nongnu Archives] --> F[Ported Packages]
    end
    
    subgraph management [Package Management]
        G[Install Package] --> H[Add to load-path]
        H --> I[Auto-dependencies]
    end
    
    subgraph ondemand [On-demand Loading]
        J[package-on-demand] --> K[Load on Need]
        K --> L[Save Performance]
    end
    
    B --> G
    D --> G
    F --> G
    I --> M[Reload Emacs]
    M --> N[Packages Ready]
    
    style install fill:#e8f5e9,stroke:#2e7d32
    style management fill:#f3e5f5,stroke:#7b1fa2
    style ondemand fill:#fff3e0,stroke:#ef6c00
```

## Plugin Configuration

```mermaid
flowchart TB
    subgraph config [Configuration Structure]
        A[elpa] --> B[Package Directories]
        B --> C[Site-lisp]
        B --> D[Melpa Cache]
        B --> E[GNU Packages]
    end
    
    subgraph hooks [Mode Hooks]
        F[Text Mode] --> G[Spell Check]
        F --> H[Syntax Highlight]
        F --> I[Indentation]
        
        subgraph markdown [Markdown Hook]
            F --> J[Skip Code Blocks]
            F --> K[Skip URLs]
        end
        
        subgraph org [Org Mode Hook]
            suborg:org-mode --> L[Enable Spell Check]
            suborg:org-mode --> M[Enable Agendas]
        end
    end
    
    subgraph performance [Performance]
        N[Caching] --> O[Load Path Cache]
        N --> P[Package Cache]
        O --> Q[Fast Startup]
    end
    
    style config fill:#e1f5fe,stroke:#0277bd
    style hooks fill:#f3e5f5,stroke:#7b1fa2
    style performance fill:#e8f5e9,stroke:#2e7d32
```

## Best Practices

:::info {name="Editor Plugin Best Practices"}
1. Keep packages updated using `M-x package-refresh-contents`
2. Use on-demand loading for large packages
3. Enable backup before installing new packages
4. Check dependencies before installation
5. Use melpa mode for latest packages
6. Keep package versions compatible
7. Test packages in personal config first
:::
