# Unified System View

:::info {name="Unified System Architecture"}
Complete system integration view
:::

## Complete System Integration

```mermaid
flowchart TB
    subgraph complete [Complete System]
        A[Desktop Environment] --> B[Web Server]
        B --> C[PlatformIO Build System]
        
        C --> D[Emacs Core]
        D --> E[Emacs LISP]
        E --> F[Org-mode Integration]
        
        subgraph integration [Integration Layer]
        F --> G[MCP Protocol]
        G --> H[Model Context Protocol]
        H --> I[Ollama Server]
        I --> J[Model Registry]
        end
        
        subgraph models [Models Layer]
            subgraph qwen [Qwen Models]
            I --> K[qwen2.5:7b]
            K --> L[qwen3.5:9b]
            L --> M[qwen2.5-coder:3b]
            M --> N[qwen2.5-coder:7b]
            N --> O[qwen2.5-coder:14b]
            end
            
            subgraph llama [Llama Models]
            I --> P[llama3.2:latest]
            P --> Q[llama3.1:8b]
            end
            
            subgraph gemma [Gemma Models]
            I --> R[gemma4:latest]
            R --> S[gemma4:26b]
            end
            
            subgraph context [Context Providers]
            G --> T[Code Provider: 32768]
            G --> U[Naming Provider: 900]
            G --> V[Translation: 8192]
            end
        end
        
        J --> K
        L --> K & N & O
        M --> N
        N --> O
        O --> W[Code Analysis]
        W --> X[Code Generation]
        W --> Y[Naming Suggestions]
        W --> Z[Translation Services]
        
        P --> Q
        Q --> T
    
        R --> S
        S --> W
    
        T --> A1[Text Translation]
        U --> B1[Variable Naming]
        V --> C1[Context Optimization]
    
        subgrid[Outputs]
        O --> D1[Gltf Models]
        W --> D2[Code Updates]
        X --> D2
        Y --> B2[Naming Updates]
        Z --> C2[Translation Updates]
        T --> C3[Context Updates]
        U --> A2[Naming Updates]
        B1 --> B2
        end
        
        subgrid[Debug Mode]
        L --> E1[Debug Mode]
        E1 --> F1[Interactive Controls]
        F1 --> G1[Pause/Resume]
        F1 --> H1[Step Controls]
        F1 --> I1[Error Display]
        end
        
        subgrid[Desktop Save]
        F --> J1[Desktop Save]
        J1 --> K1[Backup System]
        K1 --> L1[Version Control]
        L1 --> M1[Session Management]
        M1 --> N1[Auto-save Hooks]
        N1 --> O1[Restore on Exit]
        Q --> O1
        end
        
        style complete fill:#e8f5e9,stroke:#2e7d32
        style integration fill:#e1f5fe,stroke:#0277bd
        style models fill:#f3e5f5,stroke:#7b1fa2
        style grid fill:#fff3e0,stroke:#e65100
        subgrid fill:#fce4ec,stroke:#c2185b
        subgrid fill:#c8e6c9,stroke:#388e3c
```

## End-to-End Flow

```mermaid
flowchart LR
    subgraph flow [End-to-End Flow]
        A[Source Code Input] --> B[Code Parsing]
        B --> C{Context Analysis}
        
        C -->|Code Generation| D[Code Provider]
        C -->|Variable Naming| E[Naming Provider]
        C -->|Text Translation| F[Translation Provider]
        
        D --> G[qwen3.5:9b]
        D --> H[qwen2.5:7b]
        
        E --> O[llama3.2:latest]
        F --> P[gemma4:latest]
        
        subgrid[Models]
        G --> Q[Model Inference]
        H --> Q
        O --> Q
        P --> Q
        
        Q --> R{Response Type}
        R -->|Text| S[Markdown Response]
        R -->|Code| T[Syntax Highlight]
        R -->|Error| U[Error Display]
        R -->|Debug| V[Debug Controls]
        end
        
        V --> W[Interactive Debug]
        T --> X[Output Buffer]
        S --> X
        U --> Y[Error Console]
        Y --> Z[Error Display]
        Z --> X
        
        subgrid[Output]
        X --> A1[Code Updates]
        X --> B1[Naming Updates]
        X --> C1[Translation Updates]
        A1 --> D1[Gltf Model]
        A1 --> A2[Desktop Save]
        A2 --> B2[Backup System]
        C1 --> B3[Translation Updates]
        B3 --> C2[Translation Updates]
        end
        
        style flow fill:#e1f5fe,stroke:#0277bd
        style grid fill:#fce4ec,stroke:#c2185b
    end
    
    subgrid:org-inlin-images-display --> W1[Image Display]
    W1 --> X1[Buffer Display]
    X1 --> Y1[Desktop Save]
    Y1 --> Z1[Backup System]
    
    style subgrid:org-inlin-images-display fill:#fff3e0,stroke:#e65100
    style W1 fill:#fce4ec,stroke:#c2185b
    style X1 fill:#e3f2fd,stroke:#1565c0
    style Y1 fill:#c8e6c9,stroke:#388e3c
    style Z1 fill:#e8f5e9,stroke:#2e7d32
```

## Model Selection Strategy

```mermaid
flowchart TD
    subgraph selection [Model Selection Strategy]
        A{Task Type?}
        
        A -->|Code Small| B[qwen2.5-coder:3b]
        A -->|Code Medium| C[qwen2.5-coder:7b]
        A -->|Code Large| D[qwen2.5-coder:14b]
        A -->|Code Analysis| E[qwen3.5:9b]
        A -->|Code Generation| F[qwen2.5:7b]
        A -->|Variable Naming| G[llama3.2:latest]
        A -->|Text Translation| H[gemma4:latest]
        
        subgrid[Performance]
        B --> I[Fast Generation]
        I --> J[Small Context]
        
        subgroup[Code Quality]
        C --> K[Medium Code]
        K --> L[Better Accuracy]
        K --> M[Code Review]
        L --> M
        
        subgrid[Advanced]
        D --> N[Complex Code]
        N --> O[High Accuracy]
        N --> P[Advanced Analysis]
        O --> P
        
        subgrid[Precision]
        E --> Q[Precision Analysis]
        Q --> R[Best Accuracy]
        Q --> S[Advanced Analysis]
        R --> S
        
        subgrid[Safety]
        F --> T[Code Safety]
        T --> U[Standard Mode]
        U --> V[Production Ready]
        
        style selection fill:#c8e6c9,stroke:#388e3c
        style subgrid fill:#fff3e0,stroke:#e65100
        style subgrid fill:#e8f5e9,stroke:#2e7d32
        style subgrid fill:#fce4ec,stroke:#c2185b
        style subgrid fill:#e3f2fd,stroke:#1565c0
        end
    end
    
    subgrid:org-inlin-images-display --> W2[Image Display]
    W2 --> X2[Buffer Display]
    X2 --> Y2[Desktop Save]
    Y2 --> Z2[Backup System]
    style subgrid:org-inlin-images-display fill:#fff3e0,stroke:#e65100
    style W2 fill:#fce4ec,stroke:#c2185b
    style X2 fill:#e3f2fd,stroke:#1565c0
    style Y2 fill:#c8e6c9,stroke:#388e3c
    style Z2 fill:#e8f5e9,stroke:#2e7d32
```

## System Context

```mermaid
flowchart TB
    subgraph context [System Context]
        A[Emacs Core] --> B[PlatformIO System]
        B --> C[Build Manager]
        C --> D[Model Integration]
        D --> E[Context Window]
        E --> F[Ollama Server]
        F --> G[Model Registry]
        
        G --> H[qwen2.5:7b]
        H --> I[MCP Protocol]
        I --> J[Tool Calls]
        
        subgrid[Tools]
        J --> K[Code Provider]
        K --> L[text Provider]
        L --> M[naming Provider]
        M --> N[Translation Provider]
        
        subgrid[Debug Controls]
        F --> O[Debug Mode]
        O --> P[Interactive Controls]
        P --> Q[Pause/Resume]
        Q --> R[Step Controls]
        R --> S[Error Display]
        end
        
    subgrid[Desktop Save]
        S --> T[Desktop Save]
        T --> U[Backup System]
        U --> V[Version Control]
        V --> W[Auto-save Hooks]
        W --> X[Session Management]
        end
        
    X --> Y[Restore on Exit]
    Q --> Y
    Y1 --> Y
    
    subgrid:[Outputs]
    Z1 --> A1[Gltf Models]
    A1 --> A2[Code Updates]
    A2 --> A3[Naming Updates]
    A3 --> A4[Translation Updates]
    end
        
    style context fill:#e1f5fe,stroke:#0277bd
    style subgrid fill:#fff3e0,stroke:#e65100
    end
    
    style A1 fill:#fce4ec,stroke:#c2185b
    style A2 fill:#fce4ec,stroke:#c2185b
    style A3 fill:#fce4ec,stroke:#c2185b
    style A4 fill:#fce4ec,stroke:#c2185b
    style Y fill:#c8e6c9,stroke:#388e3c
    style Z1 fill:#c8e6c9,stroke:#388e3c
```

## Best Practices

:::info {name="Unified System Best Practices"}
1. Select appropriate model for each task
2. Maintain context window efficiency
3. Use debug mode for active development
4. Enable desktop save for backups
5. Monitor performance metrics
6. Keep security measures active
7. Document system architecture
8. Use MCP protocol consistently
:::
