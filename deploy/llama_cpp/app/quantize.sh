#!/bin/bash
set -e

MODELS_DIR="${MODELS_DIR:-/models}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "===================================="
echo "  LLAMA.CPP - MODEL SETUP"
echo "===================================="
echo ""
echo "MODELS_DIR: ${MODELS_DIR}"
mkdir -p "${MODELS_DIR}"

cd "${MODELS_DIR}"

echo "===================================="
echo "  Installing Git LFS..."
echo "===================================="
git lfs install || echo "Git LFS may already be installed"

echo ""
echo "===================================="
echo "  Available models to clone:"
echo "=============================="
echo ""
echo "  1. Qwen3-4B-Thinking-2507 (4GB - lightweight)"
echo "  2. Meta-Llama-3.1-8B-Instruct (4.7GB - recommended)"
echo "  3. Gemma-4-12B-It (15GB - large)"
echo "  4. Mistral-7B-Instruct-v0.3 (5GB)"
echo ""
echo "Choose one model to download:"
echo ""
read -p "Enter model ID (or press Enter for default Qwen3-4B): " model_id

case ${model_id} in
    "1")
        echo "Cloning: Qwen3-4B-Thinking-2507"
        GIT_LFS_SKIP_SMUDGE=0 git clone "https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507" "Qwen3-4B-Thinking-2507"
        ;;
    "2")
        echo "Cloning: Meta-Llama-3.1-8B-Instruct"
        GIT_LFS_SKIP_SMUDGE=0 git clone "https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF" "Meta-Llama-3.1-8B-Instruct-i1-GGUF"
        ;;
    "3")
        echo "Cloning: Gemma-4-12B-It"
        GIT_LFS_SKIP_SMUDGE=0 git clone "https://huggingface.co/ggml-org/gemma-4-12b-it-GGUF" "gemma-4-12b-it-GGUF"
        ;;
    "4"|"mistral")
        echo "Cloning: Mistral-7B-Instruct-v0.3"
        GIT_LFS_SKIP_SMUDGE=0 git clone "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF" "Mistral-7B-Instruct-v0.3-GGUF"
        ;;
    "")
        echo "Cloning: Qwen3-4B-Thinking-2507 (default)"
        GIT_LFS_SKIP_SMUDGE=0 git clone "https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507" "Qwen3-4B-Thinking-2507"
        ;;
    *)
        echo "Invalid model ID. Using default Qwen3-4B-Thinking-2507"
        GIT_LFS_SKIP_SMUDGE=0 git clone "https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507" "Qwen3-4B-Thinking-2507"
        ;;
esac

echo ""
echo "===================================="
echo "  Converting to GGUF format..."
echo "=============================="

# Find the converted GGUF file
GGUF_FILE=$(find "${MODELS_DIR}" -name "*.gguf" -type f -size +10M 2>/dev/null | head -1)

if [[ -z "${GGUF_FILE}" ]]; then
    echo "ERROR: No GGUF file found. Did the clone succeed?"
    ls -lah "${MODELS_DIR}"
    exit 1
else
    echo "Found GGUF model: ${GGUF_FILE}"
fi

echo ""
echo "===================================="
echo "  Starting llama-server..."
echo "=============================="

# Restart docker-compose to load new model
cd "${SCRIPT_DIR}/.."
docker-compose down --remove-orphans 2>/dev/null || true
docker-compose up -d

echo ""
echo "===================================="
echo "  SETUP COMPLETE!"
echo "=============================="
echo ""
echo "  GGUF file: ${GGUF_FILE}"
echo "  Server is running at: http://localhost:8089"
echo "  Access your model!"
echo ""
