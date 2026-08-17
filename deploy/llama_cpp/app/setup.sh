#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_DIR="$(cd "${SCRIPT_DIR}"/.. && pwd)"

echo "===================================="
echo "  LLAMA.CPP SETUP WIZARD"
echo "===================================="
echo ""

# Check host requirements
check_requirements() {
    echo "=== Checking host requirements ==="
    
    # Check Docker
    if ! docker --version >/dev/null 2>&1; then
        echo "ERROR: Docker not found. Please install Docker first."
        exit 1
    fi
    echo "✓ Docker installed"
    
    # Check NVIDIA
    if ! nvidia-smi >/dev/null 2>&1; then
        echo "ERROR: NVIDIA drivers not found. Please ensure GPU is available."
        exit 1
    fi
    echo "✓ NVIDIA drivers installed"
    
    return 0
}

# Create host models directory
setup_directories() {
    echo ""
    echo "=== Setting up directories ==="
    
    MODELS_DIR="${HOME}/llm_model/models"
    CACHE_DIR="${HOME}/llm_cache"
    
    mkdir -p "${MODELS_DIR}"
    mkdir -p "${CACHE_DIR}"
    
    echo "✓ Models directory: ${MODELS_DIR}"
    echo "✓ Cache directory: ${CACHE_DIR}"
}

# Build docker image
build_image() {
    echo ""
    echo "=== Building Docker image ==="
    cd "${SCRIPT_DIR}"
    docker build -t llama_cpp:latest -f Dockerfile .
    echo "✓ Docker image built: llama_cpp:latest"
}

# Download model
download_model() {
    echo ""
    echo "=== Downloading model ==="
    echo ""
    echo "Available models:"
    echo "  1. Meta-Llama-3.1-8B-Instruct (4.7GB) - Recommended for chat"
    echo "  2. Qwen3-4B-Thinking (4GB) - Lightweight option"
    echo "  3. Mistral-7B-Instruct-v0.3 (5GB)"
    echo "  4. Gemma-4-12B-It (15GB) - Large model"
    echo ""
    
    read -p "Select model (1-4, or enter to skip manual download): " choice
    
    case "$choice" in
        "1")
            echo "Downloading: Meta-Llama-3.1-8B-Instruct (4.7GB)..."
            MODELS_DIR="${HOME}/llm_model/models"
            wget --show-progress -O "${MODELS_DIR}/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" \
                "https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
            ;;
        "2")
            echo "Downloading: Qwen3-4B-Thinking (4GB)..."
            MODELS_DIR="${HOME}/llm_model/models"
            wget --show-progress -O "${MODELS_DIR}/Qwen3-4B-Thinking.Q4_K_M.gguf" \
                "https://huggingface.co/Qwen/Qwen3-4B-Thinking/resolve/main/Qwen3-4B-Thinking.Q4_K_M.gguf"
            ;;
        "3")
            echo "Downloading: Mistral-7B-Instruct-v0.3 (5GB)..."
            MODELS_DIR="${HOME}/llm_model/models"
            wget --show-progress -O "${MODELS_DIR}/Mistral-7B-Instruct-v0.3-Q5_K_M.gguf" \
                "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/Mistral-7B-Instruct-v0.3-Q5_K_M.gguf"
            ;;
        "4")
            echo "Downloading: Gemma-4-12B-It (15GB)..."
            MODELS_DIR="${HOME}/llm_model/models"
            wget --show-progress -O "${MODELS_DIR}/gemma-4-12b-it-Q5_K_M.gguf" \
                "https://huggingface.co/ggml-org/gemma-4-12b-it-GGUF/resolve/main/gemma-4-12b-it-Q5_K_M.gguf"
            ;;
        "")
            echo "Skipping model download (you may add later)..."
            ;;
        *)
            echo "Invalid choice. Using Meta-Llama-3.1-8B-Instruct..."
            MODELS_DIR="${HOME}/llm_model/models"
            wget --show-progress -O "${MODELS_DIR}/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" \
                "https://huggingface.co/mradermacher/Meta-Llama-3.1-8B-Instruct-i1-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
            ;;
    esac
}

# Start container
start_container() {
    echo ""
    echo "=== Starting container ==="
    cd "${SCRIPT_DIR}"
    
    # Stop and remove old containers
    docker compose down --remove-orphans 2>/dev/null || true
    
    # Start with GPU
    docker compose up -d
    
    echo "✓ Container started"
}

# Check container is ready
wait_ready() {
    echo ""
    echo "=== Checking container status ==="
    
    sleep 5
    
    if docker compose ps | grep -q llama_cpp; then
        echo "✓ Container is running"
    else
        echo "WARNING: Container may not be running yet"
    fi
}

# Run all steps
main() {
    echo ""
    echo "Starting setup wizard..."
    echo ""
    
    check_requirements
    setup_directories
    build_image
    download_model
    start_container
    wait_ready
    
    echo ""
    echo "===================================="
    echo "  SETUP COMPLETE!"
    echo "===================================="
    echo ""
    echo "Access llama.cpp at: http://localhost:8089"
    echo ""
    echo "Your models are in: ${HOME}/llm_model/models"
    echo ""
    echo "Commands:"
    echo "  - View logs: docker logs llama_cpp"
    echo "  - Stop: docker compose down"
    echo "  - Restart: docker compose down && docker compose up -d"
    echo "  - Access shell: docker exec -it llama_cpp bash"
    echo "========================================"
}

main "$@"
