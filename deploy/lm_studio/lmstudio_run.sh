
#curl -fsSL https://lmstudio.ai/install.sh | bash
export PATH="/home/sabeiro/.lmstudio/bin:$PATH"
lms bootstrap
lms daemon up
lms get qwen/qwen3-4b-2507
lms get qwen3-coder-30b-a3b.gguf
