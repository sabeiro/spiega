# vLLM Docker Setup - AGENTS.md

Follow this guide to set up vLLM with Llama-3.1-8B-Instruct for LLM inference.

## Quick Start

```bash
cd /models/llm
chmod +x download_model.sh setup.sh

# Start service and let it download model
docker compose up -d

# Wait for model to download and copy to models folder
# Takes ~20-30 minutes on first run
```

## Commands

```bash
# Start
cd /models/llm && docker compose up -d

# Logs
docker compose logs -f vllm

# Stop
docker compose down

# Model info
ls -lh models/
```

## Model Locations

- **Downloaded folder**: `llama-3.1-8b-instruct/`
- **Final location**: `models/llama-3.1-8b-instruct/`
- **Format**: Q4_K_M (4-bit quantized)

## API Access

```bash
curl "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-8b-instruct",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Troubleshooting

- **Container not starting**: Check GPU driver `nvidia-smi`
- **Model not copied**: Run `docker compose exec vllm bash`
- **Permission errors**: `chmod -R 755 models/`
