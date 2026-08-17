import os, sys, re, json
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from llama_cpp import Llama

#sudo apt-get install libblas-dev liblapack-dev gfortran libopenblas-dev
#CMAKE_ARGS="-DGGML_CUDA=on -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python --break-system-packages

baseDir = os.environ['HOME'] + '/lav/src/'
modDir = os.environ['HOME'] + '/Downloads/llm_model/'
model_id = "Qwen3-4B-Instruct-2507-Q3_K_L.gguf"
llm = Llama(model_path=modDir + model_id,n_gpu_layers=-1,seed=1337,n_ctx=2048)
output = llm("Q: 2+2? A: ",max_tokens=32,stop=["Q:", "\n"],echo=True)
print(output)




SERVER_PATH = "server.py"

@pytest.mark.asyncio
async def test_mcp_server_connection():
    """Connect to an MCP server and verify the tools"""
    exit_stack = AsyncExitStack()
    server_params = StdioServerParameters(command="python3", args=[SERVER_PATH], env=None)
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))
    await session.initialize()
    response = await session.list_tools()
    tools = response.tools
    tool_names = [tool.name for tool in tools]
    tool_descriptions = [tool.description for tool in tools]
    print("\nYour server has the following tools:")
    for tool_name, tool_description in zip(tool_names, tool_descriptions):
        print(f"{tool_name}: {tool_description}")
    await exit_stack.aclose()
