#!/bin/bash
# GGUF Model Downloader (No HF Token Required)
# Usage: ./download_gguf.sh <model-name>

set -e

MODELS=(
    "llama-3.1-8b-instruct-q4_K_M.gguf"
    "llama-3.2-3b-instruct-q4_K_M.gguf"
    "llama-3.3-70b-instruct-q8_0.gguf"
    "mixtral-8x7b-v0.1-q4_K_M.gguf"
    "mistral-7b-v0.3-q4_K_M.gguf"
    "mistral-nemo-12b-instruct-q4_K_M.gguf"
    "phi-3-mini-4k-instruct-q4_K_M.gguf"
    "gemma-2-2b-it-q4_K_M.gguf"
    "qwen2.5-7b-instruct-q4_K_M.gguf"
    "llava-1.5-7b-hf-q4_K_M.gguf"
)

MODEL=${1:-${MODELS[0]}}
OUTPUT_DIR="${HOME}/models/gguf"
mkdir -p "${OUTPUT_DIR}"
MODEL_PATH="${OUTPUT_DIR}/${MODEL}"

echo "Downloading ${MODEL}..."

# Try to download - handle various model sources
for url in "https://huggingface.co/${MODEL}" "https://huggingface.co/${MODEL%.*}/resolve/main/${MODEL}"; do
    echo "Trying: $url"
    if curl -s -L -o "${MODEL_PATH}" "${url}"; then
        echo "✅ Downloaded to: ${MODEL_PATH}"
        ls -lh "${MODEL_PATH}"
        break
    else
        echo "❌ Failed: $url (404 or no token needed)"
    fi
done
