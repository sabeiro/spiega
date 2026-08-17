# PlatformIO Mode Overview

:::info {name="Integration Point"}
File: `mcp_server/emacs/emacs.el` (lines 5366-5444)
:::

## PlatformIO Setup

```mermaid
flowchart TD
    A[Detect platformio.ini] --> B{File Exists?}
    B -->|Yes| C[Enable PlatformIO Mode]
    B -->|No| D[Standard Mode]
    
    C --> E[C-c i b Build]
    C --> F[C-c i u Upload]
    C --> G[C-c i s Serial]
    C --> H[C-c i c Clean]
    
    E --> I[use-native-make]
    F --> I
    G --> I
    H --> I
    
    subgraph makefile [Makefile Integration]
        I --> J[Native Makefile]
        J --> K[Use platformio.ini settings]
    end
```

## Available Commands

| Keybinding | Command | Description |
|------------|---------|-------------|
| `C-c i b` | platformio-build | Build the project |
| `C-c i u` | platformio-upload | Upload firmware |
| `C-c i s` | platformio-monitor | Open serial monitor |
| `C-c i c` | platformio-clean | Clean build artifacts |

## Build Process

```mermaid
sequenceDiagram
    participant User as User
    participant Emacs as Emacs
    participant PlatformIO as PlatformIO
    participant Build as Build System
    
    User->>Emacs: C-c i b
    activate Emacs
    Emacs->>Emacs: Call `platformio-build`
    deactivate Emacs
    activate BuildSystem
    BuildSystem->>PlatformIO: Generate Makefile
    PlatformIO->>Build: Compile project
    Build->>PlatformIO: Build Complete
    deactivate BuildSystem
    PlatformIO->>Emacs: Display Build Output
    deactivate Emacs
```

## Upload & Flash

```mermaid
flowchart LR
    A[Project Built] --> B[Check device connected]
    B --> C[C-c i u Upload]
    C --> D[platformio device list]
    D --> E[platformio device detect]
    E --> F[Upload to device]
    F --> G[Verify upload]
    G --> H{Success?}
    H -->|Yes| I[Show success message]
    H -->|No| J[Show error message]
```

## Serial Monitor

```mermaid
flowchart TD
    A[C-c i s] --> B[Call `platformio-monitor`]
    B --> C{Device Connected?}
    C -->|Yes| D[Open serial monitor]
    C -->|No| E[Show device connection error]
    D --> F[Read UART data]
    F --> G{New data?}
    G -->|Yes| H[Display in buffer]
    H --> G
    G -->|No| I[Wait for next data]
```

## Project Structure

```mermaid
graph TD
    A[PlatformIO Project] --> B[platformio.ini]
    A --> C[board.txt]
    A --> D[source/]
    A --> E[firmware/]
    A --> F[build/outputs]
    
    B --> G[env:.*]
    B --> H[platformio.ini:config]
    
    subgraph Configuration [Configuration Files]
        G --> G1[Environment Specific]
        G1 --> G1a[Device Settings]
        G1 --> G1b[Compiler Flags]
    end
```

## Error Handling

```mermaid
flowchart TD
    A[Command Execution] --> B{Build Success?}
    B -->|Yes| C[Success Indicators]
    B -->|No| D{Error Type}
    
    D --> D1[Device Not Found] --> D1a[Show connection error]
    D --> D2[Compilation Error] --> D2a[Show compiler output]
    D --> D3[Upload Error] --> D3a[Show flash error]
    
    C1[C-c i b Success!]
    C2[Build completed]
    C3[Firmware ready]
    
    D2a --> C
    D3a --> C
```

## Device Management

```mermaid
mindmap
  root(PlatformIO Devices)
    Available
      platformio device list
      Show all detected devices
    Connected
      platformio device detect
      Auto-detect connected device
    Upload Target
      platformio device upload <name>
      Specify device by name
      Verify successful upload
```

## Build Flags

```mermaid
flowchart LR
    A[platformio.ini] --> B[env:dev]
    A --> C[env:production]
    
    B --> D[-DCONFIG_...=value]
    C --> E{-DASSERT_DISABLE=1}
    
    D --> F[-DFIRMWARE_REV=2]
    E --> G[-DDEBUG_LEVEL=0]
```

## Clean Artifacts

```mermaid
flowchart TD
    A[C-c i c Clean] --> B[Call `platformio-clean`]
    B --> C[Remove build/outputs/]
    C --> D[Remove .pio/ directory]
    D --> E[Clean all build artifacts]
    E --> F[Project ready to rebuild]
```

## Best Practices

:::info {name="PlatformIO Recommendations"}
1. Always start with `C-c i b` before `C-c i u`
2. Check device connection before uploading with `C-c i s`
3. Use `env:` sections in `platformio.ini` for different devices
4. Clean with `C-c i c` before debugging
5. Keep build directories organized
:::
