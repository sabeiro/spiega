#!/usr/bin/env python3
"""
LLaMA-GPT-Tool MCP Server with Hybrid GPU/CPU Routing

Architcture:
- Ollama (GPU): Fast GPU inference at 11434
- lm_studio (CPU): CPU inference using system RAM at 1234
- gptel (Emacs) routes via this MCP server

Routing Logic:
1. Try Ollama GPU first (fast)
2. If Ollama OOM/blocked, fallback to lm_studio CPU
3. Monitor Ollama VRAM, auto-switch to CPU if needed
"""

import os
import requests
import json
import time
from typing import Optional, Dict, Any

# Service endpoints
OLLAMA_ENDPOINT = "http://127.0.0.1:11434"
LMSTUDIO_ENDPOINT = "http://127.0.0.1:1234"

# Model selection
OLLAMA_DEFAULT_MODEL = "qwen3.5:9b-q4_K_M"
LMSTUDIO_DEFAULT_MODEL = "qwen2.5:7b-q4_K_M"  # Smaller model for CPU

# Health check endpoints
OLLAMA_HEALTH = f"{OLLAMA_ENDPOINT}/api/ps"
LMSTUDIO_HEALTH = f"{LMSTUDIO_ENDPOINT}/models"

class HybridLLaMAServer:
    def __init__(self):
        self.model = OLLAMA_DEFAULT_MODEL
        self.use_gpu = True
        self.last_error = None
        
    def is_ollama_available(self) -> bool:
        """Check if Ollama (GPU) is healthy and model is loaded"""
        try:
            response = requests.get(OLLAMA_HEALTH, timeout=5)
            data = response.json()
            
            # Check if current model is loaded in GPU VRAM
            model_loaded = any(m['name'] == self.model for m in data)
            
            # Check VRAM usage
            if response.text:
                vram_used = int(data[0].get('vram_used', 0) if data else 0)
                vram_total = int(data[0].get('vram_total', 10e9) if data else 10e9)
                
                # If using >80% VRAM, warn or switch to CPU
                if vram_used > vram_total * 0.8:
                    print(f"⚠️  VRAM high ({vram_used}>{vram_total*0.8}) - will fallback to CPU")
                return model_loaded
            return False
            
        except requests.exceptions.ConnectionError:
            print(f"❌ Ollama not available at {OLLAMA_ENDPOINT}")
            self.last_error = "Connection refused"
            return False
        except Exception as e:
            print(f"⚠️  Ollama health check error: {e}")
            self.last_error = str(e)
            return False
    
    def is_lmstudio_available(self) -> bool:
        """Check if lm_studio (CPU) is healthy"""
        try:
            response = requests.get(LMSTUDIO_HEALTH, timeout=5)
            return response.status_code in [200, 404]  # 404 may mean no models loaded
        except requests.exceptions.ConnectionError:
            print(f"❌ lm_studio not available at {LMSTUDIO_ENDPOINT}")
            self.last_error = "lm_studio connection failed"
            return False
        except Exception as e:
            print(f"⚠️  lm_studio health check: {e}")
            self.last_error = str(e)
            return False
    
    def generate(self, prompt: str, system_prompt: str = None, 
                 options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate response using hybrid routing
        
        Routing logic:
        1. Try Ollama GPU first
        2. If Ollama unavailable or OOM, use lm_studio CPU
        """
        if options is None:
            options = {
                'temperature': 0.7,
                'max_tokens': 4000,
                'top_p': 0.9,
                'repeat_penalty': 1.1
            }
        
        try:
            # Priority: Ollama GPU
            if self.use_gpu and self.is_ollama_available():
                print(f"✨ Using Ollama GPU ({self.model})")
                return self._call_ollama(prompt, system_prompt, options)
            
            # Fallback to lm_studio CPU
            print(f"🔄 Using lm_studio CPU ({LMSTUDIO_DEFAULT_MODEL})")
            return self._call_lmstudio(prompt, options)
            
        except Exception as e:
            print(f"❌ Generation error: {e}")
            self.last_error = str(e)
            
            # Automatic fallback to CPU
            if self.use_gpu and not self.is_ollama_available():
                print("⚠️  GPU failed, auto-switching to CPU")
                self.use_gpu = False
                try:
                    return self._call_lmstudio(prompt, options)
                except:
                    raise
    
    def _call_ollama(self, prompt: str, system_prompt: Optional[str], 
                     options: Dict[str, Any]) -> Dict[str, Any]:
        """Call Ollama API (GPU)"""
        try:
            # Prepare request
            payload = json.dumps({
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": options,
                "system": system_prompt or "You are a helpful AI assistant."
            })
            
            # Send to Ollama API
            response = requests.post(
                f"{OLLAMA_ENDPOINT}/api/generate",
                headers={"Content-Type": "application/json"},
                data=payload,
                timeout=120
            )
            
            response.raise_for_status()
            data = response.json()
            
            result = {
                "response": data.get('response', ''),
                "model": data.get('model', self.model),
                "done": True,
                "source": "ollama-gpu",
                "system_fulfilled": data.get('done', True),
                "stop": data.get('done_reason', '')
            }
            
            print(f"✅ Ollama GPU response ({len(result['response'])} chars)")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Ollama API error: {e}")
            raise
    
    def _call_lmstudio(self, prompt: str, 
                      options: Dict[str, Any]) -> Dict[str, Any]:
        """Call lm_studio API (CPU/RAM)"""
        try:
            payload = json.dumps({
                "prompt": prompt,
                "n_predict": options.get('max_tokens', 4000),
                "temperature": options.get('temperature', 0.7),
                "top_k": 50,
                "top_p": options.get('top_p', 0.9),
                "repeat_penalty": options.get('repeat_penalty', 1.1),
                "n_ctx": 8192
            })
            
            response = requests.post(
                f"{LMSTUDIO_ENDPOINT}/chat/completion",
                headers={"Content-Type": "application/json"},
                data=payload,
                timeout=120
            )
            
            response.raise_for_status()
            data = response.json()
            
            result = {
                "response": data.get('text', data.get('choices', [{}])[0].get('text', '')),
                "model": LMSTUDIO_DEFAULT_MODEL,
                "done": True,
                "source": "lmstudio-cpu"
            }
            
            print(f"✅ lm_studio CPU response ({len(result['response'])} chars)")
            return result
            
        except Exception as e:
            print(f"⚠️  lm_studio API error: {e}")
            raise
    
    def load_model(self, model_name: str, source: str = "ollama"):
        """Load a model into the appropriate backend"""
        if source == "ollama":
            # Load into Ollama GPU
            response = requests.post(
                f"{OLLAMA_ENDPOINT}/api/pull",
                json={"name": model_name, "insecure": False},
                timeout=300
            )
            print(f"📥 Pulling model to GPU: {model_name}")
        else:
            # Load into lm_studio CPU
            response = requests.post(
                f"{LMSTUDIO_ENDPOINT}/models",
                json={"name": model_name},
                timeout=300
            )
            print(f"📥 Pulling model to CPU: {model_name}")


# MCP server implementation using standard MCP protocol
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Hybrid LLaMA Server")

@mcp.tool()
def generate_text(
    messages: list[dict],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 4000
) -> str:
    """
    Generate text response using hybrid GPU/CPU routing
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model name to use (default: qwen3.5:9b-q4_K_M on GPU)
        temperature: Sampling temperature (0.0-2.0)
        max_tokens: Maximum tokens to generate
        
    Returns:
        str: Model response
    """
    if not model:
        model = OLLAMA_DEFAULT_MODEL
    
    server = HybridLLaMAServer()
    
    # Extract prompt from messages
    prompt = ""
    system_prompt = None
    
    for msg in messages:
        if msg.get('role') == 'system':
            system_prompt = msg.get('content')
        elif msg.get('role') == 'user':
            prompt += f"{msg.get('content')}\n\n"
        elif msg.get('role') == 'assistant':
            prompt += msg.get('content') + "\n"
    
    if not prompt:
        raise ValueError("No user message found")
    
    # Generate response
    options = {
        'temperature': temperature,
        'max_tokens': max_tokens,
        'top_p': 0.9,
        'repeat_penalty': 1.1
    }
    
    result = server.generate(prompt, system_prompt, options)
    return result['response']

@mcp.tool()
def list_models(source: Optional[str] = None) -> list[str]:
    """
    List available models on GPU (Ollama) or CPU (lm_studio)
    
    Args:
        source: 'ollama' (GPU) or 'lmstudio' (CPU) or None for both
    """
    server = HybridLLaMAServer()
    
    models = []
    
    if not source:
        # Try Ollama first
        try:
            response = requests.get(f"{OLLAMA_ENDPOINT}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models.extend([m['name'] for m in data.get('models', [])])
                print(f"📦 Ollama GPU models ({len(models)} available)")
        except Exception as e:
            print(f"⚠️  Cannot list Ollama models: {e}")
        
        # Then lm_studio
        try:
            response = requests.get(f"{LMSTUDIO_ENDPOINT}/models", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models.extend([m['name'] for m in data.get('models', [])])
                print(f"💾 lm_studio CPU models ({len(models)} available)")
        except Exception as e:
            print(f"⚠️  Cannot list lm_studio models: {e}")
    
    elif source == "ollama":
        try:
            response = requests.get(f"{OLLAMA_ENDPOINT}/api/tags", timeout=5)
            if response.status_code == 200:
                models = [m['name'] for m in response.json()['models']]
        except:
            models = []
    
    elif source == "lmstudio":
        try:
            response = requests.get(f"{LMSTUDIO_ENDPOINT}/models", timeout=5)
            if response.status_code == 200:
                models = [m['name'] for m in response.json()['models']]
        except:
            models = []
    
    return models

@mcp.tool()
def switch_backend(source: str) -> dict:
    """
    Switch between GPU (Ollama) and CPU (lm_studio) inference
    
    Args:
        source: 'gpu' or 'cpu'
    """
    server = HybridLLaMAServer()
    
    if source == "gpu":
        server.use_gpu = True
        return {
            "status": "success",
            "source": "gpu",
            "endpoint": OLLAMA_ENDPOINT,
            "message": "Switched to GPU inference"
        }
    elif source == "cpu":
        server.use_gpu = False
        return {
            "status": "success",
            "source": "cpu",
            "endpoint": LMSTUDIO_ENDPOINT,
            "message": "Switched to CPU inference"
        }
    else:
        raise ValueError(f"Unknown source: {source}")

@mcp.tool()
def health_check() -> dict:
    """Check health of both backend services"""
    gpu_available = server.is_ollama_available()
    cpu_available = server.is_lmstudio_available()
    
    return {
        "gpu_available": gpu_available,
        "cpu_available": cpu_available,
        "active_backend": "gpu" if gpu_available else "cpu",
        "message": "Both backends operational"
    }

@mcp.tool()
def list_models() -> list[str]:
    """List models available on both GPU and CPU"""
    server = HybridLLaMAServer()
    
    models = []
    
    # List GPU models
    try:
        response = requests.get(f"{OLLAMA_ENDPOINT}/api/tags", timeout=5)
        if response.status_code == 200:
            models.extend([m['name'] for m in response.json()['models']])
    except:
        pass
    
    # List CPU models
    try:
        response = requests.get(f"{LMSTUDIO_ENDPOINT}/models", timeout=5)
        if response.status_code == 200:
            models.extend([m['name'] for m in response.json()['models']])
    except:
        pass
    
    print(f"📦 Models: {models}")
    return models
