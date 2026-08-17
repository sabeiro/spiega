#FROM python:3.11-slim
FROM ubuntu:latest
RUN curl -fsSL https://unsloth.ai/install.sh | bash -s -- --no-prompt
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH="/root/.local/lib:$PYTHONPATH"
ENV UNSLOTH_STUDIO_HOME=/home/sabeiro/.unsloth/studio
RUN curl -fsSL https://unsloth.ai/install.sh | bash -s -- --no-prompt

# OpenCV headless still pulls in GUI/runtime libs at import; provide them so cv2 imports
RUN apt-get update 
RUN apt-get install -y --no-install-recommends libxcb1 libxcb-shm0 libxcb-xfixes0 libgl1 libglib2.0-0 
RUN apt install -y curl python3-pip bash git python3
RUN apt install -y build-essential cmake libcurl4-openssl-dev wget
RUN apt install -y libopenblas-dev
RUN apt install -y vulkan-tools libvulkan-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages
# RUN CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
# COPY server.py agent.py vision.py run.sh entrypoint.sh .
# COPY static/ ./static/
# RUN chmod +x run.sh
WORKDIR /app
# EXPOSE 8002 8001

