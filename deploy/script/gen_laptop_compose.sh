#!/bin/bash
# gen_laptop_compose.sh - Update docker-compose_laptop.yml with detected hardware for llama.cpp

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose_laptop.yml"

# Detect system specs with fallback defaults
RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
RAM_GB=${RAM_KB:-3087228160}
RAM_GB=$((RAM_KB / 1048576))
CPU_CORES=$(nproc || echo 8)
CPU_CORES=${CPU_CORES:-16}

# Get GPU info with proper parsing
if command -v nvidia-smi &> /dev/null; then
    GPS_OUTPUT=$(nvidia-smi -L 2>/dev/null | head -1 || echo "")
    if [ -n "$GPS_OUTPUT" ]; then
        # Remove GPU 0: prefix
        GPS_TEMP=$(echo "$GPS_OUTPUT" | sed 's/^GPU 0: //')
        # Remove (UUID: ...) and ) parts
        GPS_NAME=$(echo "$GPS_TEMP" | cut -d'(' -f1 | sed 's/ *$//')
        # Extract VRAM - find X GB
        GPS_VRAM=$(echo "$GPS_OUTPUT" | grep -oE '([0-9]+GB)' | cut -d'[' -f1 | cut -d'B' -f1)
        GPS_VRAM=${GPS_VRAM:-8}
        GPU_NAME="${GPS_NAME:-CPU-only}"
        VRAM_GB="${GPS_VRAM:-8}"
    else
        GPU_NAME="CPU-only"
        VRAM_GB=12
    fi
else
    GPU_NAME="CPU-only"
    VRAM_GB=12
fi

# Final defaults
GPS_NAME="${GPU_NAME:-Unknown}"
GPS_VRAM=${VRAM_GB:-8}

# Calculate limits
GPS_VRAM_LIMIT=$((GPS_VRAM * 75 / 100))
[ $GPS_VRAM_LIMIT -lt 6 ] && GPS_VRAM_LIMIT=6
RAM_LIMIT=$((RAM_GB * 80 / 100))
[ $RAM_LIMIT -lt 24 ] && RAM_LIMIT=24
CPU_LIMIT=$((CPU_CORES * 80 / 100))
[ $CPU_LIMIT -lt 12 ] && CPU_LIMIT=12

LLAMA_VRAM=$((GPS_VRAM_LIMIT * 1024 * 1024))

echo "== Laptop Compose Generator (llama.cpp) =="
echo "Detected:"
echo "  RAM:    ${RAM_GB}GB"
echo "  CPU:    ${CPU_CORES} cores"
echo "  GPU:    ${GPS_NAME:-CPU-only} (${GPS_VRAM}GB)"
echo ""
echo "Applying limits:"
echo "  Memory: ${RAM_LIMIT}G"
echo "  CPU:    ${CPU_LIMIT}"
echo "  VRAM:   ${GPS_VRAM_LIMIT}G"

# Generate compose content with llama.cpp
cat > "$COMPOSE_FILE" << COMPOSE_EOF
version: "3.9"
services:
  lm_studio:
    image: ghcr.io/merryfish/lm-studio:latest
    container_name: lm-studio
    restart: unless-stopped
    user: root
    ipc: host
    environment:
      - LLAMA_HOST=http://ollama:8080/v1
      - WEBUI_VERSION=latest
      - CHAT_DIR=/chat
      - UPLOADS=/chat
      - CUSTOM_MODELS=/custom_models
      - LLAMA_MODEL=${LLAMA_MODEL:-llama3:8b}
      - LLAMA_MAX_VRAM_BYTES=${LLAMA_VRAM}
      - LLAMA_KEEP_ALIVE=10m
      - LLAMA_N_PARALLEL=2
      - LLAMA_MAX_CONTEXT_SIZE=8192
      - WEBUI_LOAD_CHAT_HISTORY=true
      - SharedMemSize=4gb
      - WEBUI_THEME=dark
      - __INIT__=chat
    volumes:
      - ./docker_data:/docker
      - ./chat:/chat
    depends_on:
      - ollama
    networks:
      - webserver-net
    deploy:
      resources:
        limits:
          memory: ${RAM_LIMIT}G
          cpus: '${CPU_LIMIT}'
        reservations:
          cpus: '${CPU_LIMIT}'
          memory: ${GPS_VRAM_LIMIT}G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 15s
    devices:
      - /dev/nvidia0:/dev/nvidia0
      - /dev/nvideact:/dev/nvideact
      - /dev/nvidiactl:/dev/nvidiactl
      - /dev/nvmap:/dev/nvmap
    security_opt: []

  ollama:
    image: ghcr.io/bartok/llama.cpp:latest
    container_name: ollama
    restart: unless-stopped
    ipc: host
    shm_size: 4gb
    devices:
      - /dev/nvidia0:/dev/nvidia0
      - /dev/nvideact:/dev/nvideact
      - /dev/nvidiactl:/dev/nvidiactl
      - /dev/nvmap:/dev/nvmap
    environment:
      - LLAMA_CUDA=1
      - LLAMA_MAX_VRAM_BYTES=${LLAMA_VRAM}
      - LLAMA_N_CTX=8192
      - LLAMA_N_BATCH=512
      - LLAMA_NUM_PARALLEL=2
      - LLAMA_HOST=0.0.0.0:8080
      - LLAMA_KEEP_ALIVE=24h
    volumes:
      - ./models:/models:rw
    networks:
      - webserver-net

networks:
  webserver-net:
    name: webserver-net
    driver: bridge
COMPOSE_EOF

echo ""
echo "✅ Updated: ${COMPOSE_FILE}"
echo ""
echo "To start services:"
echo "  cd ${SCRIPT_DIR}"
echo "  docker compose -f \"docker-compose_laptop.yml\" up -d"
echo ""
echo "To check logs:"
echo "  docker compose -f \"docker-compose_laptop.yml\" logs"
