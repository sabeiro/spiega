#!/bin/bash

DOCKER_SOCKET=/var/run/docker.sock
DOCKER_GROUP=docker
USER=sabeiro

if [ -S ${DOCKER_SOCKET} ]; then
    DOCKER_GID=$(stat -c '%g' ${DOCKER_SOCKET})

    sudo addgroup --gid ${DOCKER_GID} ${DOCKER_GROUP}
    sudo usermod --append --groups ${DOCKER_GROUP} ${USER}
	newgrp ${DOCKER_GROUP}
	newgrp $(id -gn)
fi
sg ${DOCKER_GROUP} -c "bash"

exec "$@"
