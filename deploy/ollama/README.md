# Ollama MCP Server

## Purpose
Run local coding assistant (via pi-coding-agent) with Ollama.

## Hardware Options

### Acer Laptop (NVIDIA RTX 5060)
```bash
cd /home/sabeiro/lav/src/blender_twin/mcp_server/ollama
docker compose -p acer -f docker-compose.acer.yml up -d
```
**Ports**: `11434` (Ollama), `18789` (MCP)

---

### Jetson Orin Nano (ARM, 8GB RAM)
```bash
cd /home/sabeiro/lav/src/blender_twin/mcp_server/ollama
docker compose -p jetson -f docker-compose.jetson.yml up -d
```
**Ports**: `11434` (Ollama), `18789` (MCP)

---

## Usage

### 1. Start Container
```bash
cd ~/lav/src/blender_twin/mcp_server/ollama
docker compose [acer|jetson] up -d
```

### 2. Pull Model
```bash
docker exec -it ollama-acer-<hostname> ollama pull llama3.2:1b
# or
docker exec -it ollama-jetson-<hostname> ollama pull llama3.2:1b
```

### 3. Chat
```bash
docker exec -it ollama-acer-<hostname> ollama run llama3.2:1b
docker exec -it ollama-jetson-<hostname> ollama run llama3.2:1b
```

### 4. Pull All Models
```bash
docker exec -it ollama-acer-<hostname> /bin/bash -c "
cd /root/.ollama/models
for dir in */; do
  cd "$dir"
  ollama pull --quiet "$dir"/*
  cd ..
done"
```

## Integration

Add to `~/.zshrc` or `~/.bashrc`:
```bash
# Acer
source ~/lav/src/blender_twin/mcp_server/ollama/docker-compose.acer.yml.env 2>/dev/null || true

# Jetson  
source ~/lav/src/blender_twin/mcp_server/ollama/docker-compose.jetson.yml.env 2>/dev/null || true
```

Then source:
```bash
source ${HOME}/lav/src/blender_twin/mcp_server/ollama/docker-compose.${HOSTNAME}.yml.env
```

## API Endpoints
- **Ollama API**: `http://127.0.0.1:11434`
- **MCP Protocol**: `http://127.0.0.1:18789`

## Troubleshooting
```bash
# Check container
docker compose ps

# Check logs
docker compose logs -f

# Pull model
docker exec -it ollama-${HOSTNAME} ollama pull llama3.2:1b
```
