#!/bin/bash

# Model download script for vLLM
# Downloads the first available model from AGENTS.md

set -e

echo "=== vLLM Model Download Script ==="
echo "Model: llama-3.1-8b-instruct (Q4_K_M)"
echo ""

MODEL_PATH="/models/llama-3.1-8b-instruct"
MODEL_FILE="Llama-3.1-8B-Instruct-Q4_K_M.gguf"

# Create directory
mkdir -p "$MODEL_PATH"

# HuggingFace URL for llama-3.1-8b-instruct Q4_K_M
MODEL_URL="https://huggingface.co/TheBloke/Llama-3.1-8B-Instruct-GGUF/resolve/main/Llama-3.1-8B-Instruct-Q4_K_M.gguf"

echo "Downloading model from HuggingFace..."
echo "  URL: ${MODEL_URL}"
echo "  Target: ${MODEL_FILE}"
echo ""

# Download model (use --continue to resume if interrupted)
wget --continue -O "${MODEL_PATH}/${MODEL_FILE}" "${MODEL_URL}"

echo ""
echo "✓ Model downloaded successfully!"
echo "  Location: ${MODEL_PATH}/${MODEL_FILE}"
echo "  Size: $(du -h "${MODEL_FILE}" | cut -f1)"

echo ""
echo "Next steps:"
echo "  1. Start vLLM: docker compose up -d"
echo "  2. Monitor logs: docker compose logs -f vllm"
echo "  3. Access API: http://localhost:8000"
