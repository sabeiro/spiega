FROM ubuntu:22.04

# Prevent interactive prompts during apt installations
ENV DEBIAN_FRONTEND=noninteractive

# Required to pass Nvidia drivers from host into container
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics

# Install UI, VNC, Hardware tools, AND all required backend computing libraries
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    openbox \
    curl \
    wget \
    ca-certificates \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxtst6 \
    sudo \
    lshw \
    pciutils \
    procps \
    dbus \
    dbus-x11 \
    libgomp1 \
    libvulkan1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libxshmfence1 \
    xdg-utils \
    libomp5 \
    libnuma1 \
    ocl-icd-libopencl1 \
    libgl1 \
    libatomic1 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash lmstudio && \
    echo "lmstudio ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /app

# Copy the AppImage into the container
COPY LM-Studio-0.4.13-1-x64.AppImage /app/lm-studio.AppImage
RUN chmod +x /app/lm-studio.AppImage

# Switch to the non-root user and extract the AppImage
RUN chown -R lmstudio:lmstudio /app
USER lmstudio
RUN /app/lm-studio.AppImage --appimage-extract && \
    rm /app/lm-studio.AppImage

# Copy our startup script
COPY --chown=lmstudio:lmstudio entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create directories for models and config persistence
RUN mkdir -p /home/lmstudio/.cache/lm-studio/models && \
    mkdir -p /home/lmstudio/.config/"LM Studio"

# Expose NoVNC Web UI (8080) and Local Inference Server API (1234)
EXPOSE 8080 1234

ENV DISPLAY=:0
ENV RESOLUTION=1600x900x24

CMD ["/app/entrypoint.sh"]
