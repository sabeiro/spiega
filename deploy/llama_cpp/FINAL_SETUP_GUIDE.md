# LLama.cpp Complete Setup Guide

## 🎯 Quick Start (5 minutes)

```bash
# Step 1: Get HuggingFace Token
# 1. Visit https://huggingface.co/settings/tokens
# 2. Create a new "read" token
# 3. Copy the token

# Step 2: Save token (only once)
echo "your-token-here" > ~/.hf_token
chmod 600 ~/.hf_token

# Step 3: Download model
HF_TOKEN=$(cat ~/.hf_token)
HF_TOKEN="$HF_TOKEN" hf download meta-llama/Llama-3.1-8B --include "*.gguf" --local-dir ~/Downloads/llm_model/models --force-download

# Step 4: Start server
cd /home/sabeiro/lav/src/blender_cv/mcp_server/llama_cpp
docker compose down  # Stop existing if running
docker compose up -d

# Access it:
curl http://localhost:8080/health
```

## 📊 Available Models

| Model | Size | Description |
|-------|------|-------------|
| Llama-3.2-1B | 1.5GB | Fast, lightweight |
| Llama-3.1-8B | 4.7GB | Recommended for chat |
| Mistral-7B | 5GB | Good general purpose |
| Gemma-2-9B | 6GB | Alternative to Llama |
| Qwen3-4B | 4GB | Chinese/English |

## 🔧 Configuration

### models/models.yml

```yaml
model_path: |
model_name: |
```

**Update this with your model path** after downloading!

### Models Directory Structure

```bash
~/Downloads/llm_model/models/
├── README.md          # Download instructions
├── .hf_token          # Your HF token (keep secret)
├── Llama-3.1-8B-Q4_K_M.gguf  # Your downloaded model
├── Llama-3.2-1B-Q4_K_M.gguf  # Alternative
└── mistralai/         # Mistral models
```

## 🖥️ Docker Configuration

### docker-compose.yml

```yaml
volumes:
  - ${HOME}/Downloads/llm_model/models/:/models/
```

This points to `~/Downloads/llm_model/models/` (where you save models)

### Ports

Container → Host
- 8080 → 8080 (for API requests)

## 🚦 Commands

```bash
# Check GPU
docker exec llama_cpp nvidia-smi

# View logs
docker logs -f llama_cpp

# Access shell
docker exec -it llama_cpp bash

# Restart
docker compose down
docker compose up -d

# Stop
docker compose down
```

## 💡 Tips

1. **Use smaller models** first to test (Llama-3.2-1B)
2. **Q4_K_M** quantization is the best balance
3. Always use `down` before changing models
4. Store your HF token securely at `~/.hf_token`
5. Check disk space: `df -h /home/sabeiro`

## 🆘 Troubleshooting

**Model not found:**
```bash
ls ~/Downloads/llm_model/models/*.gguf
```

**Port 8080 in use:**
```bash
lsof -i :8080    # Check what's using port 8080
docker stop $(docker ps -aq)  # Find and stop
```

**GPU not working:**
```bash
docker exec llama_cpp nvidia-smi
```

## 📚 Next Steps

1. Download your favorite model
2. Edit `models/models.yml` with the model path
3. Start with `docker compose up -d`
4. Test with `curl http://localhost:8080/health`
5. Generate chat responses

Happy coding! 🎉
