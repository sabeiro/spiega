# Unsloth Docker for Ubuntu (CUDA-NVIDIA)

This Dockerfile provides a ready-to-use environment for running Unsloth with Ubuntu and NVIDIA CUDA GPUs.

## Quick Start

```bash
# Build the image
docker build -t unsloth:cuda .

# Run with GPU access
docker run --gpus all -it --rm \
  -v /home/sabeiro/lav/src/:/home/user/ \
  unsloth:cuda \
  bash

# Start Unsloth Studio
python3 -m unsloth.cli.studio --host 0.0.0.0 -p 8888
```

## Dockerfile Components

The Dockerfile installs:

- **Base system**: Ubuntu 24.04 with NVIDIA CUDA 12.5.0
- **CUDA toolkit**: cuDNN, CUDA runtime libraries
- **PyTorch**: Auto-detects and installs CUDA-enabled PyTorch
- **Unsloth dependencies**: xformers, accelerate, bitsandbytes, triton
- **Application files**: Copy from local source

## Why This Works

1. **CUDA Auto-Detection**: Unsloth's installer (`install_unsloth.sh`) automatically detects NVIDIA GPU and installs:
   - `torch-cuda` wheels from official PyTorch index
   - No ROCm needed (ROCm is for AMD/AMD GPUs only)

2. **No ROCm Conflicts**: The image uses official NVIDIA CUDA base, so ROCm is completely absent. PyTorch will use CUDA backend directly.

3. **CUDA Support**: PyTorch will automatically use:
   ```python
   >>> import torch
   >>> torch.cuda.is_available()
   True
   >>> torch.cuda.get_device_name(0)
   'NVIDIA GeForce RTX 5060'
   ```

## Usage in Ubuntu Docker Container

```bash
# Use Ubuntu base with CUDA
FROM nvidia/cuda:12.5.0-cudnn9-devel-ubuntu24.04

# ... rest of setup
```

**Key advantage**: Works directly with unsloth.ai installer URL, which auto-detects CUDA.

## Running Unsloth Training

```python
from unsloth import FastLanguageModel

model = FastLanguageModel.from_pretrained(
    model_name="unsloth/bert-base-uncased",
    max_seq_length=2048,
    load_in_4bit=True,
)

prompt = "What is 6328944 + 12286984 ?"
inputs = model.tokenize(prompt, return_tensors="pt")
outputs = model(**inputs)
print(outputs)
```

## GPU Verification

After building, check CUDA detection:

```bash
docker run --gpus all -it unsloth:cuda python3 -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'CUDA version: {torch.version.cuda}')
print(f'GPU name: {torch.cuda.get_device_name(0)}')
"
```

## Notes

- Uses Ubuntu 24.04 as base (standard for CUDA)
- CUDA 12.5.0-cudnn9-devel (widely compatible)
- PyTorch auto-detects CUDA on NVIDIA GPUs
- Compatible with Ubuntu host machines with NVIDIA GPUs
