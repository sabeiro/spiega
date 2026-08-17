#!/bin/bash
set -e

echo "=== VLLM Setup Script ==="
echo "Creating necessary directories..."

# Create model directory if not exists
mkdir -p /home/sabeiro/lav/src/blender_cv/mcp_server/vllm/models
mkdir -p /home/sabeiro/lav/src/blender_cv/mcp_server/vllm/cache

# Create GPU device directory
mkdir -p /home/sabeiro/lav/src/blender_cv/mcp_server/vllm/.cache

echo "=== Directories created ==="
echo "Ready to run docker compose up -d"
