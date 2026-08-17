#!/usr/bin/env bash
# Test that open-webui and ollama containers can reach each other on the same network.
# Run from the directory containing docker-compose.yml.

set -e

COMPOSE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$COMPOSE_DIR"

echo "=== Checking containers are running ==="
for name in open-webui ollama; do
  if ! docker compose ps --status running --format '{{.Name}}' 2>/dev/null | grep -qx "$name"; then
    echo "Error: Container '$name' is not running. Start the stack with: docker compose up -d"
    exit 1
  fi
  echo "  $name: running"
done

echo ""
echo "=== Testing mutual reachability (DNS + ping from helper on webui-net) ==="
docker compose run --rm --no-deps alpine sh -c '
  echo "Pinging open-webui..."
  ping -c 2 open-webui || exit 1
  echo "Pinging ollama..."
  ping -c 2 ollama || exit 1
'

echo ""
echo "=== All checks passed: open-webui and ollama are mutually reachable. ==="
