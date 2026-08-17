
from llama_cpp import Llama
import os

llm = Llama.from_pretrained(
    repo_id="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
    local_dir=os.environ['HOME'] + "/Downloads/llm_model/",
    filename="Meta-Llama-3.1-8B-Instruct-IQ2_M.gguf",
)


#Qwen/Qwen2.5-Coder-14B-Instruct-GGUF
