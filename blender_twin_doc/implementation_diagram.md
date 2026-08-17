---
title: "Digital Twin Architecture - Mermaid Diagram"
description: "Example markdown file with embedded Mermaid diagram rendering"
tags:
  - architecture
  - mermaid
  - diagram
  - digital-twin
date: 2026-06-11
---

# Digital Twin Architecture Overview

This document demonstrates how to embed and render [Mermaid](https://mermaid.js/) diagrams in markdown files for the Blender Digital Twin project.

## System Architecture Flow

```mermaid
flowchart TD
    subgraph Sensors ["IoT Sensor Layer"]
        A[Temperature Sensors] -->|MQTT| B[Messaging Bus]
        C[Humidity Sensors] -->|MQTT| B
        D[Pressure Sensors] -->|MQTT| B
    end

    subgraph Processing ["Processing Layer"]
        B -->|Ingest| E[Data Stream Processor]
        E -->|Normalize| F[Time Series DB]
        E -->|Transform| G[Feature Extractor]
        G -->|Analyze| H[Anomaly Detector]
    end

    subgraph Intelligence ["Intelligence Layer"]
        H -->|Alerts| I[Predictive ML Model]
        I -->|Predictions| J[Decision Engine]
        F -->|Historical Data| K[Knowledge Graph]
    end

    subgraph Visualization ["Visualization Layer"]
        J -->|Commands| L[Control Actions]
        K -->|Entity Relations| M[Graph Database]
        E -->|State Updates| Q[3D WebGL Viewer]
        Q -->|Render| R[Blender Scene]
    end

    subgraph Twin ["Digital Twin Model"]
        R -->|Sync| V[Physics Simulation]
        V -->|Thermal Analysis| W[Heat FEM Solver]
        W -->|Results| Q
    end

    style Sensors fill:#e1f5fe
    style Processing fill:#fff3e0
    style Intelligence fill:#e8f5e9
    style Visualization fill:#f3e5f5
    style Twin fill:#ffe0b2
    linkStyle default stroke:#333,stroke-width:2px
```

## Component Interaction Diagram

```mermaid
sequenceDiagram
    participant Sensor as IoT Sensor
    participant Queue as Message Queue
    participant Stream as Stream Processor
    participant DB as Database
    participant ML as ML Model
    participant Twin as Digital Twin
    participant Display as Visualization

    Sensor->>Queue: Publish Sensor Data
    Queue->>Queue: Store & Route Messages
    Stream->>Queue: Subscribe & Ingest
    Stream->>DB: Insert Time Series Data
    Stream->>DB: Update Knowledge Graph
    ML->>DB: Query Historical Data
    DB-->>ML: Return Time Series
    ML->>Twin: Generate Predictions
    Twin->>Display: Update 3D Visualization
    Display->>Twin: Render Real-time Scene

    Note right of Stream: Data flows left-to-right
    Note right of ML: ML inference happens asynchronously
```

## State Machine for Twin Status

```mermaid
stateDiagram-v2
    [*] --> Initializing
    Initializing --> Connected: Sensors Online
    Connected --> Stable: All Systems Normal
    Connected --> Warning: Minor Deviation
    Warning --> Stable: Auto-Correct
    Warning --> Critical: Issue Escalated
    Critical --> Stable2: Issue Resolved
    Critical --> Warning: Partial Recovery
    Stable --> Warning: Parameter Change
    Stable2 --> Initializing: Reboot

    state "Connected Components" as Connected
    state "Recovering" as Stable2
```

## Data Flow Architecture

```mermaid
graph LR
    subgraph Input ["Input Sources"]
        A1[Edge Devices] --> A2[API Endpoints]
        B1[Manual Inputs] --> A2
    end

    subgraph Storage ["Storage Layer"]
        C1[(Time Series DB)]
        C2[(Graph DB)]
        C3[(Document Store)]
    end

    subgraph Compute ["Compute Layer"]
        D1[Stream Processing]
        D2[Batch Processing]
        D3[ML Inference]
    end

    subgraph Output ["Output Destinations"]
        E1[WebSocket Stream]
        E2[REST API]
        E3[MQTT Pub]
        E4[WebGL Viewer]
    end

    A2 --> C1
    A2 --> C2
    A2 --> C3
    A2 --> D1
    D1 --> C1
    B1 --> D2
    D2 --> C3
    C1 --> D3
    C2 --> D3
    D3 --> E1
    C1 --> E2
    C2 --> E2
    D3 --> E3
    C1 --> E4
    C2 --> E4
```

## Entity Relationship Map

```mermaid
erDiagram
    SENSORS ||--o{ READINGS : "has"
    SENSORS ||--o{ ALERTS : "generates"
    TWIN_MODEL ||--|{ READINGS : "contains"
    TWIN_MODEL ||--o{ SIMULATION : "executes"

    SENSORS {
        string id PK
        string name
        string type
        string status
        timestamp created_at
        timestamp last_seen
    }

    READINGS {
        string id PK
        int sensor_id FK
        timestamp timestamp
        float value
        float quality
    }

    ALERTS {
        string id PK
        string sensor_id FK
        string severity
        timestamp triggered
        string message
    }

    TWIN_MODEL {
        string id PK
        string name
        string version
        string status
        timestamp last_update
    }

    SIMULATION {
        string id PK
        string model_id FK
        simulation_config
        results_json
        timestamp completed
    }
```

## Deployment Pipeline

```mermaid
flowchart LR
    A[Requirements] --> B[Development]
    B --> C[Code Review]
    C --> D[Tests]
    D --> E[Build Docker Image]
    E --> F[Push to Registry]
    F --> G[CI/CD Pipeline]
    G --> H[Deploy Stage]
    H --> I[Smoke Tests]
    I --> J[Deploy Production]
    J --> K[Health Checks]
    K --> L[Monitor Alerts]

    style A fill:#fce4ec
    style B fill:#f3e5f5
    style C fill:#e1f5fe
    style D fill:#e8f5e9
    style E fill:#fff3e0
    style F fill:#fffde7
    style G fill:#f3e5f5
    style H fill:#e1f5fe
    style I fill:#e8f5e9
    style J fill:#f3e5f5
    style K fill:#e1f5fe
    style L fill:#f3e5f5
```

## Class Diagram for Core Classes

```mermaid
classDiagram
    class Sensor {
        +String id
        +String name
        +String type
        +String status
        +List~Reading~readings
        +connect()
        +disconnect()
        +getStatus()
        +getReadings()
    }

    class Reading {
        +Long timestamp
        +Float value
        +Float quality
        +String timestamp ISO8601
    }

    class TwinModel {
        +String id
        +String name
        +String version
        +SimulationModel model
        +String status
        +float last_update_epoch
        +initialize()
        +runSimulation()
        +updateState()
    }

    class SimulationModel {
        +String config
        +Vector parameters
        +double results[]
        +String status
        +setup()
        +compute()
    }

    class Alert {
        +String id
        +String sensor_id
        +int severity
        +String message
        +Long triggered_epoch
    }

    class Database {
        +TimeSeriesDB time_series
        +GraphDB graph
        +DocumentStore doc
        +connect()
        +executeQuery()
        +close()
    }

    Sensor "1" -- "0..*" Reading : contains
    Sensor "*" --o "1" Alert : generates
    TwinModel "1" -- "1" SimulationModel : has
    TwinModel "1" --o "1" Database : uses
    Alert "1" --o "1" Sensor : references
```

## Sequence Diagram - Alert Handling

```mermaid
sequenceDiagram
    participant IoT as IoT Device
    participant Stream as Stream Processor
    participant AlertSys as Alert System
    participant DB as TimeSeries DB
    participant ML as Anomaly Detector
    participant User as User Notification

    IoT->>Stream: Submit anomaly reading
    Stream->>DB: Store reading
    Stream->>ML: Request anomaly check
    %% activation ML
	ML->>DB: Load recent history
    DB-->>ML: Return history window
    ML-->>ML: Compute anomalies
    ML->>ML: Evaluate thresholds
    %% deactivation ML
    ML-->>Stream: Anomaly Detected
    Stream->>AlertSys: Create alert record
    AlertSys->>DB: Persist alert
    AlertSys->>User: Send notification
    User->>AlertSys: Acknowledge/Confirm
    AlertSys->>Stream: Alert resolved
    Stream->>DB: Mark alert closed
```

## Notes

- Mermaid diagrams are rendered by compatible markdown viewers
- Common diagram types supported: flowchart, sequence, class, graph, state, er
- Use appropriate syntax for each diagram type
- Ensure your viewer has Mermaid.js loaded
- For custom styling, see [Mermaid documentation](https://mermaid.js/#/)

## License

This knowledge base content is available under Creative Commons BY-NC-SA 4.0.
