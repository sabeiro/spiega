# LLM Inference Service Configuration

## Overview
This directory contains deployment configuration for a local LLM inference service powered by Unsloth library for efficient fine-tuning and inference on consumer/hobbyist GPUs (RTX 3060, RTX 4060, RTX 5060, etc.).

## Service Architecture

```
┌─────────────────────────────────────────────┐
│  Unsloth Inference Service                   │
│  (Local LLM Inference & Fine-Tuning)         │
├─────────────────────────────────────────────┤
│                                              │
│  ┌──────────────┐  ┌──────────────┐         │
│  │ JupyterHub   │  │ REST Inference│         │
│  │ :8888        │  │ :8000        │         │
│  └──────────────┘  └──────────────┘         │
│                                              │
│  ┌──────────────┐  ┌──────────────┐         │
│  │ VS Code IDE  │  │ Model Manager │         │
│  │ :2222        │  │               │         │
│  └──────────────┘  └──────────────┘         │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ GPU Acceleration (CUDA/cuDNN/cutlass)│   │
│  │ Model Quantization (GGUF, exl2)      │   │
│  │ Flash Attention 2 / XFormers         │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## Deployment Files

- `Dockerfile` - Build image for Unsloth service
- `Dockerfile.coding` - Build image with VS Code devtools
- `docker-compose.yml` - Production deployment configuration  
- `temp-compose.yml` - Quick development deployment
- `install_dependencies.sh` - GPU driver dependencies
- `run_unsloth.sh` - Launch script

## Quick Start

### Development Mode (Local)
```bash
# Use existing Unsloth container as inference service
docker run -d --gpus all \
  -v /home/sabeiro/lav/src/spiega/deploy/unsloth:/workspace \
  -p 8888:8888 -p 8000:8000 -p 2222:22 \
  unsloth \
  python -m unittest discover

# Or run inference via REST API
docker run --gpus all -p 8000:8000 \
  -e MODEL_PATH=/model/gemma-4-E4B-it-Q4_K_M.gguf \
  unsloth \
  unsloth serve --host 0.0.0.0 --port 8000
```

### Docker Compose Deployment
```bash
# Stop services
cd /home/sabeiro/lav/src/spiega/deploy/unsloth
docker compose down

# Start inference service
docker compose up -d

# Check status
docker compose ps
```

## Configuration

### Environment Variables
```bash
# Model Configuration
MODEL_PATH=/model/gemma-4-E4B-it-Q4_K_M.gguf
MODEL_NAME=Model
```

### Ports
- `8888` - Jupyter Hub for model fine-tuning
- `8000` - REST API for inference
- `2222` - VS Code Remote/Devtools SSH

### Volume Mounts
```yaml
-v ${HOME}/Downloads/llm_model/:/workspace/work      # Model storage
-v ${HOME}/Downloads/llm_cache/git/:${HOME}/.pi/agent/git/  # Git cache
-v ${HOME}/Downloads/llm_cache/sessions/:${HOME}/.pi/agent/sessions/  # Jupyter sessions
-v ${HOME}/lav/src/:${HOME}/lav/src/                # Source code (read-only)
```

## API Endpoints

### JupyterHub (Port 8888)
- `/hub/` - Jupyter dashboard
- `/api/sessions` - List running notebooks
- Notebook interface for Unsloth fine-tuning

### REST Inference (Port 8000)
- `/v1/generate` - Text generation
- `/v1/chat/completions` - Chat completions
- `/v1/models` - List available models

## Use Cases

1. **Fine-Tuning**: Use JupyterHub to fine-tune models on custom datasets
2. **Inference**: Query models via REST API for text generation
3. **Experimentation**: Test different quantizations (GGUF, exl2, nf4)
4. **Development**: Connect VS Code to container for debugging

## GPU Support

This service is optimized for NVIDIA GPUs with CUDA compute capability >= 7.0:
- RTX 3060 (12GB)
- RTX 4060 (8GB)  
- RTX 5060 (12GB)
- RTX 4070 (12GB)
- Tesla T4 (16GB)

Performance benchmarks:
- 3060: ~20 tokens/sec (7B quantized)
- 4060: ~25 tokens/sec (7B quantized)
- 5060: ~40 tokens/sec (7B quantized)

## Model Quantization Options

| Format | Quantization | Memory Usage | Speed | Accuracy |
|--------|-------------|--------------|-------|----------|
| GGUF   | Q4_K_M      | ~4.2GB (7B)  | Fast  | High     |
| GGUF   | Q8_0        | ~8.5GB (7B)  | Fast  | Highest  |
| exl2   | 4-bit       | ~2.8GB (7B)  | Fast  | Medium   |
| nf4    | NF4 4-bit   | ~4.0GB (7B)  | Fast  | High     |

## Notes

- Models stored in `${HOME}/Downloads/llm_model/`
- Quantized versions recommended for consumer GPUs
- Use `unsloth` library for efficient memory management
- Session state persisted to `lav/src/pi_config/`

---
