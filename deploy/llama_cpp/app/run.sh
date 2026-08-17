#!/bin/bash
cd /app/llama.cpp/bin/
#./llama-server --model /model/Qwen3.5-9B-Q4_0.gguf
llama-server --model /model/qwen3-coder-30b-a3b.gguf --n-cpu-moe 35 --load-mode mmap --load-mode mlock --cache-type-v q4_0 --cache-type-k q4_0
