#!/bin/bash

bash /app/run.sh &
unsloth studio --host 0.0.0.0 -p 8888
exec "bash -c 'python3 -u -m uvicorn agent:app --host 0.0.0.0 --port 8001 --reload --reload-dir /app'" &
