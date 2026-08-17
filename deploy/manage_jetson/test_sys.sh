nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits
watch -n 1 nvidia-smi
nvidia-smi dmon -s mu

# Profile Ollama with Nsight Systems
nsys profile --trace=cuda,nvtx --output=ollama-profile \
  ollama run llama2:13b "Explain machine learning"

# Analyze CUDA kernels
ncu --set full --target-processes all \
  ollama run llama2:13b "Test prompt"
