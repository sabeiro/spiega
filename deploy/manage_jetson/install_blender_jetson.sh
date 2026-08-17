#!/bin/bash
# =============================================================================
# Blender 5.0 Installation Script for NVIDIA Jetson (ARM64/aarch64)
# =============================================================================
# Installs Blender 5.0 from official ARM64 builds.
# Released: November 18, 2025
#
# Usage: ./install_blender_jetson.sh
# =============================================================================

set -e

BLENDER_VERSION="5.0.0"  # Blender 5.0 stable release
INSTALL_DIR="/opt/blender"
DOWNLOAD_DIR="/tmp/blender_install"

echo "=============================================="
echo "Blender Installation for NVIDIA Jetson"
echo "=============================================="
echo ""

# Check architecture
ARCH=$(uname -m)
if [ "$ARCH" != "aarch64" ]; then
    echo "Warning: This script is designed for ARM64 (aarch64) Jetson devices"
    echo "Detected architecture: $ARCH"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if Blender is already installed
if command -v blender &> /dev/null; then
    CURRENT_VERSION=$(blender --version | head -1)
    echo "Blender is already installed: $CURRENT_VERSION"
    read -p "Do you want to reinstall/upgrade? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Create directories
mkdir -p "$DOWNLOAD_DIR"
cd "$DOWNLOAD_DIR"

echo ""
echo "=== Attempting to download official ARM64 build ==="
echo ""

# Try to download official ARM64 build
# Blender 5.0 provides ARM64 builds
BLENDER_MAJOR="${BLENDER_VERSION%.*}"  # e.g., "5.0"
BLENDER_URL="https://download.blender.org/release/Blender${BLENDER_MAJOR}/blender-${BLENDER_VERSION}-linux-arm64.tar.xz"
BLENDER_FILENAME="blender-${BLENDER_VERSION}-linux-arm64.tar.xz"

# Alternative mirror URLs
BLENDER_MIRROR_URL="https://mirrors.dotsrc.org/blender/release/Blender${BLENDER_MAJOR}/blender-${BLENDER_VERSION}-linux-arm64.tar.xz"

echo "Downloading Blender ${BLENDER_VERSION} for ARM64..."
echo "URL: $BLENDER_URL"

# Try main URL first, then mirror
if wget --progress=bar:force "$BLENDER_URL" -O "$BLENDER_FILENAME" 2>&1; then
    echo "Downloaded from main server"
elif wget --progress=bar:force "$BLENDER_MIRROR_URL" -O "$BLENDER_FILENAME" 2>&1; then
    echo "Downloaded from mirror"
elif wget --progress=bar:force "https://ftp.nluug.nl/pub/graphics/blender/release/Blender${BLENDER_MAJOR}/blender-${BLENDER_VERSION}-linux-arm64.tar.xz" -O "$BLENDER_FILENAME" 2>&1; then
    echo "Downloaded from NL mirror"
fi

if [ -f "$BLENDER_FILENAME" ] && [ -s "$BLENDER_FILENAME" ]; then
    echo "Download successful!"
    
    echo ""
    echo "=== Extracting Blender ==="
    tar -xf "$BLENDER_FILENAME"
    
    # Find extracted directory
    BLENDER_DIR=$(ls -d blender-*-linux-arm64 2>/dev/null | head -1)
    
    if [ -z "$BLENDER_DIR" ]; then
        echo "Error: Could not find extracted Blender directory"
        exit 1
    fi
    
    echo ""
    echo "=== Installing to $INSTALL_DIR ==="
    sudo rm -rf "$INSTALL_DIR"
    sudo mv "$BLENDER_DIR" "$INSTALL_DIR"
    
    # Create symlink
    sudo ln -sf "$INSTALL_DIR/blender" /usr/local/bin/blender
    
    echo ""
    echo "=== Creating desktop entry ==="
    sudo tee /usr/share/applications/blender.desktop > /dev/null << EOF
[Desktop Entry]
Name=Blender
GenericName=3D Modeler
Comment=3D modeling, animation, rendering and post-production
Exec=/opt/blender/blender %f
Icon=/opt/blender/blender.svg
Terminal=false
Type=Application
Categories=Graphics;3DGraphics;
MimeType=application/x-blender;
EOF

    echo ""
    echo "=== Installation complete! ==="
    echo ""
    blender --version
    echo ""
    echo "Run Blender with: blender"
    echo "Or find it in your applications menu"
    
else
    echo ""
    echo "Official ARM64 build not available for version $BLENDER_VERSION"
    echo ""
    echo "=== Trying alternative installation methods ==="
    echo ""
    
    # Try flatpak
    if command -v flatpak &> /dev/null; then
        echo "Attempting Flatpak installation..."
        flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
        if flatpak install -y flathub org.blender.Blender; then
            echo ""
            echo "=== Blender installed via Flatpak ==="
            echo "Run with: flatpak run org.blender.Blender"
            exit 0
        fi
    fi
    
    # Fall back to building from source
    echo ""
    echo "=== Building Blender from source ==="
    echo "WARNING: This will take several hours on Jetson!"
    echo ""
    read -p "Do you want to build from source? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Alternative: Install an older version or use the Python-only workflow"
        echo "You can still use the pose JSON export without Blender's GUI"
        exit 1
    fi
    
    # Install build dependencies
    echo "Installing build dependencies..."
    sudo apt-get update
    sudo apt-get install -y \
        build-essential cmake git subversion \
        libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev \
        libglew-dev libpng-dev libjpeg-dev libfreetype6-dev \
        libopenexr-dev libopenal-dev libsdl2-dev libfftw3-dev \
        libtiff-dev libwebp-dev liblzma-dev libzstd-dev \
        libopenjp2-7-dev libhdf5-dev libopencolorio-dev \
        libboost-all-dev libeigen3-dev libxml2-dev libyaml-cpp-dev \
        libvulkan-dev glslang-tools spirv-tools \
        libepoxy-dev libpugixml-dev libpotrace-dev \
        libopenimageio-dev \
        libavdevice-dev libavfilter-dev libavformat-dev libavcodec-dev libavutil-dev libswscale-dev libswresample-dev \
        libtbb-dev libjemalloc-dev libgmp-dev \
        software-properties-common \
        libraw-dev libilmbase-dev libheif-dev libgif-dev
    
    # Install Python 3.11 (required by Blender 5.0)
    echo ""
    echo "=== Installing Python 3.11 (required by Blender 5.0) ==="
    if ! command -v python3.11 &> /dev/null; then
        echo "Adding deadsnakes PPA for Python 3.11..."
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt-get update
    fi
    
    sudo apt-get install -y \
        python3.11 python3.11-dev python3.11-venv \
        libpython3.11-dev
    
    # Install pip for Python 3.11 and required packages
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 || true
    python3.11 -m pip install --user numpy requests || true
    
    echo "Python 3.11 installed: $(python3.11 --version)"
    
    # Check/create swap to prevent OOM during compilation
    # 16GB swap is needed for Blender linking phase
    if [ $(swapon --show | wc -l) -eq 0 ]; then
        echo "Creating 16GB swap file to prevent OOM during build..."
        sudo fallocate -l 16G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=16384
        sudo chmod 600 /swapfile
        sudo mkswap /swapfile
        sudo swapon /swapfile
        echo "Swap enabled"
    fi
     
    # Install Embree 4.x from source (required for Cycles, not available as ARM package)
    echo ""
    echo "=== Building Embree 4.x from source ==="
   
    # Limit parallel jobs to prevent OOM (use half the cores, minimum 2)
    # Use only 2 parallel jobs maximum to prevent OOM crashes
    # Blender linking uses huge amounts of RAM per job
    SAFE_JOBS=2
    echo "Using $SAFE_JOBS parallel jobs to prevent memory exhaustion (OOM)"
    
    if [ ! -f "/usr/local/lib/libembree4.so" ]; then
        EMBREE_DIR="$HOME/embree_build"
        mkdir -p "$EMBREE_DIR"
        cd "$EMBREE_DIR"
        
        if [ ! -d "embree" ]; then
            git clone --depth 1 --branch v4.3.3 https://github.com/embree/embree.git
        fi
        cd embree
        rm -rf build
        mkdir -p build && cd build
        
        cmake .. \
            -DCMAKE_BUILD_TYPE=Release \
            -DEMBREE_ISPC_SUPPORT=OFF \
            -DEMBREE_TUTORIALS=OFF \
            -DEMBREE_STATIC_LIB=OFF \
            -DEMBREE_MAX_ISA=NONE \
            -DEMBREE_ISA_NEON=ON \
            -DCMAKE_INSTALL_PREFIX=/usr/local
        
        # Use limited jobs to prevent OOM
        make -j$SAFE_JOBS
        
        # Create .deb package for Embree
        echo "Creating Embree .deb package..."
        if ! command -v checkinstall &> /dev/null; then
            sudo apt-get install -y checkinstall
        fi
        
        sudo checkinstall \
            --pakdir="$HOME" \
            --pkgname="embree4-jetson" \
            --pkgversion="4.3.3" \
            --pkgrelease="1" \
            --pkgarch="arm64" \
            --pkglicense="Apache-2.0" \
            --pkggroup="libs" \
            --maintainer="jetson-build@local" \
            --provides="embree4" \
            --nodoc \
            --default \
            make install
        
        sudo ldconfig
        echo "Embree 4.x installed and packaged successfully"
        echo "Package: $HOME/embree4-jetson_4.3.3-1_arm64.deb"
    else
        echo "Embree 4.x already installed"
    fi
    
    # Build OpenImageIO 2.5 from source (Ubuntu 22.04's v2.2 has hash function incompatibility)
    echo ""
    echo "=== Building OpenImageIO 2.5 from source ==="
    echo "(System v2.2 has C++ hash function incompatibility with Blender 5.0)"
    
    # Remove system OIIO to avoid conflicts
    sudo apt-get remove -y libopenimageio-dev openimageio-tools 2>/dev/null || true
    
    if [ ! -f "/usr/local/lib/libOpenImageIO.so" ]; then
        OIIO_DIR="$HOME/oiio_build"
        mkdir -p "$OIIO_DIR"
        cd "$OIIO_DIR"
        
        if [ ! -d "OpenImageIO" ]; then
            git clone --depth 1 --branch v2.5.16.0 https://github.com/AcademySoftwareFoundation/OpenImageIO.git
        fi
        cd OpenImageIO
        rm -rf build
        mkdir -p build && cd build
        
        cmake .. \
            -DCMAKE_BUILD_TYPE=Release \
            -DCMAKE_INSTALL_PREFIX=/usr/local \
            -DOIIO_BUILD_TESTS=OFF \
            -DOIIO_BUILD_TOOLS=ON \
            -DUSE_PYTHON=OFF \
            -DUSE_QT=OFF \
            -DUSE_OPENCV=OFF \
            -DUSE_OPENGL=OFF \
            -DUSE_PTEX=OFF \
            -DUSE_NUKE=OFF \
            -DUSE_OPENVDB=OFF \
            -DSTOP_ON_WARNING=OFF
        
        # Use limited jobs to prevent OOM
        make -j$SAFE_JOBS
        
        # Create .deb package for OpenImageIO
        echo "Creating OpenImageIO .deb package..."
        if ! command -v checkinstall &> /dev/null; then
            sudo apt-get install -y checkinstall
        fi
        
        sudo checkinstall \
            --pakdir="$HOME" \
            --pkgname="openimageio-jetson" \
            --pkgversion="2.5.16" \
            --pkgrelease="1" \
            --pkgarch="arm64" \
            --pkglicense="Apache-2.0" \
            --pkggroup="libs" \
            --maintainer="jetson-build@local" \
            --provides="openimageio" \
            --nodoc \
            --default \
            make install
        
        sudo ldconfig
        echo "OpenImageIO 2.5 installed and packaged successfully"
        echo "Package: $HOME/openimageio-jetson_2.5.16-1_arm64.deb"
    else
        echo "OpenImageIO already installed from source"
    fi
    
    # Install shaderc (required for Vulkan shader compilation)
    echo ""
    echo "=== Installing shaderc ==="
    if ! pkg-config --exists shaderc 2>/dev/null; then
        echo "Building shaderc from source..."
        SHADERC_DIR="$HOME/shaderc_build"
        mkdir -p "$SHADERC_DIR"
        cd "$SHADERC_DIR"
        
        if [ ! -d "shaderc" ]; then
            git clone https://github.com/google/shaderc.git
        fi
        cd shaderc
        ./utils/git-sync-deps
        rm -rf build
        mkdir -p build && cd build
        cmake -DCMAKE_BUILD_TYPE=Release \
              -DSHADERC_SKIP_TESTS=ON \
              -DSHADERC_SKIP_EXAMPLES=ON \
              ..
        
        # Use limited jobs to prevent OOM
        # Use only 2 jobs to prevent OOM
        SAFE_JOBS=2
        make -j$SAFE_JOBS
        
        # Create .deb package for shaderc
        echo "Creating shaderc .deb package..."
        if ! command -v checkinstall &> /dev/null; then
            sudo apt-get install -y checkinstall
        fi
        
        sudo checkinstall \
            --pakdir="$HOME" \
            --pkgname="shaderc-jetson" \
            --pkgversion="2024.1" \
            --pkgrelease="1" \
            --pkgarch="arm64" \
            --pkglicense="Apache-2.0" \
            --pkggroup="libs" \
            --maintainer="jetson-build@local" \
            --provides="shaderc" \
            --nodoc \
            --default \
            make install
        
        sudo ldconfig
        echo "shaderc installed and packaged successfully"
        echo "Package: $HOME/shaderc-jetson_2024.1-1_arm64.deb"
    else
        echo "shaderc already installed"
    fi
    
    # Install updated Vulkan headers (Jetson's are too old for Blender 5.0)
    echo ""
    echo "=== Installing updated Vulkan headers ==="
    VULKAN_HEADERS_VERSION="1.3.290"
    
    if [ ! -f "/usr/include/vulkan/vulkan_core.h" ] || ! grep -q "VK_KHR_dynamic_rendering_local_read" /usr/include/vulkan/vulkan_core.h 2>/dev/null; then
        echo "Updating Vulkan headers to version $VULKAN_HEADERS_VERSION..."
        
        # Backup old headers
        if [ -d "/usr/include/vulkan" ] && [ ! -d "/usr/include/vulkan.bak" ]; then
            sudo mv /usr/include/vulkan /usr/include/vulkan.bak
        fi
        
        VULKAN_BUILD_DIR="$HOME/vulkan_headers_build"
        mkdir -p "$VULKAN_BUILD_DIR"
        cd "$VULKAN_BUILD_DIR"
        
        # Download and install Vulkan headers
        if [ ! -d "Vulkan-Headers" ]; then
            git clone --depth 1 --branch v${VULKAN_HEADERS_VERSION} https://github.com/KhronosGroup/Vulkan-Headers.git
        fi
        cd Vulkan-Headers
        sudo cmake -B build -DCMAKE_INSTALL_PREFIX=/usr
        sudo cmake --install build
        
        # Download and install Vulkan utility libraries
        cd "$VULKAN_BUILD_DIR"
        if [ ! -d "Vulkan-Utility-Libraries" ]; then
            git clone --depth 1 --branch v${VULKAN_HEADERS_VERSION} https://github.com/KhronosGroup/Vulkan-Utility-Libraries.git
        fi
        cd Vulkan-Utility-Libraries
        sudo cmake -B build -DCMAKE_INSTALL_PREFIX=/usr -DVULKAN_HEADERS_INSTALL_DIR=/usr
        sudo cmake --install build
        
        echo "Vulkan headers updated to $VULKAN_HEADERS_VERSION"
    else
        echo "Vulkan headers already up to date"
    fi
    
    # Clone Blender
    BUILD_DIR="$HOME/blender_build"
    mkdir -p "$BUILD_DIR"
    cd "$BUILD_DIR"
    
    if [ ! -d "blender" ]; then
        echo "Cloning Blender source..."
        git clone --depth 1 --branch v${BLENDER_VERSION} https://projects.blender.org/blender/blender.git
    fi
    
    cd blender
    
    # Update submodules
    make update
    
    # Clean previous build
    echo ""
    echo "=== Cleaning previous build ==="
    rm -rf ../build_linux
    mkdir -p ../build_linux
    
    # Build with explicit Python 3.11 paths
    echo ""
    echo "=== Configuring Blender with CMake ==="
    cd ../build_linux
    
    # Force use of ld.bfd instead of ld.gold (gold doesn't support memory-saving flags)
    # and use linker flags to reduce memory usage during linking
    export LDFLAGS="-fuse-ld=bfd -Wl,--no-keep-memory"
    
    cmake ../blender \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_PREFIX_PATH="/usr/local" \
        -DCMAKE_EXE_LINKER_FLAGS="-fuse-ld=bfd -Wl,--no-keep-memory" \
        -DCMAKE_SHARED_LINKER_FLAGS="-fuse-ld=bfd -Wl,--no-keep-memory" \
        -DPYTHON_VERSION=3.11 \
        -DPYTHON_LIBRARY=/usr/lib/aarch64-linux-gnu/libpython3.11.so \
        -DPYTHON_LIBPATH=/usr/lib/aarch64-linux-gnu \
        -DPYTHON_INCLUDE_DIR=/usr/include/python3.11 \
        -DPYTHON_INCLUDE_CONFIG_DIR=/usr/include/python3.11 \
        -DWITH_PYTHON_INSTALL=OFF \
        -DWITH_INSTALL_PORTABLE=OFF \
        -DWITH_CYCLES_EMBREE=ON \
        -DEMBREE_ROOT_DIR=/usr/local \
        -DOPENIMAGEIO_ROOT_DIR=/usr/local \
        -DOpenImageIO_ROOT=/usr/local \
        -DWITH_CYCLES_PATH_GUIDING=OFF \
        -DWITH_CYCLES_DEVICE_OPTIX=OFF \
        -DWITH_OPENVDB=OFF \
        -DWITH_OPENVDB_BLOSC=OFF
    
    echo ""
    echo "=== Building Blender (this will take several hours) ==="
    # Use limited jobs to prevent OOM
    # Use only 2 jobs to prevent OOM during linking
    # If still crashing, try: make -j1
    SAFE_JOBS=2
    echo "Using $SAFE_JOBS parallel jobs (limited to prevent OOM)"
    make -j$SAFE_JOBS
    
    # Install
    echo ""
    echo "=== Installing Blender ==="
    sudo make install
    
    echo ""
    echo "=== Build complete! ==="
    
    # Create .deb package
    echo ""
    echo "=== Creating .deb package ==="
    
    # Install checkinstall if not present
    if ! command -v checkinstall &> /dev/null; then
        sudo apt-get install -y checkinstall
    fi
    
    DEB_NAME="blender-${BLENDER_VERSION}-jetson-arm64"
    DEB_OUTPUT_DIR="$HOME"
    
    # Create deb package using checkinstall
    sudo checkinstall \
        --pakdir="$DEB_OUTPUT_DIR" \
        --pkgname="blender" \
        --pkgversion="${BLENDER_VERSION}" \
        --pkgrelease="1" \
        --pkgarch="arm64" \
        --pkglicense="GPL" \
        --pkggroup="graphics" \
        --maintainer="jetson-build@local" \
        --provides="blender" \
        --requires="" \
        --nodoc \
        --default \
        make install
    
    # Find and rename the created deb
    DEB_FILE=$(ls -t "$DEB_OUTPUT_DIR"/blender*.deb 2>/dev/null | head -1)
    if [ -n "$DEB_FILE" ]; then
        FINAL_DEB="$DEB_OUTPUT_DIR/${DEB_NAME}.deb"
        mv "$DEB_FILE" "$FINAL_DEB"
        echo ""
        echo "=============================================="
        echo ".deb package created: $FINAL_DEB"
        echo "=============================================="
        echo ""
        echo "To install on another Jetson:"
        echo "  sudo dpkg -i ${DEB_NAME}.deb"
        echo "  sudo apt-get install -f  # Fix dependencies"
        echo ""
    else
        echo "Warning: Could not create .deb package"
    fi
    
    # Cleanup build directories
    echo ""
    echo "=== Cleaning up build directories ==="
    rm -rf "$HOME/embree_build"
    rm -rf "$HOME/shaderc_build"
    rm -rf "$HOME/vulkan_headers_build"
    rm -rf "$HOME/blender_build"
    echo "Build directories removed"
fi

# Cleanup
rm -rf "$DOWNLOAD_DIR"

echo ""
echo "=============================================="
echo "Blender installation finished!"
echo "=============================================="
echo ""
echo "=== Created .deb packages ==="
echo "  $HOME/embree4-jetson_4.3.3-1_arm64.deb"
echo "  $HOME/shaderc-jetson_2024.1-1_arm64.deb"
echo "  $HOME/blender-${BLENDER_VERSION}-jetson-arm64.deb"
echo ""
echo "To install on another Jetson (in order):"
echo "  sudo dpkg -i embree4-jetson_4.3.3-1_arm64.deb"
echo "  sudo dpkg -i shaderc-jetson_2024.1-1_arm64.deb"
echo "  sudo dpkg -i blender-${BLENDER_VERSION}-jetson-arm64.deb"
echo "  sudo apt-get install -f  # Fix any missing dependencies"
echo ""
echo "To use with YOLO Pose:"
echo "  1. Run pose detection: python yolo_pose_blender.py --output poses.json"
echo "  2. Open Blender and install the addon: blender_pose_receiver.py"
echo "  3. Import the poses JSON file"
echo ""

