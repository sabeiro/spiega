#https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/
#https://pypi.jetson-ai-lab.io/jp6/cu126
#https://pytorch.org/get-started/locally/

##---------------------------CUDA-------------------------------------------

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/arm64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-8 cuda-compat-12-8

##--------------------------current-system----------------------------

lspci | grep -i nvidia
hostnamectl
gcc --version
dpkg -l | grep nvidia-l4t-core
apt-cache show nvidia-jetpack
nvcc --version
nvidia-smi
grep CUDNN_MAJOR -A 2 /usr/include/cudnn_version.h
#git clone --branch v12.5 https://github.com/NVIDIA/cuda-samples.git
#cd cuda-samples/Samples/1_Utilities/deviceQuery
#make
./cuda-samples/Samples/1_Utilities/deviceQuery/deviceQuery
apt list linux-headers-$(uname -r) 


###-------------------------------apt--------------------------------

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip libopenblas-dev libjpeg-dev zlib1g-dev \
    libavcodec-dev libavformat-dev libswscale-dev

###nvidia docker
#https://docs.nvidia.com/jetson/agx-thor-devkit/user-guide/latest/setup_docker.html
sudo apt-get update
sudo apt install -y nvidia-container curl
curl https://get.docker.com | sh && sudo systemctl --now enable docker
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl daemon-reload && sudo systemctl restart docker
sudo usermod -aG docker $USER
newgrp docker
sudo nvpmodel -m 0
sudo jetson_clocks
docker info | grep -i nvidia

#sudo apt-get update
sudo apt install -y g++ freeglut3-dev build-essential libx11-dev libxmu-dev libxi-dev libglu1-mesa-dev libfreeimage-dev libglfw3-dev
sudo apt install -y nvidia-gds
sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libopenblas-dev libavcodec-dev libavformat-dev libswscale-dev
sudo apt install ubuntu-drivers-common
sudo apt-get install -y  python3-pip libopenblas-dev
sudo apt-get install -y zlib1g
sudo apt-get install -y libcudnn9-cross-aarch64-cuda-12
sudo apt-get install -y python3-pip libopenblas-dev
#sudo apt install cuda-compat


#wget raw.githubusercontent.com/pytorch/pytorch/5c6af2b583709f6176898c017424dc9981023c28/.ci/docker/common/install_cusparselt.sh
export CUDA_VERSION=12.8 # 
sudo bash ./install_cusparselt.sh


CUSPARSELT_VER="0.7.1.0"
#wget https://developer.download.nvidia.com/compute/cusparselt/redist/libcusparse_lt/linux-aarch64/libcusparse_lt-linux-aarch64-${CUSPARSELT_VER}-archive.tar.xz
#tar xf *.tar.xz
#sudo cp -a */include/* /usr/local/cuda/include/
#sudo cp -a */lib/* /usr/local/cuda/lib64/
#sudo ldconfig

# wget https://developer.download.nvidia.com/compute/cuda/repos/<distro>/<arch>/cuda-keyring_1.1-1_all.deb
# sudo dpkg -i cuda-keyring_1.1-1_all.deb


##----------------------------------pip----------------------------------

#https://pytorch.org/get-started/previous-versions/
pip install torch==2.9.1 torchvision==0.24.1 torchaudio==2.9.1 --index-url https://download.pytorch.org/whl/cu128

it clone --branch release/0.$VERSION https://github.com/pytorch/vision torchvision
cd torchvision
export BUILD_VERSION=0.$VERSION.0
python3 setup.py install --user # remove --user if installing in virtualenv
export TORCH_INSTALL=https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl
export TORCH_INSTALL=https://pypi.jetson-ai-lab.io/jp6/cu126/+f/37d/7e156cfb4a646/torch-2.10.0-cp310-cp310-linux_aarch64.whl#sha256=37d7e156cfb4a646c4d7347597727db1529d184108f703324dfff1842cec094e
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools pip wheel
python3 -m pip install numpy>2
#python3 -m pip install nvidia-pyindex
#python3 -m pip install nvidia-cuda-runtime-cu12
#python3 -m pip install --no-cache $TORCH_INSTALL
python3 -m pip install "https://pypi.jetson-ai-lab.io/jp6/cu126/+f/854/fe6d63a2a7526/torch_tensorrt-2.8.0+cu126-cp310-cp310-linux_aarch64.whl#sha256=854fe6d63a2a75266cf89df5ba6f1dcbe3a6716ed52db86c541fe7483f4199c1"
python3 -m pip install "https://pypi.jetson-ai-lab.io/jp6/cu126/+f/1b6/357c5532db61e/torchvision-0.25.0-cp310-cp310-linux_aarch64.whl#sha256=1b6357c5532db61e9bfe7ad69f73ba73e8214010de021da703d360d2cc16c3d7"


#python3 -m pip install nvidia-cuda-nvcc-cu12 nvidia-cublas-cu12 nvidia-cuda-opencl-cu12 nvidia-cuda-opencl-cu12 nvidia-nvjpeg-cu129

export PATH=${PATH}:/usr/local/cuda-12.6/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda-12.6/lib64
python -c "import torch"


python3 test_cuda.py
