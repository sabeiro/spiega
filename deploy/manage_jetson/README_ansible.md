# YOLO Pose Estimation - Ansible Deployment

Ansible playbook for deploying and running the YOLO pose estimation project on NVIDIA Jetson devices.

## Prerequisites

### On Control Machine (your computer)

```bash
# Install Ansible
pip install ansible

# Or on Ubuntu/Debian
sudo apt install ansible
```

### On Jetson Device

- JetPack installed (CUDA, cuDNN, TensorRT)
- SSH access enabled
- Sudo privileges for the user

## Quick Start

1. **Configure inventory:**
   ```bash
   # Edit inventory.yml with your Jetson's IP/hostname
   nano inventory.yml
   ```

2. **Test connection:**
   ```bash
   ansible jetson -m ping
   ```

3. **Run full setup:**
   ```bash
   ansible-playbook playbook.yml
   ```

## Usage

### Run Everything (First Time Setup)

```bash
# Full installation: OpenCV, OpenFrameworks, Python env, models
ansible-playbook playbook.yml
```

### Run Specific Components

```bash
# Setup only (no running)
ansible-playbook playbook.yml --tags setup

# Build OpenCV with CUDA only
ansible-playbook playbook.yml --tags opencv

# Setup Python environment only
ansible-playbook playbook.yml --tags python

# Setup OpenFrameworks only
ansible-playbook playbook.yml --tags openframeworks

# Prepare YOLO models only
ansible-playbook playbook.yml --tags model
```

### Run the Applications

```bash
# Run Python pose detector
ansible-playbook playbook.yml --tags "python,run"

# Build and run OpenFrameworks app
ansible-playbook playbook.yml --tags "openframeworks,run"
```

### Cleanup

```bash
# Remove build artifacts (keeps installed software)
ansible-playbook playbook.yml --tags cleanup
```

## Configuration

### Inventory Variables

Edit `inventory.yml` to configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `ansible_host` | jetson | Jetson hostname or IP |
| `ansible_user` | sab | SSH username |
| `cuda_arch` | 8.7 | CUDA compute capability |
| `yolo_model` | yolov8n-pose | YOLO model name |
| `use_camera` | false | Use camera or video file |
| `video_file` | sfondo_seba.mp4 | Input video file |

### CUDA Architecture by Device

| Device | cuda_arch |
|--------|-----------|
| Jetson Orin (Nano/NX/AGX) | 8.7 |
| Jetson Xavier (NX/AGX) | 7.2 |
| Jetson Nano | 5.3 |
| Jetson TX2 | 6.2 |

## Project Structure

```
cv/
├── media/                    # Video files
│   └── sfondo_seba.mp4
├── model/                    # YOLO models
│   ├── yolov8n-pose.onnx
│   └── yolov8n-pose.pt
├── pose_estimate_of/         # OpenFrameworks app
│   ├── src/
│   │   ├── main.cpp
│   │   ├── ofPoseEstimate.cpp
│   │   └── ofPoseEstimate.h
│   └── bin/
│       └── pose_estimate_of
├── pose_estimate_py/         # Python scripts
│   ├── yolo_pose_blender.py
│   ├── blender_pose_receiver.py
│   └── detect.py
└── script/                   # Deployment scripts
    ├── playbook.yml          # Main Ansible playbook
    ├── inventory.yml         # Host configuration
    ├── ansible.cfg           # Ansible settings
    └── build_opencv_cuda.sh  # Manual OpenCV build
```

## Troubleshooting

### SSH Connection Issues

```bash
# Test SSH connection
ssh sab@jetson

# If using key-based auth, ensure key is loaded
ssh-add ~/.ssh/id_rsa
```

### OpenCV Build Fails

```bash
# Check CUDA installation on Jetson
nvcc --version
cat /usr/local/cuda/version.txt

# Increase swap if OOM during build
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### OpenFrameworks Display Issues

```bash
# Ensure X11 forwarding or run locally on Jetson
export DISPLAY=:0

# Or use VNC/remote desktop
```

### Model Export Fails

```bash
# Install ultralytics manually
pip install ultralytics

# Download model manually
yolo export model=yolov8n-pose.pt format=onnx
```

## Advanced Usage

### Run on Multiple Jetsons

```yaml
# inventory.yml
jetson:
  hosts:
    jetson-1:
      ansible_host: 192.168.1.100
    jetson-2:
      ansible_host: 192.168.1.101
    jetson-3:
      ansible_host: 192.168.1.102
```

```bash
# Deploy to all
ansible-playbook playbook.yml

# Deploy to specific host
ansible-playbook playbook.yml --limit jetson-1
```

### Custom Variables

```bash
# Override variables from command line
ansible-playbook playbook.yml \
  -e "yolo_model=yolov8s-pose" \
  -e "use_camera=true" \
  -e "camera_id=0"
```

### Dry Run

```bash
# Check what would be changed without making changes
ansible-playbook playbook.yml --check --diff
```

