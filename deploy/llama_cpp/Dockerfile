FROM python:slim
#FROM ghcr.io/abetlen/llama-cpp-python:latest

RUN apt-get update
RUN apt update
RUN apt install -y curl python3-pip bash git  
RUN apt install -y build-essential cmake libcurl4-openssl-dev wget
RUN apt install -y libopenblas-dev 
RUN apt install -y vulkan-tools libvulkan-dev
#RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
#RUN dpkg -i cuda-keyring_1.1-1_all.deb

RUN adduser --disabled-password --gecos '' ubuntu || true

COPY ./app /app
RUN chmod +x  /app/run.sh
WORKDIR /app

RUN git clone https://github.com/ggerganov/llama.cpp.git
RUN cd /app/llama.cpp/
WORKDIR /app/llama.cpp/
RUN cmake . -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS # -DGGML_VULKAN=ON # -DGGML_CUDA=ON 
RUN make GGML_CUDA=1 && make install && make clean
RUN  rm -rf /var/lib/apt/lists/*
WORKDIR /app/
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD cat /app/run.sh

#ENTRYPOINT ["/app/run.sh"]


#RUN export PATH=$PATH:/app/llama.cpp/bin/
#RUN curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install | sh -s -- --daemon
#RUN nix profile install nixpkgs#llama-cpp
#RUN  wget https://huggingface.co/afrideva/Tiny-Vicuna-1B-GGUF/resolve/main/tiny-vicuna-1b.q5_k_m.gguf
#RUN CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS" pip install -r requirements.txt
#RUN curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install | sh -s -- --no-daemon

#EXPOSE 8080
