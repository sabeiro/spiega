# LLama.cpp Docker - Simplified for local use
FROM debian:bookworm

RUN apt-get update && apt-get install -y \
    git \
    libcurl4-openssl-dev \
    build-essential \
    python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy compiled llama-cpp-python and config
COPY --chown=ubuntu:root llama-cpp-server /app/llama-cpp-server
COPY --chown=ubuntu:root run.sh /app/run.sh
COPY --chown=ubuntu:root models/volumes/dev/models.yml /app/models.yml

# Set permissions
RUN chmod +x /app/run.sh

# Default user
USER ubuntu

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

ENTRYPOINT ["./run.sh"]
