
ARG baseimage=nvidia/cuda:12.8.1-cudnn-devel-ubuntu22.04

FROM ${baseimage} AS baseimage
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8


ENV TZ="Etc/UTC"

ARG DEBIAN_FRONTEND=noninteractive
# Build arguments
ARG ARG_UID=1000
ARG ARG_GID=1000

RUN <<eot
    set -eux
    apt -qy update
    apt -qy install --no-install-recommends \
        -o APT::Install-Recommends=false \
        -o APT::Install-Suggests=false \
        console-setup tzdata dbus x11-utils x11-xserver-utils libgl1-mesa-glx 
    apt -qy update
    DEBIAN_FRONTEND=noninteractive  apt -qy install --no-install-recommends \
        -o APT::Install-Recommends=false \
        -o APT::Install-Suggests=false \
        libfuse2 kmod fuse libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgtk-3-0 libgbm1 libasound2 xserver-xorg xvfb x11vnc
    mkdir -p /root/.vnc && x11vnc -storepasswd test123 /root/.vnc/passwd
eot

ENV DISPLAY=:99

#########################

FROM baseimage AS final

ADD ./LM-Studio* /data/lms/
ADD ./http-server-config.json /http-server-config.json

RUN <<eot
    set -eux
    chmod ugo+x /data/lms/*.AppImage
    /data/lms/*.AppImage --appimage-extract
eot


ADD ./docker-entrypoint.sh /usr/local/bin/
ADD ./docker-healthcheck.sh /usr/local/bin/

# Ensure the scripts are executable
RUN chmod +x /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-healthcheck.sh
# Setup the healthcheck
HEALTHCHECK --interval=1m --timeout=10s --start-period=1m \
  CMD /bin/bash /usr/local/bin/docker-healthcheck.sh || exit 1


# Run the server
# CMD ["sh", "-c", "tail -f /dev/null"] # For development: keep container open
ENTRYPOINT ["/bin/bash", "/usr/local/bin/docker-entrypoint.sh"]
