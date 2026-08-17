#!/bin/bash
# =============================================================================
# OpenCV with CUDA DNN Build Script for Jetson Orin
# =============================================================================
# This script builds OpenCV from source with CUDA support for DNN inference.
# Run this on the Jetson device.
#
# Requirements:
# - JetPack installed (includes CUDA, cuDNN, TensorRT)
# - At least 8GB free disk space
# - Build takes ~2-3 hours on Orin
# =============================================================================

set -e

# Set CUDA paths first
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export CPATH=$CUDA_HOME/include:$CPATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Add to ~/.bashrc to make permanent
echo 'export CUDA_HOME=/usr/local/cuda' >> ~/.bashrc
echo 'export PATH=$CUDA_HOME/bin:$PATH' >> ~/.bashrc
echo 'export CPATH=$CUDA_HOME/include:$CPATH' >> ~/.bashrc

# Then install
pip install pycuda

# Using 4.10.0 to avoid __half comparison bug in 4.8.0
OPENCV_VERSION="4.10.0"
INSTALL_PREFIX="/usr/local"
BUILD_DIR="$HOME/opencv_build"

echo "=== Building OpenCV ${OPENCV_VERSION} with CUDA for Jetson Orin ==="

# Install dependencies
echo "Installing build dependencies..."
sudo apt-get update
sudo apt-get install -y \
    build-essential cmake git pkg-config \
    libjpeg-dev libpng-dev libtiff-dev \
    libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev \
    libgtk-3-dev libatlas-base-dev gfortran \
    python3-dev python3-numpy \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

# Create build directory
mkdir -p ${BUILD_DIR}
cd ${BUILD_DIR}

# Remove old build if exists (in case switching versions)
if [ -d "opencv/build" ]; then
    echo "Removing old build directory..."
    rm -rf opencv/build
fi

# Clone OpenCV and contrib
if [ ! -d "opencv" ] || [ "$1" == "--clean" ]; then
    echo "Cloning OpenCV..."
    rm -rf opencv
    git clone --depth 1 --branch ${OPENCV_VERSION} https://github.com/opencv/opencv.git
fi

if [ ! -d "opencv_contrib" ] || [ "$1" == "--clean" ]; then
    echo "Cloning OpenCV contrib..."
    rm -rf opencv_contrib
    git clone --depth 1 --branch ${OPENCV_VERSION} https://github.com/opencv/opencv_contrib.git
fi

# Create build directory
mkdir -p opencv/build
cd opencv/build

# Detect CUDA compute capability for Jetson Orin (SM 8.7)
# Orin Nano/NX: 8.7, AGX Orin: 8.7
CUDA_ARCH="8.7"

echo "Configuring OpenCV with CUDA..."
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} \
    -D OPENCV_EXTRA_MODULES_PATH=${BUILD_DIR}/opencv_contrib/modules \
    -D WITH_CUDA=ON \
    -D WITH_CUDNN=ON \
    -D OPENCV_DNN_CUDA=ON \
    -D ENABLE_FAST_MATH=ON \
    -D CUDA_FAST_MATH=ON \
    -D CUDA_ARCH_BIN=${CUDA_ARCH} \
    -D WITH_CUBLAS=ON \
    -D WITH_LIBV4L=ON \
    -D WITH_GSTREAMER=ON \
    -D WITH_OPENGL=ON \
    -D WITH_QT=OFF \
    -D BUILD_opencv_python3=ON \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    ..

# Build with all available cores
echo "Building OpenCV (this will take a while)..."
make -j$(nproc)

# Install
echo "Installing OpenCV..."
sudo make install
sudo ldconfig

echo ""
echo "=== OpenCV ${OPENCV_VERSION} with CUDA installed successfully! ==="
echo ""
echo "Verify installation with:"
echo "  pkg-config --modversion opencv4"
echo "  python3 -c \"import cv2; print(cv2.getBuildInformation())\" | grep -A5 CUDA"
echo ""
echo "Now rebuild your OpenFrameworks project:"
echo "  cd /home/gmare/mount/jetson/cv/of_yolo_example"
echo "  make clean && make"
echo ""

