#!/bin/bash
# Camera Diagnostic Script for Jetson

echo "=========================================="
echo "Jetson Camera Diagnostics"
echo "=========================================="
echo

echo "1. Checking video devices..."
ls -la /dev/video* 2>/dev/null || echo "   No video devices found!"
echo

echo "2. Checking camera detection..."
v4l2-ctl --list-devices 2>/dev/null || echo "   v4l2-ctl not available"
echo

echo "3. Checking nvarguscamerasrc..."
gst-inspect-1.0 nvarguscamerasrc > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ nvarguscamerasrc available"
else
    echo "   ✗ nvarguscamerasrc NOT available"
    echo "   Install: sudo apt install nvidia-l4t-gstreamer"
fi
echo

echo "4. Testing GStreamer pipeline (5 seconds)..."
timeout 5 gst-launch-1.0 nvarguscamerasrc sensor-id=0 num-buffers=30 ! \
    'video/x-raw(memory:NVMM),width=1280,height=720,framerate=30/1' ! \
    nvvidconv ! fakesink 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ GStreamer pipeline works"
else
    echo "   ✗ GStreamer pipeline FAILED"
fi
echo

echo "5. Checking OpenCV GStreamer support..."
python3 << 'EOF'
import cv2
print(f"   OpenCV version: {cv2.__version__}")
print(f"   OpenCV path: {cv2.__file__}")

backends = []
for b in cv2.videoio_registry.getBackends():
    backends.append(cv2.videoio_registry.getBackendName(b))
print(f"   Backends: {backends}")

if 'GSTREAMER' in backends:
    print("   ✓ GStreamer backend available")
else:
    print("   ✗ GStreamer backend NOT available")
    print("   Fix: pip uninstall opencv-python opencv-python-headless")
    print("        sudo apt install python3-opencv")
EOF
echo

echo "6. Checking for processes using camera..."
fuser /dev/video0 2>/dev/null && echo "   Camera in use by PID above" || echo "   Camera not in use"
echo

echo "7. Testing OpenCV capture..."
python3 << 'EOF'
import cv2

# Try simple pipeline first
pipeline = "nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1280,height=720,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
print(f"   Pipeline: {pipeline[:60]}...")

cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        print(f"   ✓ Capture works! Frame shape: {frame.shape}")
    else:
        print("   ✗ Capture opened but read() failed")
    cap.release()
else:
    print("   ✗ Failed to open capture")
    print("   This usually means GStreamer backend issue")
EOF
echo

echo "=========================================="
echo "Diagnostics complete"
echo "=========================================="
