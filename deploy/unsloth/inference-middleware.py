#!/usr/bin/env python3
"""
UNSLOTH Request Middleware

Automatically adds UNSLOTH_TOKEN header/cookie to every inference request.
This middleware can be used with any HTTP client or Python requests library.

Usage:
    from middleware import add_unsloth_token
    headers = add_unsloth_token(original_headers=original_headers)
"""

import os
import requests
import typing
from typing import Dict, Optional


def get_unsloth_token() -> Optional[str]:
    """
    Retrieve UNSLOTH_TOKEN from environment variable.
    Falls back to 'unsloth_inference' if not set.
    """
    return os.environ.get("UNSLOTH_TOKEN") or os.environ.get("UNSLOTH_INFERENCE_TOKEN") or "unsloth_inference"


def add_unsloth_token(
    url: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    """
    Add UNSLOTH_TOKEN to request headers/cookies.
    
    Args:
        url: API endpoint URL
        headers: Original request headers
        cookies: Original request cookies
    
    Returns:
        Dict with UNSLOTH_TOKEN added to headers
    """
    result_headers = headers.copy() if headers else {}
    result_cookies = cookies.copy() if cookies else {}
    
    token = get_unsloth_token()
    
    # Add token as Authorization header (standard pattern)
    result_headers["Authorization"] = f"Bearer {token}"
    
    # Optionally add to user-agent
    result_headers.setdefault("User-Agent", "Unsloth-Inference-Client/1.0")
    
    return result_headers


def create_session() -> requests.Session:
    """
    Create a pre-configured requests.Session with UNSLOTH_TOKEN headers.
    Should be used for multiple requests to avoid overhead.
    """
    session = requests.Session()
    
    token = get_unsloth_token()
    session.headers["Authorization"] = f"Bearer {token}"
    session.headers["User-Agent"] = "Unsloth-Inference-Client/1.0"
    
    return session


def make_request(
    url: str,
    json_data: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    **kwargs
) -> typing.Union[requests.Response, requests.PreparedRequest]:
    """
    Convenience wrapper to make a request with automatic token handling.
    
    Args:
        url: API endpoint
        json_data: JSON payload (will be serialized to body)
        headers: Additional headers (token will be added)
        **kwargs: Extra args for requests (timeout, stream, etc.)
    
    Returns:
        Response object
    """
    session = create_session()
    
    result_headers = headers.copy() if headers else {}
    token = get_unsloth_token()
    result_headers["Authorization"] = f"Bearer {token}"
    
    response = session.post(
        url,
        headers=result_headers,
        json=json_data,
        **kwargs
    )
    
    return response


# API Endpoints
GEN_END = "/v1/generate"
CHAT_END = "/v1/chat/completions"
EMBED_END = "/v1/embeddings"
MODELS_END = "/v1/models"


def generate_text(
    prompt: str,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    **kwargs
) -> requests.Response:
    """Generate text using the local LLM."""
    return make_request(
        GEN_END,
        json_data={
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **{k: v for k, v in kwargs.items() if k in ["system", "stop"]}
        }
    )


def chat_completions(
    messages: list,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    **kwargs
) -> requests.Response:
    """Chat completions endpoint (conversational)."""
    return make_request(
        CHAT_END,
        json_data={
            "model": "Model",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **{k: v for k, v in kwargs.items() if k in ["stream"]}
        }
    )


def get_models() -> requests.Response:
    """List available models."""
    return make_request(MODELS_END)


def get_embeddings(
    input_text: str,
    **kwargs
) -> requests.Response:
    """Get embeddings from the model."""
    return make_request(
        EMBED_END,
        json_data={"input": input_text}
    )


__all__ = [
    "get_unsloth_token",
    "add_unsloth_token", 
    "create_session",
    "make_request",
    "generate_text",
    "chat_completions",
    "get_models",
    "get_embeddings"
]
