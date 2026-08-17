#!/bin/bash
set -e

MODELS_DIR="${MODELS_DIR:-/models}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "  LLAMA.CPP - MODEL DOWNLOADER"
echo "=========================================="
echo ""
echo "MODELS_DIR: ${MODELS_DIR}"
echo ""

# Check if directory exists, create if not
mkdir -p "${MODELS_DIR}"

# Function to download model with Git LFS
download_with_lfs() {
    local model_url="$1"
    local model_name="$(basename "$model_url")"
    
    echo "=========================================="
    echo "  DOWNLOADING: ${model_name}"
    echo "=========================================="
    echo "Git LFS cloning..."
    
    cd "${MODELS_DIR}"
    GIT_LFS_SKIP_SMUDGE=0 git clone "${model_url}" 2>&1 || {
        echo "Git LFS clone failed. Trying direct download..."
        echo "=========================================="
    }
    
    cd "${SCRIPT_DIR}/.."
    return 0
}

# Function to download model with wget
download_with_wget() {
    local model_url="$1"
    
    echo "=========================================="
    echo "  DOWNLOADING: ${model_url}"
    echo "=========================================="
    
    wget --show-progress -O "${MODELS_DIR}/$(basename "$model_url")" "${model_url}" 2>&1
}

# Available models to download
echo "Available model options (select one to download):"
echo "=========================================="
echo ""
echo "1. Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf (4.7GB recommended)"
echo "   URL: https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
echo ""
echo "2. Qwen3-4B-Thinking-2507-Q4_K_M.gguf (~4GB)"
echo "   URL: https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507/resolve/main/Qwen3-4B-Thinking-2507.Q4_K_M.gguf"
echo ""
echo "3. Gemma-4-12B-It-Q5_K_M.gguf (~15GB)"
echo "   URL: https://huggingface.co/ggml-org/gemma-4-12b-it-GGUF/resolve/main/gemma-4-12b-it-Q5_K_M.gguf"
echo ""
echo "4. Mistral-7B-Instruct-v0.3-Q5_K_M.gguf (~5GB)"
echo "   URL: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/Mistral-7B-Instruct-v0.3-Q5_K_M.gguf"
echo ""
echo "=========================================="
echo ""
read -p "Enter model number to download (1-4, or 's' to skip to selection): " choice

# Prompt for model URL if no selection
if [[ "$choice" != "s" ]] && ! download_with_lfs \
    "https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"; then
    echo "Git LFS failed. Downloading with direct link..."
    if ! download_with_wget \
        "https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"; then
        echo "=========================================="
        echo "  WARNING: Download failed!"
        echo "=========================================="
        echo "Please try downloading the model manually:"
        echo "  cd ${MODELS_DIR}"
        echo "  wget https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
        echo ""
    fi
fi

# Check for GGUF files
echo "=========================================="
echo "Checking for available GGUF models..."
echo "=========================================="

GGUF_FILES=$(find "${MODELS_DIR}" -name "*.gguf" -type f -size +10M 2>/dev/null | sort)

if [[ -z "${GGUF_FILES}" ]]; then
    echo "No GGUF models found in ${MODELS_DIR}"
    echo "Models directory is empty or no .gguf files detected"
    exit 1
else
    echo "Found GGUF models:"
    echo "${GGUF_FILES}"
fi

# Update docker-compose to use the latest model
echo "=========================================="
echo "Updating docker-compose to restart server..."
docker-compose down --remove-orphans 2>/dev/null || true
docker-compose up -d

echo "=========================================="
echo "  DONE! Server is running."
echo "=========================================="
echo "Access llama.cpp at: http://localhost:8089"
echo "=========================================="
