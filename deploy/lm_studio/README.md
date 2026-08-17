# LLM Studio on NVIDIA Jetson CUDA

## 🎴 GPU Support Available
This installation uses NVIDIA Jetson with full CUDA support.

## How to Run

### Option 1: Run script directly
```bash
cd ~/lav/src/blender_cv/mcp_server/
source setup.sh && bash run_lm_studio.sh
```

### Option 2: Run directly
```bash
pip install llm-studio==0.9.0 uvicorn
cd ~/lav/src/blender_cv/mcp_server/lm_studio/
python3 -m lm_studio.train.cli --port 8000 --host 0.0.0.0 --log-file logs/train.log
```

## Files Provided
- `Dockerfile` - For Docker deployments (if Docker available)
- `docker-compose.yml` - Docker Compose for easy deployment
- `run_lm_studio.sh` - Direct runner script
- `README.md` - This file

CUDA acceleration is automatically enabled by llm_studio when running on NVIDIA hardware.

## Note
The base llm_studio installation includes native CUDA support through llama.cpp. On your Jetson, GPU acceleration will work automatically.

