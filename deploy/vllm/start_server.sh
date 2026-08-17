
#!/bin/bash

# --- CONFIGURATION START ---
MODEL_NAME="Ministral-3-14B-Reasoning-2512-Q4_K_M.gguf" 
MODEL_PATH="/model/$MODEL_NAME" # Must match model location in volumes section
PORT=8000
MAX_TOKENS=4096
# --- CONFIGURATION END ---

echo "Starting vLLM Inference Server..."
echo "Attempting to load model: $MODEL_NAME"

#vllm serve "Qwen/Qwen2.5-1.5B-Instruct"
vllm serve "Qwen/Qwen2.5-Coder-14B-Instruct"

# The main command that starts the high-performance API server
#python3 -m vllm.entrypoints.api_server --model $MODEL_PATH --port $PORT --max-model-len $MAX_TOKENS 

echo "Server stopped or failed to start."
