#!/usr/bin/env python3
"""
Local LLM Inference Service with Unsloth

A simple wrapper script to start a local LLM inference service using Unsloth.
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path


def get_gpu_info():
    """Get GPU information via nvidia-smi."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free,cuda.utilization", 
             "--format=csv,noheader"], 
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split('\n')
    except:
        return f"CUDA not detected or not available"


def find_best_model():
    """Find the best model to load based on available GPU memory."""
    gpu_mem = get_gpu_info()
    if not isinstance(gpu_mem, list):
        print(f"Could not detect GPU memory: {gpu_mem}")
        return None, None
    
    total_mem_gb = int(gpu_mem[0].split(' ')[2]) if len(gpu_mem[0].split(' ')) > 2 else 0
    
    if total_mem_gb >= 4.0:
        return "/model/gemma-4-E4B-it-Q4_K_M.gguf", "Q4_K_M"
    elif total_mem_gb >= 2.0:
        return "/model/tinyllama-1.1b-Q4_K_M.gguf", "Q4_K_M"
    else:
        return None, None


def start_inference(model_path=None, model_quantization=None, port=8000):
    """Start the inference service using Unsloth."""
    
    if model_path is None:
        model_path, model_quantization = find_best_model()
        
        if model_path is None:
            print("No suitable model found. Please specify a model path.")
            print("Available models can be placed in /model/ directory:")
            print("  - gemma-4-E4B-it-Q4_K_M.gguf (4.2GB)")
            print("  - gemma-1.5-4B-it-Q4_K_M.gguf (2.1GB)")
            print("  - tinyllama-1.1b-Q4_K_M.gguf (0.9GB)")
            return False
    
    print(f"Starting Unsloth inference service...")
    print(f"  Model: {model_path}")
    print(f"  Quantization: {model_quantization}")
    print(f"  Port: {port}")
    
    # Start unsloth serve
    cmd = [
        sys.executable, "-m", "unsloth", "serve",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--model", model_path,
        "--tokenizer", os.environ.get("MODEL_PATH", model_path)
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Inference service failed: {e}")
        return False
    
    print("Inference service started successfully!")
    print(f"Access via: http://localhost:{port}")
    return True


def check_model_exists():
    """Check if model files exist."""
    model_path, _ = find_best_model()
    if model_path:
        return Path(model_path).exists()
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Start Local LLM Inference Service with Unsloth"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default=None,
        help="Model path (auto-detect if not specified)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to listen on (default: 8000)"
    )
    parser.add_argument(
        "--no-gpu",
        action="store_true",
        help="Run CPU-only (use for testing)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("UNSLOTH LOCAL INFERENCE SERVICE")
    print("=" * 60)
    
    if args.no_gpu:
        print("Running without GPU acceleration...")
    
    # Check if model exists
    if args.model:
        model_path = args.model
        model_quantization = None
    else:
        model_path, model_quantization = find_best_model()
        if model_path is None and not args.no_gpu:
            print("\nWarning: No suitable model found.")
            print("Please add a model to /model/ directory or use --help for options.")
            return 0
    
    return start_inference(model_path=model_path)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
