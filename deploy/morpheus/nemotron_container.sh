sudo docker run -it --rm --pull always --runtime=nvidia \
-p ${VLLM_PORT:-8000}:${VLLM_PORT:-8000} \
-e HF_TOKEN=$HF_TOKEN -e VLLM_PORT=${VLLM_PORT:-8000} \
-e VLLM_GPU_MEMORY_UTILIZATION=${VLLM_GPU_MEMORY_UTILIZATION:-0.8} \
-e VLLM_USE_FLASHINFER_MOE_FP4=1 -e VLLM_FLASHINFER_MOE_BACKEND=throughput \
-v $HOME/.cache/huggingface:/root/.cache/huggingface \
nvcr.io/nvidia/vllm:25.12.post1-py3 \
bash -c "wget -q -O /tmp/nano_v3_reasoning_parser.py --header=\"Authorization: Bearer \$HF_TOKEN\" \
https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4/resolve/main/nano_v3_reasoning_parser.py && \
vllm serve nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 \
--port \$VLLM_PORT --gpu-memory-utilization \$VLLM_GPU_MEMORY_UTILIZATION \
--trust-remote-code --enable-auto-tool-choice --tool-call-parser qwen3_coder \
--reasoning-parser-plugin /tmp/nano_v3_reasoning_parser.py --reasoning-parser nano_v3 --kv-cache-dtype fp8"

