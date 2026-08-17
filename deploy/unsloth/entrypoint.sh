#!/bin/bash

# Set environment variables
export PYTHONPATH="/root/.local/lib:$PYTHONPATH"
unset PYTHONNOUSERSITE

# Create base environment
unset UNSLOTH_USE_TORCH_COMPILE
unset UNSLOTH_INSTALL_TOKENIZER_FROM_SOURCE
export TRANSFORMERS_CACHE=/root/.cache/huggingface

# Upgrade pip for base installation
python3 -m pip install --upgrade --break-system-packages pip || true

# Install base dependencies
python3 -m pip install --break-system-packages \
    huggingface-hub[text,torch] \
    torch==2.1.2 --index-url https://download.pytorch.org/whl/cpu -c "https://github.com/unsloth/unsloth/raw/main/requirements/requirements-base.txt" \
    --force-reinstall \
    || true

echo "Base environment setup complete"
exec unsloth studio --host=0.0.0.0 --port=8080
