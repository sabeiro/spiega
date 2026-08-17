# Jetson CV - Digital Twin Prototype for On-Prem Deployment

**Prototype project** for on-premises digital twin systems using NVIDIA Jetson hardware, local AI inference, and FEM/physics simulations. **No cloud providers** - fully on-prem solution using local Ollama instances and Jetson Orin Nano for edge computing.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                Digital Twin Ecosystem                      │
├──────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │   Blender   │    │   Visual    │    │   3D        │   │
│  │  Integration│    │   Graphics  │    │             │   │
│  └─────────────┘    └─────────────┘    └─────────────┘   │
│                          │        │            │           │
│  ┌──────────────────────┼─────────┼────────┐  │           │
│  │  Computer Vision     │ FEM      │ Physics│  │           │
│  │  Pose Est.          │ Solver   │ Sim.   │  │           │
│  │  Object Det.        │ Heat     │ CFD    │  │           │
│  └─────────────────────┼─────────┴────────┘  │           │
│                        │                    │           │
│  ┌─────────────────────▼──────────────────▼───┐          │
│  │         Real-World Sensors (IoT)           │          │
│  │  ┌──────────┐ ┌──────────┐ ┌────────────┐ │          │
│  │  │ Camera   │ │ IoT      │ │ OPC-UA     │ │          │
│  │  │ Sensor   │ │ Stream   │ │ MQTT       │ │          │
│  │  └──────────┘ └──────────┘ └────────────┘ │          │
│  └────────────────────────────────────────────┘          │
│                          │                                │
│  ┌───────────────────────▼───────────────────────────────┐│
│  │    Knowledge Graphs │ Optimization Energy              ││
│  │    GraphDB/RDF      │ Engine                           ││
│  └─────────────────────┴─────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
```

## Project Structure

```
blender_cv/
├── README.md                      # This file - Project overview
├── README.org                     # Org mode documentation
├── sys_sync.sh                    # System synchronization script
├── pi_config/                     # MCP agent configuration
│   ├── SKILLS.md                  # Available skills/agents
│   ├── AGENTS.md                  # MCP agent roles
│   ├── SYSTEM.md                  # Core system policies
│   └── SYSTEM_APPEND.md           # Project-specific overrides
├── camera_esp32/                  # ESP32-based IoT cameras
├── camera_py/                     # Python camera implementations
├── camera/                        # Runtime application (TensorRT)
├── controller_apk/                # Android controller applications
├── controller_arduino/            # Arduino-based controllers
├── controller_js/                 # JavaScript controllers
├── controller_m5stack/            # M5Stack hardware integration
├── controller_pico/               # Raspberry Pi Pico integration
├── controller_c/                  # C-based controller implementations
├── heat_fem/                      # FEM thermal analysis (DOLPHIN/FEniCS)
├── manage_jetson/                 # Jetson deployment management
├── media/                         # Output images/videos
├── model/                         # Saved AI models (.onnx, .pt, .engine)
├── phys_opt/                      # Physics optimization engines
├── pose_estimate_of/              # OpenFrameworks C++ models
├── pose_estimate_py/              # PyTorch/Ultralytics models
└── video_to_3d/                   # Video reconstruction pipelines
```

## Hardware Requirements


## Hardware Stack Architecture
- **Storage:** 32GB SSD (expandable to 1TB+ for media)


## Hardware Stack Architecture

### Core Edge Computing (Primary Targets)
- **NVIDIA Jetson Orin Nano** (4GB/8GB RAM) - Primary deployment target
  - JetPack 6.x with TensorRT acceleration
  - Real-time inference (≤100ms latency)
  - Container isolation for multiple services

- **NVIDIA RTX 5060** (desktop) - Alternative for offline rendering
  - High-throughput batch processing
  - 3D scene reconstruction
  - FEM simulation visualization

### Edge IoT Devices (Distributed Sensing)
- **ESP32** (IoT Cameras, MQTT Broker Nodes)
  - WiFi/BLE enabled
  - Deep sleep mode for power efficiency
  - RGB, thermal, depth cameras
  - MQTT pub/sub capabilities
  - Microphone arrays for audio
  - Accelerometer + gyroscope sensors
  - Custom PCB mounting options

- **Arduino Uno R4** (Controller Applications)
  - WiFi & BLE modules
  - Real-time control logic
  - I2C/SPI sensors integration
  - Servo motor drivers
  - ADC for analog signals
  - CAN bus support

- **Raspberry Pi Zero W/2 W** (Lightweight Edge Nodes)
  - Pi Camera Module support
  - CSI camera interfaces
  - LoRaWAN expansion
  - GPIO sensor arrays
  - Lightweight inference (quantized models)

- **Raspberry Pi Pico/Pico 2** (Microcontroller Edge)
  - RP2040 dual-core ARM
  - 125MHz-133MHz CPU
  - PWM control (motors, servos)
  - I2C/SPI sensor buses
  - BLE/UART communication
  - Deep sleep support

- **Raspberry Pi 4/5** (Workstation Deployment)
  - Full desktop applications
  - Multiple CSI camera inputs
  - FEM simulation rendering
  - Docker container hosting
  - High-bandwidth SSD storage

- **M5Stack** (Modular Sensors Platform)
  - ESP32-WROOM + ATwin module
  - AI Kit with Coral TPU
  - LIDAR + cameras
  - Depth cameras (ToF)
  - Accelerometer + gyroscope
  - Microphone array
  - LoRa + WiFi + BLE

### Camera Modules Supported
- **CSI Cameras** (Native Jetson)
  - IMX219 (standard RGB)
  - IMX477 (global shutter)
  - IMX335 (wide angle)
  - IMX415 (depth/3D)
  - RGB + IR + Thermal multi-sensor
  - 4K @ 60fps capable

- **USB Cameras** (Fallback/Development)
  - Logitech C920/C930
  - Intel RealSense D435
  - Microsoft Kinect (legacy)
  - Micro USB cameras

- **ESP32 Cameras** (IoT Vision Nodes)
  - OV2640 (VGA, low cost)
  - OV7670 + V2
  - OV8865 (WVGA, color)
  - MIPI interface options

- **M5Stack Cameras** (Depth Sensing)
  - TOF depth camera
  - RGB depth array
  - 3D point cloud output

### Camera Integration Features
- **Multi-camera fusion** - Sensor data merging
- **Camera calibration** - Intrinsics/Extrinsics
- **Color correction** - White balance
- **HDR processing** - Tone mapping
- **Exposure control** - Auto/manual
- **Focus distance** - Near/far focus
- **Frame rate control** - FPS throttling
- **Buffer management** - Circular queues

### Hardware Communication Interfaces

- **I2C** - Sensor data reading (IMU, temp, pressure)
- **SPI** - Camera modules, display panels
- **UART** - Serial console, BLE dongles
- **GPIO** - Digital I/O, PWM control
- **CAN Bus** - Automotive-grade control
- **Ethernet** - High-bandwidth networking
- **WiFi/BLE** - Wireless sensor networks
- **LoRa** - Low power long-range

### Resource Requirements by Deployment

| Device | RAM | GPU | CPU | Storage |
|--------|-----|-----|-----|---------|
| Jetson Orin | 8GB | 120 TOPS | 4x A76AE | NVMe SSD |
| RTX 5060 | 16GB+ | 6GB GDDR6 | 6-core CPU | |
| Raspberry Pi | 4GB | CPU-only | Quad-core | SD/NVMe |
| ESP32 | 520KB | N/A | Tenspeed | Flash |
| Arduino | 2KB | N/A | N/A | Flash |
| M5Stack | 520KB | Coral TPU | 4GB eMMC | |

### Storage Recommendations
- **NVMe SSD** - Primary models/data (32GB+ minimum)
- **SD Card** - Backup for Pi devices (16GB+ Class 10)
- **USB Flash** - Portable configuration files
- **HDD** - Archival media (8TB+ recommended)

---

## Hardware Requirements

### Minimum Resources
- **Jetson:** 8GB RAM, JetPack 6.x
- **PC Workstation:** 16GB RAM, 4GB+ GPU
- **Edge Nodes:** 4GB+ (Raspberry Pi/Zero)
- **MCU Nodes:** 520KB+ (ESP32/Pico)

---

---

## Core Components

### 1. Computer Vision Pipeline (`camera_py/`, `camera/`)

Real-time pose estimation using TensorRT-accelerated models:

- **pose_estimate_py/** - PyTorch/Ultralytics training & export
  - Train custom pose models with YOLO11n-pose
  - Export to ONNX for TensorRT conversion
  - Batch processing with queue management

- **pose_estimate_of/** - OpenFrameworks C++ for high-performance inference
  - ONNX runtime integration
  - Low-latency deployment

- **model/** - Model artifacts storage:
  - `.pt` - PyTorch models (training)
  - `.onnx` - ONNX Intermediate format
  - `.engine` - TensorRT optimized engines

**Features:**
- CSI camera support (IMX219, RGB, thermal)
- Real-time inference (≤100ms latency)
- Zoom, pan, flip controls
- Photo/video capture
- Histogram and vectorscope displays

### 2. Finite Element Analysis (`heat_fem/`)

Thermal and structural simulations using FEniCSx/DOLPHIN:

- **FEM Mesh** - Adaptive mesh refinement
- **Thermal Analysis** - Heat transfer, conduction, radiation
- **Structural** - Stress, strain, deformation
- **Optimization** - Topology optimization for lightweight designs

**Features:**
- HDF5 output for large datasets
- 30-minute solver timeout
- Mesh quality validation
- Parallel computation (8 cores max)

### 3. Physics Optimization (`phys_opt/`)

Constraint-based optimization engines:

- **Pyomo** - Mathematical modeling
- **IPOPT** - Interior-point optimization
- **Result caching** - 24-hour cache
- **Multi-physics** - Thermal + structural + fluid

### 4. Visualization & 3D (`blender_cv/`, `video_to_3d/`)

3D modeling and rendering:

- **Blender integration** - 3D scene assembly
- **ONNX models** - Direct export to 3D
- **WebGL** - Web-based 3D viewers
- **Export formats** - .obj, .fbx, .glb

### 5. IoT & Sensor Integration

Real-world data ingestion:

- **MQTT** - MQTT broker for sensor pub/sub
- **OPC-UA** - Industrial device integration
- **CoAP** - Lightweight MQTT alternative
- **Sensor fusion** - Multi-sensor data merging
- **Data streams** - High-frequency telemetry

### 6. Edge Computing & Deployment

On-prem deployment capabilities:

- **JetPack 6.x** - NVIDIA accelerated runtime
- **TensorRT** - GPU-accelerated inference
- **ONNX Runtime** - CPU GPU interoperability
- **Model optimization** - Quantization, pruning for edge
- **Docker/Kubernetes** - Container orchestration
- **sys_sync.sh** - System synchronization script

---

## On-Prem Architecture

### Network Design
```
┌──────────────────────────────────────────┐
│    ON-PREM ONLY - No Cloud Connection    │
├──────────────────────────────────────────┤
│  ┌─────────────┐                        │
│  │ Jetson      │                        │
│  │ Orin Nano   │ ─────────────────────► │
│  │ (Edge Node) │  Real-time Inference   │
│  └─────────────┘                        │
├──────────────────────────────────────────┤
│  ┌─────────────┐                        │
│  │ Ollama      │                        │
│  │ Local       │                        │
│  │ Instance    │                        │
│  └─────────────┘                        │
├──────────────────────────────────────────┤
│  ┌─────────────┐                        │
│  │ GraphDB     │                        │
│  │ Knowledge   │                        │
│  └─────────────┘                        │
├──────────────────────────────────────────┤
│  ┌─────────────┐                        │
│  │ MQTT Broker │                        │
│  │ (RabbitMQ)  │                        │
│  └─────────────┘                        │
├──────────────────────────────────────────│
│  ┌─────────────┐                        │
│  │ NVMe SSD    │                        │
│  │ Storage     │                        │
│  └─────────────┘                        │
└──────────────────────────────────────────┘
```

### Security
- **No SSH** from untrusted networks
- **Container isolation** for all services
- **Read-only** file permissions on shared volumes
- **Local LLM** only (Ollama - no API keys)
- **No external** database connections

---

## Digital Twin Capabilities

### What's Included
- **Visual Twin** - 3D models from Blender + pose estimation
- **Physical Twin** - FEM + physics simulations + multi-physics
- **Sensing Twin** - IoT integration, real-time data streams
- **Intelligent Twin** - ML models, knowledge graphs, predictive analytics
- **Optimized Twin** - Energy modeling, resource allocation
- **Connected Twin** - MQTT, OPC-UA, standard protocols

### Skills Available
See `pi_config/SKILLS.md` for complete skill definitions:
- FEM/FEniCS → Structural/mechanical analysis
- Optimization → Energy/resource optimization
- Vision → Real-time object tracking
- Knowledge graph → Component relationships
- IoT → MQTT, OPC-UA integration
- Time series → Historical analysis
- Edge computing → On-device inference

---

## Quick Start

### 1. Environment Setup

```bash
# Load CUDA environment
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export CPATH=$CUDA_HOME/include:$CPATH

source ~/.bashrc
```

### 2. Install Dependencies

```bash
# System packages
sudo apt install python3-opencv python3-numpy

# Python packages
cd camera
pip install -r requirements.txt

# Configure camera (CSI)
sudo /opt/nvidia/jetson-io/jetson-io.py
```

### 3. Build Models

```bash
# Train pose model
cd pose_estimate_py
python train.py

# Export to ONNX
model.export(format='onnx')
mv model.onnx ../model/

# Create TensorRT engine
cd ../camera
python build_engine.py
```

### 4. Run Application

```bash
cd camera
python -m camera.camera_controller

# Or use Docker
docker compose up -d
```

### 5. Deploy Digital Twin

```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

---

## Skills & Agents Configuration

The pi_config/ directory contains MCP agent configurations:
- **SKILLS.md** - All available skills for digital twin operations
- **AGENTS.md** - Agent roles and responsibilities
- **SYSTEM.md** - Core system policies and constraints
- **SYSTEM_APPEND.md** - Project-specific overrides

See [SKILLS.md](mcp_server/ollama/pi_config/SKILLS.md) for complete skill catalog.

---

## Testing & Quality

### Code Quality
- **Unit tests ≥70%** - Coverage requirement
- **Static analysis** - pylint, black, flake8
- **Lint** - No production code without testing
- **Documentation** - Type hints, docstrings

### CI/CD (Local Only)
```bash
# Run tests
pytest -xvs

# Code quality
pylint --errors-only ./src

# Format
black ./src --check --diff
```

### Version Control
```bash
# Check changes
git diff

# Commit
git commit -m "feat: add vision improvement"

# Tag release
git tag -a v1.0.0 -m "Initial Digital Twin Release"
```

---

## Development Guidelines

### Code Style
- **Python** - PEP8, type hints, docstrings
- **C++** - Modern C++17/20, RAII principles
- **Blender** - bpy, operators, operators only

### Documentation
- **Markdown** - Technical documentation
- **Org mode** - Research notes (README.org)
- **API docs** - Sphinx for Python modules

### Testing
- **Unit tests** - Test individual components
- **Integration tests** - MCP tool workflows
- **End-to-end** - Full digital twin scenarios
- **Performance** - Inference latency checks

---

## Deployment Checklists

### Pre-Deployment
- ✅ All dependencies installed
- ✅ Models trained and exported to ONNX
- ✅ Docker containers built
- ✅ Test data generated
- ✅ Logs configured for JSON output

### Post-Deployment
- ✅ Services running (docker compose ps)
- ✅ Logs healthy (docker compose logs | grep ERROR)
- ✅ Models loaded (ollama list)
- ✅ Camera feed active
- ✅ MQTT broker responding

---

## Support & Resources

### Documentation
- **README.org** - Org mode with math/formulas
- **SKILLS.md** - Full skill catalog
- **AGENTS.md** - MCP agent roles
- **SYSTEM.md** - System policies

### External References
- **NVIDIA Jetson** - https://developer.nvidia.com/jetson
- **TensorRT** - https://docs.nvidia.com/deeplearning/tensorrt/
- **ONNX** - https://onnx.ai/
- **Blender** - https://www.blender.org/
- **FEniCSx** - https://fems.readthedocs.io/
- **DOLPHIN** - https://fems.readthedocs.io/

---

## Contributing

1. Fork this prototype repository
2. Create feature branches
3. Add tests for new functionality
4. Update SKILLS.md for new capabilities
5. Submit pull request with documentation

### Code Review Checklist
- [ ] Lint passes (pylint, black, flake8)
- [ ] Unit tests added
- [ ] Code coverage ≥70%
- [ ] Documentation updated
- [ ] SKILLS.md updated (if new skill)

---

## License

MIT License - Feel free to use for on-prem digital twin projects

---

## Archive Notice

**⚠️ Deprecated:** This README.md is a legacy file for archive purposes. All documentation has been moved to the `docs/` directory. Please refer to the official documentation at `/home/sabeiro/lav/docs/` for up-to-date information.

---

## Notes

## Project Highlights

- ⚠️ **Deprecated:** This README.md is a legacy file. Please refer to `/home/sabeiro/lav/docs/` for up-to-date documentation.
- ✅ **Local LLM** - Ollama for agent interactions
- ✅ **Edge computing** - Jetson Orin Nano deployment
- ✅ **Digital twin stack** - Complete FEM + vision + IoT
- ✅ **Standard protocols** - MQTT, OPC-UA, DTCL
- ✅ **No external dependencies** - Self-contained system
