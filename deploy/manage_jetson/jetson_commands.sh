#camera
#nvgstcapture-1.0 --orientation 2
#enable pin
#sudo /opt/nvidia/jetson-io/jetson-io.py
v4l2-ctl --list-devices
#
# Build TensorRT engine from ONNX (run once on Jetson; then use .engine for inference)
# /usr/src/tensorrt/bin/trtexec --onnx=$HOME/dav/cv/model/yolov8n-pose.onnx --saveEngine=$HOME/dav/cv/model/trt_cache/yolov8n-pose.engine --fp16 --workspace=1073741824
#
# Benchmark existing engine
# /usr/src/tensorrt/bin/trtexec --loadEngine=$HOME/dav/cv/model/trt_cache/yolov8n-pose.engine --iterations=300 --avgRuns=300 | tee $HOME/dav/cv/model/result/yolo_run.log 
