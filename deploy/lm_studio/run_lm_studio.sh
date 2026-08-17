#!/bin/bash
# Run lm_studio on NVIDIA Jetson (CUDA available)
set -ex

# Create directories
mkdir -p ~/Downloads/{models,cache,logs,uploads}

# Install llm-studio (if not already installed)
pip install --upgrade pip 2>/dev/null
pip install --no-cache-dir lmstudio uvicorn gunicorn fastapi aiohttp requests numpy pandas tqdm
# Run lm_studio
cd ~/Downloads
python3 -m lmstudio.train.cli --port 8000 --host 0.0.0.0 --log-file logs/train.log
