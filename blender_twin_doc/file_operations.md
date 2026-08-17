# File Operations Overview

:::info {name="File System Integration"}
Integrates Emacs with Blender, PlatformIO, and file management utilities
:::

## Core File Operations

```mermaid
flowchart TB
    subgraph fileops [File Operations]
        A[Read File] --> B[Syntax Highlight]
        A --> C[Code Parsing]
        A --> D[Line Numbering]
        A --> E[Buffer Loading]
        
        subgraph write [Write Operations]
            F[Create File] --> G[Syntax Validation]
            F --> H[Directory Check]
            F --> I[Overwrite Warning]
        end
        
        subgraph edit [Edit Operations]
            J[Targeted Edit] --> K[Text Replacement]
            J --> L[Uniqueness Check]
            J --> M[Conflict Detection]
        end
        
        subgraph backup [Backup System]
            N[backup-by-copying] --> O[~/emacs.d/saves/]
            N --> P[Delete Old Versions]
            P --> Q[Keep 6 New + 2 Old]
        end
        
        subgraph save [Save System]
            R[Desktop Save] --> S[~/emacsd/dotfiles/]
            R --> T[Auto-save Paths]
        end
    end
    
    style fileops fill:#f9f,stroke:#333,stroke-width:1px
    style write fill:#bbf,stroke:#333
    style edit fill:#bfb,stroke:#333
    style backup fill:#fbb,stroke:#333
    style save fill:#fbf,stroke:#333
```

## PlatformIO File Operations

```mermaid
flowchart LR
    A[platformio.ini] --> B[env:.*]
    A --> C[platform:.*]
    A --> D[config:.*]
    
    B --> E[Device:dev]
    B --> F[Device:test]
    
    C --> G[Platform:ESP32]
    C --> H[Platform:Arduino]
    
    subgraph sources [Project Sources]
        E --> I[firmware/]
        E --> J[driver/]
        E --> K[config/]
    end
    
    subgraph buildartifacts [Build Artifacts]
        G --> L[build/outputs/]
        H --> M[.pio/ directory]
    end
    
    subgraph configfiles [Project Configs]
        I --> N[board.txt]
        I --> O[.espidf/]
    end
```

## PlatformIO Commands

```mermaid
flowchart TD
    A[PlatformIO Commands] --> B[C-c i b]
    A --> C[C-c i u]
    A --> D[C-c i s]
    A --> E[C-c i c]
    
    style B fill:#9f9,stroke:#333
    style C fill:#99f,stroke:#333
    style D fill:#99f,stroke:#333
    style E fill:#ccc,stroke:#333
```

## Blender File Operations

```mermaid
flowchart LR
    subgraph blenderfiles [Blender Files]
        A[Import .obj] --> B[Parse Mesh]
        A --> C[Verify Normals]
        A --> D[Check Materials]
        
        subgraph export [Export Options]
            E[Export .glb] --> F[Gltf Format]
            E --> G[PBR Materials]
            E --> H[Scale 1.0]
        end
        
        subgraph blendfiles [Blend Files]
            I[Import .blend] --> J[Load Assets]
            I --> K[Scene Structure]
            I --> L[Object Hierarchy]
        end
    end
    
    B --> F & G & H
    C --> F & G & H
    D --> F & G & H
    J --> F & G & H
    K --> F & G & H
    L --> F & G & H
```

## Read Operations

```mermaid
flowchart TD
    A[Read File Command] --> B[File Access]
    B --> C{File Type?}
    
    C --> C1[Text File] --> D1[Read Content]
    C --> C2[Image File] --> D2[Load as Attachment]
    C --> C3[Large File] --> E[Offset/Read]
    
    D1 --> F[Parse & Highlight]
    D2 --> G[Display in Buffer]
    E --> H[Line by Line Read]
    
    subgraph parsing [Text Parsing]
        F --> I[Syntax Colorization]
        F --> J[Built-in Parser]
    end
    
    subgraph display [Image Display]
        G --> K[Inline Display]
        G --> L[Thumbnail Preview]
    end
    
    subgraph optimization [Large Files]
        H --> E1[Line Offset]
        E1 --> E2[Limit Lines]
        E2 --> E3[Continue Reading]
    end
```

## Write Operations

```mermaid
flowchart TD
    A[Write File Command] --> B[Parent Directory Check]
    
    B --> C{Directory Exists?}
    C -->|No| D[Auto Create]
    C -->|Yes| E[Write to File]
    
    E --> F{File Exists?}
    F -->|No| G[Create New File]
    F -->|Yes| H[Overwrite Warning]
    
    H --> I{User Choice?}
    I -->|Yes| J[Overwrite]
    I -->|No| K[Cancel Write]
    
    G --> L[Write Content]
    J --> L
    
    L --> M[Create Attachment]
    M --> N[Syntax Highlight]
    
    subgraph validation [Content Validation]
        N --> O[Encoding Check]
        N --> P[File Size Check]
        N --> Q[Line Count Check]
        
        subgraph encoding [Encoding Support]
            O --> R[UTF-8 Text]
            O --> S[UTF-8 Image]
        end
    end
    
    subgraph size [Size Limits]
        Q --> T[Truncate at 2000 lines]
        Q --> U[Truncate at 50KB]
    end
```

## Edit Operations

```mermaid
flowchart TD
    A[Edit File Command] --> B{Targeted Edit}
    
    B --> C[Uniqueness Check]
    C --> D{OldText Count?}
    
    D -->|Not Unique| E[Conflict Warning]
    D -->|Unique| F[Perform Edit]
    
    F --> G[Replace Text]
    G --> H[No Overlap Check]
    
    H --> I[Validate Changes]
    I --> J[Apply Edit]
    
    subgraph conflicts [Conflict Handling]
        E --> K[Show Error]
        K --> L[Request Modification]
        
        subgraph merge [Merge Edits]
            M[Nearby Changes]
            M --> N[Merge into One]
        end
    end
    
    subgraph validation [Edit Validation]
        J --> O[Uniqueness Confirm]
        J --> P[No Overlap Check]
        O --> Q[Apply]
        P --> Q
    end
    
    style C fill:#ff9,stroke:#333
    style E fill:#f99,stroke:#333
```

## Backup System

```mermaid
flowchart TD
    subgraph backup [Backup Configuration]
        A[backup-by-copying] --> B[Directories to Backup]
    end
    
    subgraph locations [Backup Locations]
        B --> C[~/emacs.d/saves/]
        C --> D[~/lav/tmp/]
    end
    
    subgraph cleanup [Cleanup Strategy]
        E[Cleanup Old Versions] --> F[kept-new-versions 6]
        E --> G[kept-old-versions 2]
        E --> H[Version Control t]
    end
    
    subgraph restore [Restore System]
        I[Restore Backup] --> J[Desktop Restore]
        J --> K[Restore-eager 0]
    end
    
    subgraph schedule [Schedule]
        L[Auto-run On Save] --> M[Backup Files]
        M --> N[Update Version List]
    end
    
    A --> C
    C --> N
    M --> N
    N --> E
    E --> I
```

## Auto-save System

```mermaid
flowchart TD
    subgraph autosave [Auto-save Configuration]
        A[desktop-save t] --> B[Auto-save Enabled]
    end
    
    subgraph savepaths [Save Paths]
        C[Save Directory] --> D[~/emacsd/dotfiles/]
        C --> E[Temporary File Directory]
    end
    
    subgraph restore [Restore Settings]
        F[Confirm Kill Processes nil]
        F --> G[Graceful Shutdown]
        
        subgraph eager [Eager Restore]
        H[desktop-restore-eager 0]
        H --> I[Restore on Exit]
    end
    
    A --> D & E
    D --> J{Save Event}
    E --> J
    
    subgraph events [Trigger Events]
        J --> K[File Modified]
        J --> L[Buffers Changed]
    end
    
    K --> M[Save to Backup]
    L --> M
    M --> N[Update Metadata]
```

## Desktop Save

```mermaid
flowchart LR
    A[Desktop Save Enabled] --> B[Save to Desktop Direct]
    B --> C[~/emacsd/dotfiles/]
    C --> D[Store Config]
    
    subgraph restore [Restore Options]
        E[On Emacs Start]
        F[On Exit]
    end
    
    subgraph settings [Restore Settings]
        G[desktop-restore-eager 0]
        G --> H[Restore on Exit]
    end
    
    D --> I[Desktop Config Ready]
    
    subgraph backuprestore [Backup & Restore]
        J[Backup on Save] --> K[Create Backup]
        K --> L[Delete Old Versions]
        L --> M[Restore on Start]
    end
```

## Large File Handling

```mermaid
flowchart TD
    A[Large File Read] --> B[File Size Check]
    
    B --> C{Under 50KB?}
    C -->|Yes| D[Read Full File]
    C -->|No| E[Use Offset/Read]
    
    D --> F[Parse Content]
    F --> G[Display in Buffer]
    
    subgraph offsetread [Offset/Read Method]
        E --> H[Limit Lines]
        H --> I[Read Specific Range]
        I --> J{Continue?}
        J -->|Yes| K[Increment Offset]
        J -->|No| F
        K --> H
    end
    
    subgraph limits [Reading Limits]
        H --> L[Truncate at 2000 Lines]
        I --> L
    end
    
    D --> L & I
```

## File Type Handling

```mermaid
mindmap
  root(File Type Handling)
    Text Files
      Plain Text
      Markdown
      Org-mode
      Code Files
      Syntax Highlight
      Parsing Functions
    Image Files
      JPEG
      PNG
      GIF
      WebP
      Inline Display
      Thumbnail Preview
    Large Files
      Offset-based Reading
      Line Limits
      Size Limits
    Binary Files
      Raw Data
      Hex Display
    Audio/Video
      Metadata Only
```

## File Operations Summary

| Operation | Command | Function |
|-----------|---------|----------|
| Read File | Read path | Load file into buffer |
| Read with offset | Read path offset limit | Read specific lines |
| Write File | Write path content | Create/write file |
| Edit File | Edit path edits | Targeted text replacement |
| Delete File | bash rm path | Remove file |
| List Files | bash ls | List directory |
| Search Files | bash rg term | Recursive grep |
| Backup | backup-by-copying | Create backup |
| Restore | desktop-restore | Restore config |
| Save | C-x C-s | Save buffer |
| Auto-save | desktop-save | Auto-save enabled |

:::info {name="File Operations Best Practices"}
1. Always check file type before reading
2. Use offset/limit for large files
3. Enable backup on important files
4. Use parent directory creation for writes
5. Validate file encoding
6. Check limits (2000 lines, 50KB)
:::
