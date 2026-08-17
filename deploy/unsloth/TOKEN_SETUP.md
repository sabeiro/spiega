# UNSLOTH Token Configuration

## Overview

The Unsloth inference service requires `UNSLOTH_TOKEN` in every request. This document shows how to set up the token and ensure it's included in all API calls.

## Environment Variable Setup

### Docker Compose (Recommended)

Set the token in your environment before starting the service:

```bash
export UNSLOTH_TOKEN="your-token-here"
cd /home/sabeiro/lav/src/spiega/deploy/unsloth
docker compose up -d
```

### docker-compose.yml Configuration

The `docker-compose.yml` includes:

```yaml
environment:
  - UNSLOTH_TOKEN=${UNSLOTH_TOKEN:-your-api-token-here}
  - OPCODE_API_KEY=${UNSLOTH_TOKEN:-}
  - OPCODE_API_BASE_URL=http://localhost:8000/v1
```

This ensures the token is available to the container and passed to requests.

## Using the Python Middleware

### Option 1: Auto-configuration

The `inference-middleware.py` automatically reads `UNSLOTH_TOKEN`:

```python
from inference_middleware import create_session, generate_text

session = create_session()  # Auto-reads UNSLOTH_TOKEN from environment
response = generate_text(
    session=session,
    prompt="Explain quantum computing",
    max_tokens=200
)
```

### Option 2: HTTP Client with Token Header

```python
import requests
import os

UNSLITH_TOKEN = os.environ.get("UNSLOTH_TOKEN", "unsloth_inference")
headers = {
    "Authorization": f"Bearer {UNSLITH_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(
    "http://localhost:8000/v1/generate",
    headers=headers,
    json={
        "prompt": "Hello world",
        "max_tokens": 50
    }
)

print(response.json())
```

### Option 3: Direct MCP Client Integration

Pass the token as part of the client configuration:

```python
import mcp
from mcp import ClientSession, InitializationParams

params = InitializationParams(
    client_name="Pi-Coding-Agent-unsloth",
    client_info={
        "name": "unsloth-client",
        "version": "1.0"
    }
)

# Connect to the service
async with ClientSession(params) as session:
    await session.initialize()
    # All requests will include token automatically
    result = await session.call_tool("generate", {
        "prompt": "Hello",
        "token": UNSLITH_TOKEN
    })
```

## Token Environment Variables

### Standard Location

```bash
export UNSLOTH_TOKEN="your-token"
```

### Alternative Names

The middleware accepts these alternative names (they're equivalent):

- `UNSLOTH_TOKEN`
- `UNSLOTH_INFERENCE_TOKEN`
- `OPCODE_API_KEY`

### Docker Network Integration

For Docker, set the token before starting:

```bash
# Set token in host environment
docker export UNSLOTH_TOKEN="my-token"

# Start service with token
cd ~/lav/src/spiega/deploy/unsloth
docker compose up -d
```

## Request Examples

### Using requests library

```python
import requests
import os

token = os.environ.get("UNSLOTH_TOKEN", "default-token")
url = "http://localhost:8000/v1/generate"

payload = {
    "prompt": "Explain machine learning",
    "max_tokens": 256
}

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "X-Docker-Network": "mcp-inference-network"
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

### cURL

```bash
UNSLITH_TOKEN="your-token"

curl -X POST "http://localhost:8000/v1/generate" \
  -H "Authorization: Bearer $UNSLITH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello","max_tokens":50}'
```

## Docker Network Details

When running inside Docker:

```bash
# Token is available in container as environment variable
env UNSLOTH_TOKEN="${UNSLITH_TOKEN}"

# Request from inside container includes token automatically
curl -X POST "http://localhost:8000/v1/generate" \
  -H "Authorization: Bearer $UNSLOTH_TOKEN" \
  -d '{"prompt":"Test"}'
```

## Security Notes

- Keep `UNSLOTH_TOKEN` in your CI/CD secrets, not in git repos
- Rotate tokens regularly
- Use distinct API keys for different environments (dev, prod, test)
- Token is only stored in environment variable, not on disk

## Testing Setup

### 1. Verify Token is Available

```bash
docker compose exec unsloth env | grep UNSLOTH
```

Should show:
```
UNSLOTH_TOKEN=your-token-value
OPCODE_API_KEY=your-token-value
```

### 2. Test Inference Request

```bash
curl http://localhost:8000/v1/generate
```

### 3. Check Logs

```bash
docker compose logs -f unsloth
```

## Common Issues

**Issue: 401 Unauthorized**
```bash
# Solution: Verify token is set
export UNSLOTH_TOKEN="correct-token"
docker compose restart unsloth
```

**Issue: Token not found**
```bash
# Check environment
docker compose exec unsloth env | grep UNSLOTH

# Fix: Start with correct token
unset UNSLOTH
export UNSLOTH_TOKEN="new-token"
docker compose up -d
```

**Issue: Running inside Docker without token**
```bash
# Make token persistent as docker env var
echo "export UNSLOTH_TOKEN='your-token'" >> ~/.bashrc
source ~/.bashrc

# Start docker with token
docker compose up -d
```

---
EOF
cat /home/sabeiro/lav/src/spiega/deploy/unsloth/TOKEN_SETUP.md