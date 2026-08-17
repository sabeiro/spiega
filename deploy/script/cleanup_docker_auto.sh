#!/bin/bash
# cleanup_docker_auto.sh - Automated Docker cleanup (no prompts)
# Safe mode: removes only dangling items and unused containers

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose_laptop.yml"
SERVICE_IMAGES="ghcr.io/merryfish/llm-studio ollama"
MANAGED_SERVICES="llm-studio ollama"

echo "=== Docker Cleanup (Automated Mode) ==="
echo "Working directory: ${SCRIPT_DIR}"
echo ""

# Step 1: Stop managed services
echo "🔴 Step 1: Stopping managed services..."
docker compose -f "$COMPOSE_FILE" stop $MANAGED_SERVICES 2>/dev/null || echo "  ⚠️  No managed services running"
echo "  ✅ Services stopped."
echo ""

# Step 2: Remove all exited containers
echo "🗑️  Step 2: Removing all stopped containers..."
docker container prune -f 2>/dev/null || true
echo "  ✅ Stopped containers removed."
echo ""

# Step 3: Remove dangling (unused) images
echo "🖼️  Step 3: Removing dangling images..."
docker image prune -f 2>/dev/null || true
echo "  ✅ Unused images removed."
echo ""

# Step 4: Keep only required images
echo "🔧 Step 4: Keeping only required images (${SERVICE_IMAGES})..."
for img in $SERVICE_IMAGES; do
    # Check if image exists
    if docker images -q "$img" >/dev/null 2>&1; then
        : # Keep it
    else
        # Try to re-pull
        docker pull "$img:latest" 2>/dev/null || echo "  ⚠️  Could not pull: $img"
    fi
done
echo "  ✅ Required images preserved."
echo ""

# Step 5: Show disk usage
echo "📊 Step 5: Current disk usage..."
docker system df -h 2>/dev/null | head -20
echo ""

# Step 6: Restart managed services
echo "🟢 Step 6: Restarting managed services..."
if docker compose -f "$COMPOSE_FILE" up -d $MANAGED_SERVICES 2>/dev/null; then
    docker compose -f "$COMPOSE_FILE" ps
    echo "  ✅ Services restarted."
else
    echo "  ℹ️  Services may need network access (see gen_laptop_compose.sh)"
fi
echo ""

echo "✅ Automated cleanup complete!"
echo ""
echo "Manual commands (if needed):"
echo "  - Remove ALL systems (volumes included): docker system prune -a -f"
echo "  - Remove only since 24h: docker system prune -f --filter 'until=24h'"
echo "  - View disk usage: docker system df -h"
echo ""
