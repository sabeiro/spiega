#!/usr/bin/env bash
# Install dependencies for Jetson (aarch64). Use Python 3.10 on JetPack 6.x.
# Do NOT install PyTorch from PyPI (cu126) — those wheels lack Jetson Orin (SM 8.7) kernels.

set -e

# JetPack 6.1. Set INSTALL_DOCKER=1, INSTALL_CUSPARSELT=1, INSTALL_SYSTEM_DEPS=1 as needed.
# BUILD_TORCHVISION=1: build torchvision 0.20 from source (required for timm/ultralytics; takes ~15–30 min).
# BUILD_TORCHAUDIO=1: build torchaudio 2.5 from source (pairs with torch 2.5).
INSTALL_DOCKER=0
INSTALL_CUSPARSELT=0
INSTALL_SYSTEM_DEPS=0
BUILD_TORCHVISION=1
BUILD_TORCHAUDIO=1

# --- Docker + NVIDIA container runtime (set SKIP_DOCKER=1 to skip if already configured) ---
if [ "${INSTALL_DOCKER:-0}" = "1" ]; then
  sudo apt install -y nvidia-container curl
  curl -fsSL https://get.docker.com | sh && sudo systemctl --now enable docker
  sudo nvidia-ctk runtime configure --runtime=docker
  sudo systemctl restart docker
  sudo apt install ripgrep cmake libvterm-dev
  sudo usermod -aG docker "$USER" || true
  echo "Log out and back in (or run: newgrp docker) for docker group to take effect."
fi

#sudo snap install go --classic
#go install github.com/mark3labs/mcphost@latest


# --- System deps (needed for some Python packages) ---
if [ "${INSTALL_SYSTEM_DEPS:-0}" = "1" ]; then
sudo apt-get install -y python3-pip libopenblas-dev \
  libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install -y --no-install-recommends libjpeg-dev libpng-dev libtiff-dev cmake ninja-build 2>/dev/null || true
sudo apt-get install mesa-vulkan-drivers #ollama acceleration
fi
# --- cuSparseLT: required for JetPack 6.1 PyTorch 2.5 wheel. Not needed for 6.0 torch 2.3. ---
if [ "${INSTALL_CUSPARSELT:-0}" = "1" ]; then
  if [ ! -f /usr/local/cuda/lib64/libcusparseLt.so ]; then
    echo "Installing cuSparseLT for JetPack 6.1..."
    wget -q https://developer.download.nvidia.com/compute/cusparselt/redist/libcusparse_lt/linux-aarch64/libcusparse_lt-linux-aarch64-0.8.1.1_cuda12-archive.tar.xz -O /tmp/cusparselt.tar.xz
    tar xf /tmp/cusparselt.tar.xz -C /tmp
    sudo cp -a /tmp/libcusparse_lt-linux-aarch64-0.8.1.1_cuda12-archive/include/* /usr/local/cuda/include/
    sudo cp -a /tmp/libcusparse_lt-linux-aarch64-0.8.1.1_cuda12-archive/lib/* /usr/local/cuda/lib64/
    sudo ldconfig
    rm -rf /tmp/cusparselt.tar.xz /tmp/libcusparse_lt-linux-aarch64-0.8.1.1_cuda12-archive
  fi
fi

# --- PyTorch stack: one matching wheel set only (no mix with PyPI torch/torchvision). ---
# numpy<2 for Jetson wheels. OpenCV 4.12+ requires numpy>=2 → pin OpenCV <4.12.
python3 -m pip install --upgrade pip
python3 -m pip install 'numpy<2'
python3 -m pip install 'opencv-python-headless>=4.8.0,<4.12'
python3 -m pip install 'opencv-python>=4.8.0,<4.12' 2>/dev/null || true  # if you use non-headless opencv

# Fix point: NVIDIA v61 torch 2.5.0 wheel only (CUDA works). Do not replace with jp6/cu126 or PyPI — those can install +cpu.
# Wheel is saved under WHEELS_DIR so we don't re-download on next run.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
WHEELS_DIR="${WHEELS_DIR:-$SCRIPT_DIR/wheels}"
TORCH_WHEEL="torch-2.5.0-cp310-cp310-linux_aarch64.whl"
TORCH_URL="https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl"

NEED_TORCH_INSTALL=1
TORCH_VER=$(python3 -c "import torch; print(torch.__version__)" 2>/dev/null || echo "")
if [ -n "$TORCH_VER" ] && [[ "$TORCH_VER" == 2.5* ]] && [[ "$TORCH_VER" != *"+cpu"* ]]; then
  echo "PyTorch $TORCH_VER already installed (v61, CUDA). Skipping."
  NEED_TORCH_INSTALL=0
fi

if [ "$NEED_TORCH_INSTALL" = "1" ]; then
  python3 -m pip uninstall -y torch torchvision torchaudio 2>/dev/null || true
  mkdir -p "$WHEELS_DIR"
  if [ ! -f "$WHEELS_DIR/$TORCH_WHEEL" ]; then
    echo "Downloading PyTorch 2.5.0 wheel to $WHEELS_DIR/..."
    wget -q -O "$WHEELS_DIR/$TORCH_WHEEL" "$TORCH_URL"
  else
    echo "Using cached wheel $WHEELS_DIR/$TORCH_WHEEL"
  fi
  echo "Installing PyTorch 2.5.0 for JetPack 6.1 (v61, CUDA)..."
  python3 -m pip install --no-cache-dir "$WHEELS_DIR/$TORCH_WHEEL"
fi

# --- TorchVision from source (ABI-compatible with v61 torch 2.5; no prebuilt wheel for JP 6.1) ---
if [ "${BUILD_TORCHVISION:-0}" = "1" ]; then
  HAVE_VISION=0
  if python3 -c "import torchvision; exit(0 if tuple(map(int, torchvision.__version__.split('.')[:2])) >= (0, 20) else 1)" 2>/dev/null; then
    HAVE_VISION=1
  fi
  if [ "$HAVE_VISION" = "0" ]; then
    echo "Building torchvision 0.20 from source (compatible with torch 2.5; this may take 15–30 min)..."
    BUILD_DIR=$(mktemp -d)
    git clone --depth 1 --branch v0.20.0 https://github.com/pytorch/vision.git "$BUILD_DIR/vision"
    (
      cd "$BUILD_DIR/vision"
      python3 -m pip install wheel  # needed for build
      export MAX_JOBS=1
      export TORCH_CUDA_ARCH_LIST="8.7"
      python3 -m pip install --no-build-isolation -v .
    )
    rm -rf "$BUILD_DIR"
  else
    echo "torchvision 0.20+ already installed. Skipping build."
  fi
fi

# --- TorchAudio from source (ABI-compatible with v61 torch 2.5; no prebuilt wheel for JP 6.1) ---
if [ "${BUILD_TORCHAUDIO:-0}" = "1" ]; then
  HAVE_AUDIO=0
  if python3 -c "import torchaudio; v=torchaudio.__version__; exit(0 if (v.startswith('2.5.')) else 1)" 2>/dev/null; then
    HAVE_AUDIO=1
  fi
  if [ "$HAVE_AUDIO" = "0" ]; then
    echo "Building torchaudio 2.5.0 from source (compatible with torch 2.5; may take 10–20 min)..."
    BUILD_DIR=$(mktemp -d)
    git clone --depth 1 --branch v2.5.0 https://github.com/pytorch/audio.git "$BUILD_DIR/audio"
    (
      cd "$BUILD_DIR/audio"
      python3 -m pip install wheel
      export MAX_JOBS=1
      export TORCH_CUDA_ARCH_LIST="8.7"
      python3 -m pip install --no-build-isolation -v .
    )
    rm -rf "$BUILD_DIR"
  else
    echo "torchaudio 2.5.x already installed. Skipping build."
  fi
fi

# --- Verify CUDA ---
python3 test_cuda.py
