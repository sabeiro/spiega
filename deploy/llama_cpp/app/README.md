# LLAMA.CPP Docker Setup

## Quick Start

### Option 1: Download a model directly

```bash
# Inside docker container
docker exec -it llama_cpp bash
cd /models
wget https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

```bash
# Or from your host
# Create the models directory on your host first
mkdir -p ~/Downloads/llm_model/models
wget https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf -P ~/Downloads/llm_model/models/
```

Then start the server:
```bash
docker compose up -d
```

### Option 2: Use quantize.sh to download with Git LFS (recommended)

```bash
cd ./app/
./quantize.sh
```

This script will:
1. Install Git LFS
2. Clone a model (Qwen3-4B-Thinking-2507 by default)
3. Convert to GGUF format
4. Restart the server

### Option 3: Quick command for common models

```bash
# Meta-Llama-3.1-8B-Instruct (4.7GB) - Best for chat
wget https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf

# Qwen3-4B (4GB) - Lightweight
wget https://huggingface.co/Qwen/Qwen3-4B-Thinking/resolve/main/Qwen3-4B-Thinking.Q4_K_M.gguf

# Gemma-4-12B (15GB) - Large model  
wget https://huggingface.co/ggml-org/gemma-4-12b-it-GGUF/resolve/main/gemma-4-12b-it-Q5_K_M.gguf

# Mistral-7B-Instruct-v0.3 (5GB)
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/Mistral-7B-Instruct-v0.3-Q5_K_M.gguf
```

## Configuration

- **MODELS_DIR**: `/models` (host: `${HOME}/Downloads/llm_model/models/`)
- **LLM_CACHE_DIR**: `/app/llm_cache` (host: `${HOME}/llm_cache`)
- **Port**: `8089`
- **Threads**: CPU threads (use `--threads` flag for manual override)

## Available Models

| Model | Size | Use Case |
|-------|------|----------|
| Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf | 4.7GB | Chat, general tasks |
| Qwen3-4B-Thinking-Q4_K_M.gguf | 4GB | Lightweight tasks |
| Gemma-4-12B-It-Q5_K_M.gguf | 15GB | Large context tasks |
| Mistral-7B-Instruct-v0.3-Q5_K_M.gguf | 5GB | Fast inference |

## Usage

Access the model at: http://localhost:8089

### API Examples

```bash
# Test API
curl http://localhost:8089

# Generate text
curl http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama-3.1-8b-instruct",
    "messages": [
      {
        "role": "user",
        "content": "Explain quantum computing in simple terms"
      }
    ],
    "max_tokens": 500
  }'

# Stream responses
curl http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama-3.1-8b-instruct",
    "messages": [
      {"role": "user", "content": "Hello"}
    ],
    "stream": true
  }'
```

## Troubleshooting

### No model found
```bash
# Check for models
docker exec llama_cpp find /models -name "*.gguf"
```

### View logs
```bash
docker logs llama_cpp
```

### Kill and restart
```bash
docker compose down
docker compose up -d
```

### Check GPU is detected
```bash
docker exec llama_cpp nvidia-smi
```

## License

MIT
