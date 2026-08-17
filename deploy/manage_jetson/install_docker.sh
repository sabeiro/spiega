sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml

ls /etc/docker/daemon.json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "runtimes": {
    "nvidia": {
      "path": "/usr/bin/nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}

sudo systemctl restart docker
