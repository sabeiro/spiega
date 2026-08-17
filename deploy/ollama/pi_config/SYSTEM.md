# System Configuration

## Environment
- **OS:** Ubuntu 26.04 LTS
- **Architecture:** x86-64 / ARM64 (Jetson Orin)
- **GPU:** NVIDIA RTX 5060 (8GB VRAM) / Jetson Orin Nano (10 TOPS)
- **RAM:** 32GB (Recommended: 64GB for high-throughput)
- **Storage:** 500GB+ NVMe SSD (Recommended: 1TB with RAID0)
- **Power:** 220W+ continuous (with GPU)
- **Network:** Gigabit Ethernet / Wi-Fi 6

## Hardware Support

### Edge Nodes
- Jetson Orin Nano (4GB RAM, 12 TOPS NPU)
- Jetson Orin NX (16GB RAM, 216 TOPS)
- NVIDIA RTX 5060 (8GB GDDR6)
- RTX 4070/4080 for high-throughput
- Coral TPU for inference acceleration

### Supported Camera Modules
- OV2640 (VGA, 30 FPS)
- IMX219 (HD, 30 FPS)
- IMX477 (QHD, 60 FPS)
- Thermal sensors (MLX90614)
- Depth cameras (ToF, LIAR)
- RGB+Depth fusion

### Sensors
- IMU (accelerometer, gyroscope)
- Barometric pressure
- Temperature & humidity
- Microphone array (8-channel)
- GPS/Geolocation
- LiDAR (optional)

---

## Security Policies

### Network Access
- Local development only (127.0.0.1)
- No external network access in containers
- Port forwarding restricted
- No outbound connections except to trusted services
- Rate limiting on external endpoints

### File Permissions
```bash
# Directory permissions
data/           drwxr-xr-x     755
logs/           drwxr-xr-x     700
config/         drwxr-xrw-     750
models/         drwxr-x---     750
sensitive/      drwxr-----     700

# File permissions
*.py           644
*.pyc          640
*.conf         600
*.key          600
*.pem          600

# Sensitive data
credentials/    drwx------     700
private_keys/   drwx------     700
```

### Container Permissions
- No sudo execution from containers
- Read-only file permissions on shared volumes
- Drop capabilities: `--cap-drop=ALL`
- No privileged containers
- Seccomp profile: `default`
- AppArmor profile: `docker-default`

---

## Deployment Modes

### A) Development Mode

```bash
# Enable debug logging
LOG_LEVEL=DEBUG

# Permissive security
MODE=development
ALLOW_INsecure=1

# Resource limits relaxed
MAX_MEMORY=8GB
MAX_CPU=80%
```

**Features:**
- All MCP tools enabled
- Unlimited context window
- Full system access
- Debug mode enabled
- No rate limiting

### B) Production Mode

```bash
# Production settings
LOG_LEVEL=INFO
MODE=production

# Resource restrictions
MAX_MEMORY=4GB
MAX_CPU=90%
MAX_CONCURRENT=4

# Security hardening
ENCRYPT_SECRETS=1
RATE_LIMIT=100/s
```

**Features:**
- Production-hardened security
- Rate limiting
- Resource capping
- Audit logging
- Health checks

### C) Edge Mode

```bash
# Edge deployment
MODE=edge
LOW_POWER_MODE=1
DEEP_SLEEP_ENABLED=1

# Wake triggers
WAKE_ON_MOTION=1
WAKE_ON_GPIO=1
WAKE_ON_WIFI=1
```

**Features:**
- Deep sleep mode
- Low-power operation
- Local processing only
- Minimal network use
- Battery optimization

---

## Ollama Configuration

### Model Constraints

```yaml
# Max concurrent requests
max_concurrent_requests: 2
context_window: 8192  # tokens
keep_alive: 10m  # minutes
model_memory_limit: 8GB

# Model caching
model_cache_size: 10GB
auto_download: true
prune_old_models: true

# Response time
max_response_time_ms: 30000
min_throughput_rpm: 5
```

### Context Management

```yaml
# Context window
max_tokens: 8192
default_context: 2048
compression: 0.65

# Memory optimization
memory_budget: 16GB
quantization: fp16
keep_alive_window: 110m
```

### Request Queue

```yaml
queue_max_size: 100
queue_timeout_ms: 30000
fallback_model: ""
priority_queue: true
```

---

## Resource Monitoring

### Performance Metrics

```python
# CPU usage
cpu_current: < 90%
cpu_average: < 70%
cpu_spike_threshold: > 100%

# Memory usage
memory_used: < 4GB
memory_average: < 2.5GB
memory_swap: 0

# Disk I/O
read_ops: < 500/s
write_ops: < 100/s
disk_utilization: < 80%

# Network throughput
upload_rate: < 100MB/s
download_rate: < 200MB/s
latency_p99: < 50ms
```

### Alert Thresholds

```bash
# Warning thresholds
LOGGING_MEMORY_WARNING=80%
LOGGING_CPU_WARNING=80%
LOGGING_DISK_WARNING=85%
LOGGING_NETWORK_WARNING=90%

# Critical thresholds
ALERT_MEMORY_CRITICAL=95%
ALERT_CPU_CRITICAL=95%
ALERT_DISK_CRITICAL=95%
ALERT_NETWORK_CRITICAL=95%
```

---

## MCP Server Configuration

### Tool Definitions

```yaml
# Code tools
code-read:
  description: Read source files and logs
  capabilities: [read, analyze]
  scope: [src/, logs/, config/]

code-ask:
  description: Analyze code without execution
  capabilities: [syntax, logic]
  max_tokens: 8192

code-run:
  description: Execute code with restrictions
  capabilities: [execute, output]
  restrictions: [no_network, safe_only]
  timeout_sec: 60
  memory_limit_mb: 512

# MCP Server permissions
max_concurrent_tools: 4
tool_timeout_ms: 30000
request_validation: true
```

### Security Model

```yaml
# Read-only tools
read_only:
  tools: [code-read, code-ask]
  scope: [/src/, /logs/, /data/]

# Write tools (restricted)
write_tools:
  tools: [code-run]
  restrictions: [write_file:/logs/, write_file:/data/]
  no_database: true
  no_external_api: true

# Full access (admin only)
admin_tools:
  tools: []
  scope: [/]
  restrictions: []
```

---

## Network Configuration

### Local Network

```yaml
host: 127.0.0.1
port_ollama: 11434
port_mcp: 18789
port_api: 8000

# Bind address
bind_address: 0.0.0.0
external_access: true
```

### External Access

```yaml
# Production mode
external_network: false

# Allow-listed IPs (optional)
allow_ips: []  # Empty = no access

# Rate limiting
rate_limit_requests: 100/s
rate_limit_window: 60s
```

---

## Process Limits

### CPU Management

```yaml
# Per-process limits
max_cpu_percent: 90
cpu_affinity: []
cpu_isolation: true

# Process controls
nice_level: 19
pdeath_signal: 9
oom_score_adj: -500
```

### Memory Management

```yaml
# Memory limits
process_memory_max: 4GB
cache_memory_max: 2GB
heap_memory_max: 1.5GB

# Swapping policy
memory_swap_enabled: false
memory_overcommit: false
```

### Concurrency Control

```yaml
# Parallelism limits
max_workers: 4
max_file_handles: 1024
max_connections: 300

# Queue management
queue_depth: 100
queue_timeout: 30s
backlog_max: 4
```

---

## Build Requirements

### Base Image

```dockerfile
# Base image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    gcc \
    make \
    cmake \
    build-essential \
    && apt-get clean

# Install Python packages
RUN pip install --no-cache-dir \
    torch>=2.1.0 \
    pytorch-lightning>=2.1.0 \
    opencv-python>=4.8.0 \
    numpy>=1.24.0 \
    pandas>=2.0.0 \
    scipy>=1.11.0 \
    torchvision>=0.16.0 \
    pillow>=10.0.0 \
    uvicorn>=0.23.0 \
    fastapi>=0.100.0
```

---

## Environment Variables

### Development

```bash
export PYTHONPATH=""
export PYTHONDONTWRITEBYTECODE=1
export PY_DEBUG=1
export LOG_LEVEL=DEBUG
export MAX_MEMORY=8GB

# Security relaxed
export ALLOW_INSECURE=1
export SKIP_TLS_VERIFY=1
export SKIP_CERT_VERIFICATION=1
```

### Production

```bash
export PYTHONPATH=""
export PYTHONDONTWRITEBYTECODE=1
export LOG_LEVEL=INFO
export MAX_MEMORY=4GB

# Security hardened
export ALLOW_INSECURE=0
export SKIP_TLS_VERIFY=0
export SKIP_CERT_VERIFICATION=0
export ENCRYPT_SECRETS=1
```

---

## Startup Configuration

### Service Dependencies

```yaml
services:
  ollama:
    requires:
      - docker
      - python
      - mcp-server
    environment:
      - OLLAMA_MODELS=/models
      - OLLAMA_MAX_MEMORY=16GB

  mcp-server:
    depends_on:
      - ollama
    environment:
      - MCP_MODE=production
      - MCP_MAX_WORKERS=4

  web-ui:
    depends_on:
      - mcp-server
    ports:
      - "8000:8000"
```

---

## Health Checks

### Ollama Health

```bash
# Check if Ollama is running
curl -s http://localhost:11434/ping

# Get system statistics
curl -s http://localhost:11434/api/tags

# Check model availability
curl -s http://localhost:11434/api/version
```

### MCP Server Health

```bash
# Check MCP server status
curl -s http://localhost:18789/health

# Get worker stats
curl -s http://localhost:18789/stats
```

---

## Monitoring

### Logging Configuration

```yaml
# Log format
format: json

# Log levels
dev: DEBUG
staging: INFO
prod: INFO
```

### Metrics Export

```yaml
export:
  prometheus: true
  grafana: true
  dataplane: false

scrape_interval: 15s
scrape_timeout: 10s
```

---

## License

MIT License - See LICENSE file for details.
