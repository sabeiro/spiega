# LLama.cpp Setup Guide

## Step 1: Get a HuggingFace Token

1. Visit: https://huggingface.co/settings/tokens
2. Click "New token"
3. Create a token with "read" permission
4. Copy the token (it's only shown once!)

## Step 2: Save Your Token

```bash
# Save token in your home directory
echo "your-huggingface-token-here" > ~/.hf_token

# Secure the file
chmod 600 ~/.hf_token

# Export for use
export HF_TOKEN=$(cat ~/.hf_token)
```

## Step 3: Download a Model

### Option 1: Recommended - Meta-Llama-3.1-8B-Instruct (4.7GB)

```bash
# Ensure models directory exists
mkdir -p ~/Downloads/llm_model/models

# Download the model
cd ~/Downloads/llm_model/models
export HF_TOKEN=$(cat ~/.hf_token)
hf download meta-llama/Llama-3.1-8B --include "*.gguf" --local-dir . --force-download
```

### Option 2: Quick Test - Llama-3.2-1B-Instruct (1.5GB)

```bash
cd ~/Downloads/llm_model/models
export HF_TOKEN=$(cat ~/.hf_token)
hf download meta-llama/Llama-3.2-1B --include "*.gguf" --local-dir . --force-download

# Rename to standard name
mv Llama-3.2-1B-Instruct.gguf Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

### Available Models

Use the same command pattern:

```bash
# Llama 3.1 8B (4.7GB) - Best for chat
hf download meta-llama/Llama-3.1-8B --include "*.gguf" --local-dir .

# Mistral 7B (5GB)
hf download mistralai/Mistral-7B-Instruct-v0.3 --include "*.gguf" --local-dir .

# Llama 3.2-1B (1.5GB) - Fastest
hf download meta-llama/Llama-3.2-1B --include "*.gguf" --local-dir .

# Gemma 2 9B (6GB)
hf download google/gemma-2-9b --include "*.gguf" --local-dir .

# TinyLlama 1.1B (0.5GB) - Very fast
hf downloadTinyLlama/TinyLlama-1.1B-Chat-v1.0 --include "*.gguf" --local-dir .
```

## Step 4: Configure Docker

Edit `models/volumes/dev/models.yml` in your models directory:

```yaml
model_path: /models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
model_name: Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

**Important**: Replace with your actual model filename!

## Step 5: Start the Container

```bash
cd /home/sabeiro/lav/src/blender_cv/mcp_server/llama_cpp
docker compose up -d

# Check logs
docker logs llama_cpp

# Access container for manual downloads
docker exec -it llama_cpp bash
cd /models
# Download models manually inside container if needed
```

## Troubleshooting

### Download Failed
1. Check your HF token: `export HF_TOKEN=$(cat ~/.hf_token)`
2. Verify token works: `hf whoami`
3. Try again with force-download: `hf download --include "*.gguf" --local-dir . --force-download`

### Model Already Exists
```bash
# Skip existing files
hf download --include "*.gguf" --local-dir . --force-download --allow-existing
```

### Not Enough Space
Check disk space: `df -h /home/sabeiro`

### View Download Progress
```bash
# Inside container
docker exec -it llama_cpp /bin/bash
cd /models
# Run model download commands manually
```

### Check Docker Compose Configuration
```bash
# View current configuration
cat models/volumes/dev/models.yml

# Verify model filename exists
ls -lh /home/sabeiro/Downloads/llm_model/models/
```

## Quick Start (All Steps)

```bash
# 1. Get HF token
curl -o ~/.hf_token "YOUR_HUGGINGFACE_TOKEN"
chmod 600 ~/.hf_token

# 2. Download Llama-3.2-1B (small test model)
cd /home/sabeiro/Downloads/llm_model/models
hf download meta-llama/Llama-3.2-1B --include "*.gguf" --local-dir .

# 3. Configure model path
cd /home/sabeiro/lav/src/blender_cv/mcp_server/llama_cpp/models/volumes/dev
echo "model_path: |" models.yml >> models.yml
echo "  /home/sabeiro/Downloads/llm_model/models/Llama-3.2-1B.gguf" >> models.yml

# 4. Start
cd /home/sabeiro/lav/src/blender_cv/mcp_server/llama_cpp
docker compose up -d
```

## Tips

- **Smaller models** are better for testing
- **Q4_K_M** quantization is good balance of speed/quality
- Use `--include "*.gguf"` to download only model files
- Always `down` before `up -d` when changing models
- Store token in `~/.hf_token` securely

EOF
cat /home/sabeiro/lav/src/blender_cv/mcp_server/llama_cpp/SETUP_INSTRUCTIONS.md