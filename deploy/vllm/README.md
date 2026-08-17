# vLLM MCP Server

Docker-based vLLM setup for LLM inference with GPU acceleration.

## Overview

This project provides a Docker Compose setup for running vLLM (Large Language Model serving) with NVIDIA GPU support. It follows the patterns from the main [src/](/home/sabeiro/lav/src/) project.

## Quick Start

### 1. Initialize Setup

```bash
cd /home/sabeiro/lav/src/blender_cv/mcp_server/vllm
chmod +x download_model.sh setup.sh
./setup.sh
```

### 2. Start vLLM Container

```bash
docker compose up -d
```

### 3. Download Model

```bash
./download_model.sh
```

This will download `llama-3.1-8b-instruct-Q4_K_M.gguf` from HuggingFace.

### 4. Wait for Model to Copy

Download takes ~10-30 minutes depending on your connection. Wait until the model completes copying from container.

### 5. Use vLLM

Once the model is downloaded, vLLM will automatically serve it. Access the API at `http://localhost:8000`.

## Model Information

- **Model**: `llama-3.1-8b-instruct`
- **Format**: GGUF Q4_K_M (4-bit quantized)
- **Location**: `models/llama-3.1-8b-instruct/`
- **Source**: HuggingFace - [TheBloke/Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/TheBloke/Llama-3.1-8B-Instruct-GGUF)

## Docker Compose Configuration

The vLLM container:
- Uses NVIDIA GPU devices
- Mounts local `models/` and `cache/` folders
- Dropped all capabilities for security
- Allocated 8GB shared memory
- Requested 4 CPU cores

## Usage Examples

### Test the API

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-8b-instruct",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Using MCP Client

Once vLLM is running, the MCP server can connect to it for LLM operations.

## Common Commands

```bash
# Start service
docker compose up -d

# Stop service
docker compose down

# View logs
docker compose logs -f vllm

# Run interactive shell in container
docker compose exec vllm bash

# Copy model from container
docker compose exec vllm bash -c "ls -lh /models/"
```

## Troubleshooting

### Image Pull Errors

If you get "pull access denied" errors, try pulling the image manually:

```bash
docker pull vllm/vllm-openai:latest
```

Alternative images:
- `vllm/vllm-openai:latest` - Generic vLLM OpenAI API
- `vllm/vllm-nightly-cu121` - Nightly builds with PyTorch 2.4+
- `vllm/vllm-jetpack` - NVIDIA JetPack versions

## Security

- Container drops all capabilities
- Security option `no-new-privileges:true`
- Read-only filesystem for model directory
- Named volumes for data isolation

## Environment Variables

Available environment variables:
- `VLLM_MODEL` - Path to model directory
- `VLLM_CACHE` - Path to cache directory
- Custom environment variables can be added to `docker-compose.yml`

## References

- [vLLM Official Documentation](https://docs.vllm.ai)
- [GGUF Models](https://huggingface.co/TheBloke)
- [Docker GPU Support](https://docs.docker.com/desktop/linux/gpu/)

## License

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

*Part of the Blender CV MCP Server project*
