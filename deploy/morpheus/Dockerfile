docker run --rm -ti --gpus=all -p8000:8000 -p8001:8001 -p8002:8002 \
  -v $PWD/models:/models \
  nvcr.io/nvidia/tritonserver:23.06-py3 \
  tritonserver --model-repository=/models/triton-model-repo \
    --exit-on-error=false \
    --log-info=true \
    --strict-readiness=false \
    --disable-auto-complete-config