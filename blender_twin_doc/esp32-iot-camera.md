# ESP32 IoT Camera Integration Project

## Overview

ESP32-based IoT cameras provide distributed sensing edge nodes for multi-camera systems, offering Wi-Fi/BLE connectivity, MQTT pub/sub capabilities, deep sleep mode, and support for multiple camera modules (RGB, thermal, depth).

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              ESP32 IoT Camera Nodes                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │
│  │  ESP32  │  │ ESP32   │  │ ESP32   │                  │
│  │ Camera  │  │ Camera  │  │ Camera  │                  │
│  │ (RGB)   │  │ (Thermal)│  │(Depth) │                  │
│  └────┬────┘  └────┬────┘  └────┬────┘                  │
│       │            │            │                        │
│   ┌───▼────────────▼────────────▼───┐                    │
│   │           Edge MQTT Broker      │                    │
│   │           (Mosquitto/Eclipse)   │                    │
│   └────────────┬───────────┬────────┘                    │
│                │           │                             │
│   ┌───────────▼───────────▼─────────┐  ┌───────────────┐│
│   │           Data Stream           │  │  3D Recons.   ││
│   │  ┌───────────────────────────┐  │  │                ││
│   │  │   Frame Capture           │  │  │  Pose Est.    ││
│   │  │   Sensor Fusion           │  │  │                ││
│   │  │   MQTT Pub/Sub              │  │  └───────────────┘│
│   │  └───────────────────────────┘  │                     │
│   └─────────┬────────────┬───────────┘                     │
│             │            │                                 │
│   ┌─────────▼───────────▼───────┐                          │
│   │   AI Models / Inference     │                          │
│   │   ┌─────────────────────┐   │                          │
│   │   │  YOLO/Deep Sort     │   │                          │
│   │   │  OpenCV Processing  │   │                          │
│   │   │  Pose Est. Model    │   │                          │
│   │   └─────────────────────┘   │                          │
│   └─────────────────────────────┘                          │
└─────────────────────────────────────────────────────────┘
```

---

## Hardware Configuration

### Supported ESP32 Camera Modules

| Module | Resolution | Frame Rate | Interface | Notes |
|--------|------------|------------|-----------|-------|
| OV2640 | 640x480 (VGA) | 30 FPS | I2C bus | Low-cost, RGB |
| OV7675 | 640x480 (VGA) | 30 FPS | I2C bus | Low-cost, RGB |
| OV8865 | 800x480 (WVGA) | 30 FPS | I2C bus | Higher res, color |
| IMX219 | 1280x720 (HD) | 30 FPS | CSI (CSI-2.0) | Higher res |
| IMX477 | 1920x1080 (QHD) | 60 FPS | CSI (CSI-2.0) | Global shutter |
| MIPI CSI | Up to 4K @ 60fps | N/A | MIPI CSI | Jetson compatible |
| Thermal | 640x480 (VGA) | 25 FPS | I2C bus | 10-50°C range |
| Depth (ToF) | 320x240 (QVGA) | 30 FPS | I2C bus | 0.2-1m range |
| RGB+Depth | 320x240 | 30 FPS | I2C bus | Dual capture |

### ESP32 IoT Camera Capabilities

**Sensors:**
- RGB camera (OV2640, OV7675, OV8865, IMX219, IMX477)
- Thermal sensor (MLX90614, TCS34725)
- Depth sensor (ToF, LIAR, MIPI CSI)
- Accelerometer + gyroscope (IMU)
- Barometric pressure
- Humidity sensor
- Microphone array (optional)

**Connectivity:**
- Wi-Fi @ 802.11 b/g/n 2.4GHz
- BLE 4.2/5.0
- MQTT over Wi-Fi/BLE
- HTTP/HTTPS client/server

**Power Management:**
- Deep sleep mode (microamp level)
- Wake on GPIO pin, touch, or motion
- Power saving sleep mode
- Brown-out detection

**Communication:**
- I2C for sensor data
- SPI for camera modules
- UART for serial console
- GPIO for digital I/O, PWM
- ADC for analog signals

---

## Software Architecture

### Camera Types

**1. RGB Camera (Color Imaging)**
- Cameras: OV2640, OV7675, OV8865, IMX219, IMX477
- Use Cases: Object detection, surveillance, face recognition
- Features: Auto-exposure, auto-focus, white balance
- Frame rate: 30-60 FPS

**2. Thermal Sensor**
- Camera: Infrared (MLX90614, TCS34725)
- Use Cases: Heat signature, temperature monitoring
- Features: Temperature calibration, thermal histogram
- Range: 10-50°C adjustable

**3. Depth Camera**
- Cameras: ToF (Time-of-Flight), LIAR
- Use Cases: Gesture control, proximity, obstacle avoidance
- Features: Point cloud output, 3D mapping
- Range: 0.2m to 1m typical

**4. RGB+Depth Fusion**
- Combined RGB and depth sensors
- Uses stereo vision or dual sensor approach
- 3D reconstruction from 2D images

### Sensor Fusion Pipeline

```
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│  RGB    │  │ Thermal │  │ Depth   │  │ IMU     │
│ Camera  │  │ Sensor  │  │ Camera  │  │ Sensors │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
     │            │            │            │
     └────────────┴────────────┴────────────┘
                           │
                 ┌────────▼────────┐
                 │   Fusion Engine │
                 │  ┌─────────────┐│
                 │  │ Data Merge   ││
                 │  │ Time Sync    ││
                 │  │ Kalman Filter││
                 │  └─────────────┘│
                 └────────┬─────────┘
                          │
                 ┌────────▼────────┐
                 │   Multi-Modality│
                 │   Sensor Fusion │
                 │  ┌─────────────┐│
                 │  │ 3D Point    ││
                 │  │ Cloud Build ││
                 │  │ Gesture Rec ││
                 │  └─────────────┘│
                 └────────┬─────────┘
                          │
                 ┌────────▼────────┐
                 │   MQTT Publish  │
                 │  ┌─────────────┐│
                 │  │ Frame Data  ││
                 │  │ Sensor Data ││
                 │  │ Metadata    ││
                 │  └─────────────┘│
                 └─────────────────┘
```

---

## MQTT Protocol Configuration

### Topic Structure

```
home/camera/{camera_id}/
├── stream/              # Live video frames
├── sensor/              # Sensor readings
├── config/              # Configuration
├── status/              # Operational status
└── meta/                # Metadata
```

### Example Topics

```
home/camera/iot-camera-1/stream/rgb
home/camera/iot-camera-1/stream/thermal
home/camera/iot-camera-1/sensor/temperature
home/camera/iot-camera-1/sensor/accelerometer
home/camera/iot-camera-1/sensor/gyroscope
home/camera/iot-camera-1/status/online
home/camera/iot-camera-1/config/settings
home/camera/iot-camera-1/meta/version
```

### Payload Examples

**Frame Data (RGB):**
```json
{
  "camera_id": "iot-camera-1",
  "timestamp": 1234567890000,
  "frame_type": "rgb",
  "width": 640,
  "height": 480,
  "bytes": "[base64_encoded_frame_data]"
}
```

**Sensor Data:**
```json
{
  "camera_id": "iot-camera-1",
  "timestamp": 1234567890000,
  "frame_type": "sensor",
  "temperature_celsius": 25.5,
  "accelerometer_x": 0.1,
  "accelerometer_y": 0.2,
  "accelerometer_z": 1.0,
  "gyroscope_x": 0.01,
  "gyroscope_y": 0.02,
  "gyroscope_z": 0.03,
  "pressure_hpa": 1013.25,
  "humidity_pct": 45.5
}
```

---

## Hardware Requirements

### Minimum Resources

| Device | RAM | CPU | Storage | GPU |
|--------|-----|-----|---------|-----|
| ESP32 | 520KB | Tenspeed | Flash | N/A |
| ESP32-CAM | 520KB | Quad-core | Flash | N/A |
| ESP32-C3 | 520KB | Quad-core | Flash | N/A |
| ESP32-S3 | 520KB+ | Quad-core | 4GB eMMC | Coral TPU |

### Jetson Edge Nodes

| Device | RAM | CPU | GPU | Notes |
|--------|-----|-----|-----|-------|
| Jetson Orin Nano 4GB | 4GB | 4x A76AE | 5 TOPS | Primary edge node |
| Jetson Orin Nano 8GB | 8GB | 4x A76AE + NPU | 120 TOPS | Enhanced inference |
| Jetson Xavier NX | 8GB | 216 TOPS | 20 TOPS | Previous gen |
| Jetson AGX | 32GB | 396 TOPS | 20 TOPS | High-end |

### PC Workstations

| GPU | RAM | Use Case |
|-----|-----|----------|
| NVIDIA RTX 5060 | 16GB+ | Rendering, batch processing |
| NVIDIA RTX 4070 | 12GB | AI inference, pose estimation |
| NVIDIA RTX 4080 | 24GB | High-throughput processing |

---

## Camera Calibration

### Intrinsics

```python
import numpy as np

# Camera intrinsics
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0, 0, 1]])

# Distortion coefficients
D = np.array([k1, k2, p1, p2, k3])
```

### Extrinsics

```python
# Rotation matrix
R = np.array([[...], [...], [...]])

# Translation vector
t = np.array([tx, ty, tz])
```

---

## Color Correction

### White Balance

```python
wb_modes = {
    'auto': 'Auto white balance',
    'incandescent': 'Incandescent lighting (3200K)',
    'tungsten': 'Tungsten/halogen (2800K)',
    'fluorescent': 'Fluorescent (4000K)',
    'daylight': 'Daylight (5500K)',
    'cloudy': 'Cloudy (6500K)',
    'shady': 'Shade (7500K)'
}
```

### HDR Processing

```python
def tone_mapping(luminance_map):
    """Adaptive tone mapping for HDR images"""
    from scipy.ndimage import gaussian_filter
    
    # Calculate exposure brackets
    short_exp = 0.7 * luminance_map
    mid_exp = 1.0 * luminance_map
    long_exp = 1.3 * luminance_map
    
    # Merge exposures with adaptive weighting
    merged = (short_exp * weight_short + 
              mid_exp * weight_mid + 
              long_exp * weight_long)
    
    return merged
```

---

## Deployment

### Quick Start

```bash
# Clone project
git clone git@github.com:sabeiro/lav/esp32-iot-camera.git

# Configure camera
cd esp32-iot-camera/camera_py
python camera_esp32_impl.py --camera ov2640 --resolution vga

# Monitor MQTT stream
python camera_py/mqtt_client.py --subscribe home/camera/iot-camera-1/stream

# View live frames
ffmpeg -rtsp://localhost:554/camera/1 -c copy
```

### Container Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  camera-mqtt-broker:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf

  camera-node-1:
    build:
      context: .
      dockerfile: Dockerfile.ESP32
    ports:
      - "554:554"
    env_file:
      - .env
    depends_on:
      - camera-mqtt-broker

  pose-estimation:
    image: python:3.10-slim
    command: python src/blender_cv/pose_estimation.py
    depends_on:
      - camera-mqtt-broker
```

---

## Testing & Validation

### Unit Tests

```python
def test_camera_framing():
    """Test camera frame capture timing"""
    camera = ESP32Camera(camera_id='test-1', camera_type='ov2640')
    camera.initialize_camera()
    
    frames_per_second = 0
    for _ in range(100):
        start = time.time()
        frame = camera.capture_frame()
        end = time.time()
        
        if frame:
            frames_per_second += 1
    
    assert frames_per_second >= 25, f"Frame rate too low: {frames_per_second} FPS"

def test_sensor_fusion():
    """Test multi-sensor data fusion"""
    camera = ESP32Camera(camera_id='test-fusion', camera_type='rgb_depth')
    camera.initialize_camera()
    
    sensor_data = camera.get_sensor_data()
    assert sensor_data, "Sensor data fusion failed"
    
    # Validate sensor readings
    assert 0 <= sensor_data['temperature_celsius'] <= 50
```

### Performance Benchmarks

```bash
# Capture performance
python benchmark_capture.py --camera ov2640 --iterations 100

# Frame rate measurement
python benchmark_fps.py --camera imx415 --resolution qhd

# Power consumption test
python benchmark_power.py --mode deep_sleep --duration 600
```

---

## Troubleshooting

### Common Issues

**Problem: Camera not detected**
- Check I2C bus address: `i2cdetect -y -r /dev/i2c-<bus>`
- Verify camera power: `lsusb` (for USB cameras)
- Check camera firmware: `esptool.py flash_start`

**Problem: Low frame rate**
- Reduce resolution: `--resolution vga`
- Enable deep sleep to save power
- Check MQTT connection bandwidth

**Problem: Sensor fusion drift**
- Recalibrate IMU: `python calibrate_imu.py`
- Check for magnetic interference
- Verify Kalman filter parameters

---

## Security Considerations

### MQTT Security

```yaml
# Enable TLS
tls:
  cert_file: /etc/mosquitto/cert.crt
  key_file: /etc/mosquitto/key.key

# Enable authentication
acl_file: /etc/mosquitto/acl.conf
allow_anonymous: false
```

### Firmware Signing

```bash
# Sign camera firmware
esptool.py write_flash 0x1000 ./camera.bin
esptool.py write_flash 0x8000 ./bootloader.bin
esptool.py write_flash 0x1000 ./firmware.bin
```

### HTTPS/TLS Certificates

```bash
# Generate certificates for MQTT over TLS
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem \
  -days 365 -nodes \
  -subj "/C=XX/ST=State/L=City/O=Organization/CN=MQTT"
```

---

## License

MIT License - See LICENSE file for details.

EOF
chmod +x /home/sabeiro/lav/src/blender_cv/esp32-iot-camera.md && echo "Documentation file created: esp32-iot-camera.md"
