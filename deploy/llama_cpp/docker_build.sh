#docker build -t local/llama.cpp:light-cuda --target light -f Dockerfile_cuda .
docker run --gpus all --cap-add=IPC_LOCK ghcr.io/ggml-org/llama.cpp:server-cuda \
       --model qwen3-coder-30b-a3b.gguf --n-cpu-moe 35 --load-mode mmap --load-mode mlock \
       --cache-type-v q4_0 --cache-type-k q4_0
