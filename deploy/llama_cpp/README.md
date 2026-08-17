# 🐍 Llama MCP Server

## Quick Start

Current image ghcr.io/ggml-org/llama.cpp:light-cuda

1. **Get HF Token** (One-time):
   - Visit https://huggingface.co/settings/tokens
   - Create "read" token
   - Save: `echo "YOUR_TOKEN" > ~/.hf_token && chmod 600 ~/.hf_token`

2. **Download Model**:
   ```bash
   cd /home/sabeiro/Downloads/llm_model/models
   HF_TOKEN=$(cat ~/.hf_token)
   HF_TOKEN="$HF_TOKEN" hf download meta-llama/Llama-3.1-8B --include "*.gguf"
   ```

3. **Start Server**:
   ```bash
   cd /home/sabeiro/lav/src/blender_cv/mcp_server/llama_cpp
   docker compose up -d
   ```

4. **Test**: `curl http://localhost:8080/health`

## Troubleshooting

- No health check: `docker compose logs`
- Model not found: Check `models/models.yml`
- Port 8080 busy: `lsof -i :8080`
