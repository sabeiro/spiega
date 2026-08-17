#!/bin/bash
# Get GGUF Models Without HF Token Requirements
# Checks for token, then uses direct links

set -euo pipefail

MODELS=(
    "llama-3.1-8b-instruct-q4_K_M.gguf"
    "llama-3.1-70b-instruct-q4_K_M.gguf"
    "llama-3.2-1b-instruct-q4_K_M.gguf"
    "llama-3.2-3b-instruct-q4_K_M.gguf"
    "llama-3.2-11b-vision-instruct-q4_K_M.gguf"
    "llama-3.3-70b-instruct-q4_K_M.gguf"
    "mixtral-8x7b-v0.1-q4_K_M.gguf"
    "mistral-7b-v0.1-q4_K_M.gguf"
    "mistral-7b-v0.2-q4_K_M.gguf"
    "gemma-2-9b-it-q4_K_M.gguf"
    "phi-3-mini-4k-instruct-q4_K_M.gguf"
    "phi-3.5-mini-instruct-q4_K_M.gguf"
    "qwen2.5-7b-instruct-q4_K_M.gguf"
    "gpt2-onnx-q4_K_M.gguf"
    "gptj-6b-q4_K_M.gguf"
    "gpt4_all-12b-q4_K_M.gguf"
)

HF_TOKEN="${HUGGINGFACE_TOKEN:-}"
OUTPUT_DIR="${HOME}/models/gguf" || OUTPUT_DIR="./models/gguf"

check_download() {
    local model="$1"
    local desc="$2"
    
    echo "=== ${desc} ==="
    
    # Check file exists
    if [[ -f "${OUTPUT_DIR}/${model}" ]]; then
        echo "✅ Already downloaded: ${model}"
        ls -lh "${OUTPUT_DIR}/${model}" 2>/dev/null || echo "   File not found"
        return
    fi
    
    echo "⚠️  Not found, trying direct download..."
    
    # Try various direct download URLs (no HF token)
    for url in
        "https://huggingface.co/jartine/${model%/resolve/main/${model}"
        "https://huggingface.co/microsoft/${model%/resolve/main/${model}"
        "https://huggingface.co/microsoft/LLaMA-3.1-8B-Instructions/resolve/main/LLaMA-3.1-8B-Instruct-q4_K_M.gguf"
        "https://huggingface.co/microsoft/LLaMA-3.2-1B-Instruct-GGUF/resolve/main/llama-3.2-1b-instruct-q4_K_M.gguf"
        "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4_K_M.gguf"
        "https://huggingface.co/mistralai/Mistral-7B-v0.3-GGUF/resolve/main/mistral-7b-v0.3-q4_K_M.gguf"
    do
        echo "   → ${url}"
        if curl -sS -L -o "${OUTPUT_DIR}/${model}" "${url}" 2>/dev/null; then
            echo "   ✅ Success!"
            ls -lh "${OUTPUT_DIR}/${model}"
            return 0
        fi
    done
    
    echo "   ⚠️  Not available directly (may need HF token)" >&2
    echo "   🌐 Try: ${url}" >&2
    return 1
}

check_and_download_model() {
    check_download "$1" "$2"
}

# Main loop
if [[ -z "${HF_TOKEN:-}" ]]; then
    echo "No HF_TOKEN available, using direct download URLs"
else
    echo "HF_TOKEN present, checking huggingface.co..."
fi

# Get first model that's available
for model in "${MODELS[@]}"; do
    desc=$(echo "$model" | sed 's/.*-//' | xargs)
    check_download "${model}" "$desc" || true
done

# Summary
echo ""
echo "=== Summary ==="
echo "Models directory: ${OUTPUT_DIR}"
find "${OUTPUT_DIR}" -name "*.gguf" -exec ls -lh {} \; 2>/dev/null || true

# List all available models
echo ""
echo "✅ Ready to use with Ollama:"
echo "   ollama serve --model ${OUTPUT_DIR}/gguf/*.gguf"
echo "   ollama create mymodel -f ${OUTPUT_DIR}/gguf/*.gguf"
echo "   ollama run mymodel"
