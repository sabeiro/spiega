# ========== Dockerfile for Acer Laptop (NVIDIA RTX 5060) ========================
# GPU: NVIDIA GeForce RTX 5060
# RAM: 32GB
# Host: ~/lav/src/ (shared path between host and container)
# Config: ~/lav/src/pi_config/ (mounted to container)
# ====================================================================================

FROM ollama/ollama:latest

# Install dependencies
RUN apt update && apt install -y --no-install-recommends \
    git curl vim wget ca-certificates emacs python3 python3-pip

RUN pip3 install httpx --break-system-packages
#RUN wget https://bootstrap.pypa.io/get-pip.py
#RUN python3 get-pip.py  --break-system-packages
RUN apt clean && rm -rf /var/lib/apt/lists/*
ENV PATH="$PATH:~/.local/bin/"
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Create directory for seamless host↔guest integration
RUN mkdir -p /root/lav/src /root/.pi \
    && chmod -R 755 /root/lav/src /root/.pi

# Symlink home directory for convenience
RUN ln -s /root/lav/src /home/lav/src 2>/dev/null || true
# Install pi-coding-agent
RUN curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard
RUN curl -fsSL https://pi.dev/install.sh |  bash -s -- --no-prompt --no-onboard
RUN curl -fsSL https://opencode.ai/install | bash -s -- --no-prompt --no-onboard
RUN curl -LsSf https://aider.chat/install.sh | bash -s --
RUN curl -fsSL https://unsloth.ai/install.sh | sh
# python -m pip install aider-install
# aider-install

# Environment
ENV PATH="/root/.local/bin:$PATH"
ENV OLLAMA_KEEP_ALIVE=1h
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_VULKAN=1

# Ports
EXPOSE 11434 18789

HEALTHCHECK CMD curl -f http://localhost:11434/api/tags || exit 1

ARG UID=1000
ARG GID=1000
#RUN groupadd -o -g 1000 sabeiro && useradd -o -r -m -u 1000 -g 1000 sabeiro
#RUN addgroup --gid 1000 sabeiro && adduser --uid 1000 --gid 1000 --disabled-password --gecos "" sabeiro
#RUN groupadd -g "${GID}" sabeiro && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" sabeiro
#RUN groupadd -g 1000 sabeiro && useradd --create-home --no-log-init -u 1000 -g 1000 sabeiro
#RUN groupmod -g "${GID}" node && usermod -u "${UID}" -g "${GID}" node
#RUN adduser sabeiro

RUN usermod -l sabeiro ubuntu
RUN usermod -d /home/sabeiro/ sabeiro
RUN usermod -s /bin/bash sabeiro
RUN groupadd sabeiro
RUN usermod -aG ubuntu sabeiro
RUN usermod -aG sabeiro sabeiro

#COPY ./pi_config/ /home/sabeiro/.pi/
#VOLUME /home/sabeiro/lav/src/
#VOLUME /home/sabeiro/Downloads/llm_model/ 
#RUN ln -s /home/sabeiro/Downloads/llm_model/ /home/sabeiro/.ollama 
#RUN chown -R sabeiro:sabeiro /home/sabeiro/
USER sabeiro
WORKDIR /home/sabeiro/

# Start Ollama
#CMD ["ollama", "serve"]
