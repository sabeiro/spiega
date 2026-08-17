#!/usr/bin/env bash
# Install dependencies for 360_to_3d.
#
# Prerequisites (this script installs them):
#   - PyTorch with CUDA support (required). On Jetson: TORCH_INSTALL below. On x86: from pytorch.org.
#   - pip packages from requirements.txt (numpy, opencv, open3d, etc.)
#
# Run from repo root or from 360_to_3d/. Uses system pip (no venv).

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS="${SCRIPT_DIR}/requirements.txt"

# Jetson: PyTorch CUDA wheel. Default: JetPack 6 + Python 3.10 (cp310). Edit for other JP/Python.
TORCH_INSTALL="https://developer.download.nvidia.com/compute/redist/jp/v60/pytorch/torch-2.4.0a0+07cecf4168.nv24.05.14710581-cp310-cp310-linux_aarch64.whl"

echo "=== 360_to_3d dependencies ==="
echo "Prerequisite: PyTorch with CUDA (required for this pipeline)."

# Detect platform
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ]; then
    PLATFORM="jetson"
else
    PLATFORM="x86"
fi

# Jetson: system packages, cuDNN, and CUDA env (PyTorch/TensorRT need libcudnn.so.8)
if [ "$PLATFORM" = "jetson" ]; then
    echo "Jetson detected (aarch64). Installing system packages..."
    sudo apt-get -y update
    sudo apt-get install -y python3-pip libopenblas-dev
    sudo apt-get install -y zlib1g
    sudo apt-get -y install cudnn8-cuda-12
    # cuDNN 8 required by PyTorch wheel / TensorRT (libcudnn.so.8)
    if ! ldconfig -p 2>/dev/null | grep -q libcudnn.so.8; then
        echo "Installing cuDNN 8 (libcudnn.so.8)..."
        sudo apt-get install -y libcudnn8 libcudnn8-dev 2>/dev/null || sudo apt-get install -y libcudnn8 2>/dev/null || true
    fi

    export CUDA_HOME="${CUDA_HOME:-/usr/local/cuda}"
    CUDNN_LIB="/usr/lib/aarch64-linux-gnu"
    export PATH="${CUDA_HOME}/bin:${PATH}"
    export LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${CUDNN_LIB}:${LD_LIBRARY_PATH:-}"
    export CPATH="${CUDA_HOME}/include:${CPATH:-}"
    if [ "$CUDA_HOME" = "/usr/local/cuda" ]; then
        echo "Set CUDA_HOME and LD_LIBRARY_PATH (incl. cuDNN) for this run. For persistence add to ~/.profile:"
        echo "  export CUDA_HOME=/usr/local/cuda"
        echo "  export PATH=\$CUDA_HOME/bin:\$PATH"
        echo "  export LD_LIBRARY_PATH=\$CUDA_HOME/lib64:/usr/lib/aarch64-linux-gnu:\$LD_LIBRARY_PATH"
    fi
fi

# Upgrade pip
python3 -m pip install --upgrade pip

# Remove broken/corrupted torch dist-info (fixes "Ignoring invalid distribution -orch")
USER_SITE=$(python3 -c "import site; print(site.USER_SITE)")
for d in "$USER_SITE"/-orch* "$USER_SITE"/~orch* "$USER_SITE"/_torch*; do
    if [ -d "$d" ] || [ -e "$d" ]; then
        echo "Removing broken pip metadata: $d"
        rm -rf "$d"
    fi
done 2>/dev/null || true

# Jetson: install CUDA wheel FIRST so requirements don't replace it (timm/ultralytics depend on torch)
if [ "$PLATFORM" = "jetson" ] && [ -n "${TORCH_INSTALL}" ]; then
    echo "Installing PyTorch from Jetson CUDA wheel (shared with camera/ for ONNX+TensorRT)..."
    python3 -m pip install --user --no-cache-dir "$TORCH_INSTALL"
    TORCH_CONSTRAINT=$(mktemp)
    trap "rm -f '$TORCH_CONSTRAINT'" EXIT
    TORCH_VER=$(python3 -c "import torch; print(torch.__version__)")
    echo "torch==${TORCH_VER}" > "$TORCH_CONSTRAINT"
fi

# x86: install PyTorch with CUDA before requirements
if [ "$PLATFORM" = "x86" ]; then
    echo "Installing PyTorch with CUDA (x86)..."
    CUDA="${TORCH_CUDA:-cu121}"
    python3 -m pip install --user torch torchvision --index-url "https://download.pytorch.org/whl/${CUDA}"
fi

# Requirements (on Jetson we use -c to keep the Jetson torch wheel; no second install)
echo "Installing pip requirements from requirements.txt (--user → ~/.local)..."
if [ "$PLATFORM" = "jetson" ] && [ -f "${TORCH_CONSTRAINT:-}" ]; then
    python3 -m pip install --user -r "$REQUIREMENTS" -c "$TORCH_CONSTRAINT"
else
    python3 -m pip install --user -r "$REQUIREMENTS"
fi

echo "Verifying PyTorch CUDA (required)..."
if ! python3 -c "import torch; exit(0 if torch.cuda.is_available() else 1)"; then
    echo "ERROR: PyTorch CUDA check failed (import error or torch.cuda.is_available() is False)."
    if [ "$PLATFORM" = "jetson" ]; then
        echo "  If you see 'libcudnn.so.8: cannot open shared object file':"
        echo "    export LD_LIBRARY_PATH=/usr/lib/aarch64-linux-gnu:\$LD_LIBRARY_PATH"
        echo "    sudo apt install libcudnn8   # then re-run this script or source ~/.profile"
        echo "  Else reinstall the Jetson wheel: python3 -m pip install --user --force-reinstall \"${TORCH_INSTALL}\""
    fi
    exit 1
fi
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# Optional: pycuda (same as camera/ — for TensorRT/pose or shared use)
if [ "$PLATFORM" = "jetson" ] && [ -d "${CUDA_HOME:-/usr/local/cuda}" ]; then
    echo ""
    echo "Optional: pycuda (used by camera/ for pose; 360_to_3d uses PyTorch only):"
    echo "  python3 -m pip install --user pycuda --no-cache-dir"
fi

# Optional: CGAL Poisson (stage 5.4 fallback)
if command -v cmake &>/dev/null; then
    echo ""
    echo "=== Optional: CGAL Poisson (stage 5.4) ==="
    echo "  CLI:  sudo apt install -y libcgal-dev libeigen3-dev"
    echo "        cd ${SCRIPT_DIR}/ext/cgal_poisson && cmake -B build && cmake --build build"
    echo "  Cython (no temp PLY/OFF): same deps, then:"
    echo "        pip install --user cython numpy"
    echo "        cd ${SCRIPT_DIR}/ext/cgal_poisson && pip install --user -e ."
    echo "  On aarch64 if Cython build fails, set: export CXX=aarch64-linux-gnu-g++"
fi

# PYTHONPATH for ~/.local
PYVER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo ""
echo "=== PYTHONPATH for ~/.local ==="
echo "Add this to your ~/.profile (or ~/.bashrc) so Python finds packages in ~/.local:"
echo ""
echo "  export PYTHONPATH=\"\${HOME}/.local/lib/python${PYVER}/site-packages\${PYTHONPATH:+:\$PYTHONPATH}\""
echo ""
echo "Then run: source ~/.profile   (or open a new shell)."
echo ""
echo "Done."
