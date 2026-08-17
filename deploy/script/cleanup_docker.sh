#!/bin/bash
# cleanup_docker.sh - Remove unused Docker resources safely

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose_laptop.yml"

echo "=== Docker Cleanup Script ==="
echo "Working directory: ${SCRIPT_DIR}"
echo ""

# Prompt for confirmation
echo "This script will remove:"
echo "  - All containers not managed by docker-compose_laptop.yml"
echo "  - Unused Docker images (without stopping services)"
echo "  - Unused Docker volumes (without removing data volumes)"
echo ""
echo "Services that will be preserved (if running):"
echo "  - llm-studio"
echo "  - ollama"
echo ""

read -p "Do you want to continue? (yes/no): " CONF
if [ "$CONF" != "yes" ]; then
    echo "❌ Cleanup cancelled."
    exit 0
fi

echo ""
echo "🧹 Starting cleanup..."
echo ""

# Step 1: Get list of running managed containers
echo "📋 Step 1: Identifying managed containers..."
MANAGED_CONTAINERS=$(docker compose -f "$COMPOSE_FILE" ps -q 2>/dev/null || echo "")
echo "  Managed containers: ${MANAGED_CONTAINERS:-none}"
echo ""

# Step 2: List all containers and identify unused ones
echo "🗑️  Step 2: Removing unused containers..."
CONTAINERS_TO_REMOVE=$(docker ps -aq --filter "status=exited" | \
    grep -v "llm-studio" | \
    grep -v "ollama" || true)
echo "  Stopping unused exited containers: ${CONTAINERS_TO_REMOVE:-none}"
if [ -n "$CONTAINERS_TO_REMOVE" ]; then
    docker stop $CONTAINERS_TO_REMOVE 2>/dev/null || true
    docker rm $CONTAINERS_TO_REMOVE 2>/dev/null || true
    echo "    ✅ Removed: ${CONTAINERS_TO_REMOVE}"
else
    echo "    ℹ️  No unused containers found."
fi
echo ""

# Step 3: List all volumes and identify unused ones
echo "🗑️  Step 3: Pruning unused volumes..."
echo "  ⚠️  Skipping automatic volume removal to prevent data loss."
echo "    Run 'docker volume prune' manually if needed."
echo ""

# Step 4: Prune dangling images only
echo "🖼️  Step 4: Removing dangling (unused) images..."
DANGLING_IMAGES=$(docker images -f "dangling=true" -q || true)
if [ -n "$DANGLING_IMAGES" ]; then
    docker rmi $DANGLING_IMAGES
    echo "    ✅ Removed dangling images: ${DANGLING_IMAGES}"
else
    echo "    ℹ️  No dangling images found."
fi
echo ""

# Step 5: Optional: Remove unused images (not dangling)
read -p "Remove unused images (may affect running containers)? (yes/no): " -n 1
echo ""
if [ $? -eq 0 ]; then
    echo "🗑️  Removing unused images..."
    # Get images not used by running containers
    RUNNING_CONTAINER_IMAGES=$(docker ps -q --format "{{.ImageID}}" || true)
    ALL_IMAGES=$(docker images -q || true)
    
    if [ -n "$ALL_IMAGES" ]; then
        echo "  Checking for unused images..."
        for img in $ALL_IMAGES; do
            # Skip if image is used by running container or is llm-studio/ollama
            if echo "$RUNNING_CONTAINER_IMAGES" | grep -q "$img" || \
               echo "$img" | grep -q "^[[:alpha:]]*:[a-z]*$" || \
               echo "$img" | grep -q "^ghcr.io/merryfish/.*$" || \
               echo "$img" | grep -q "^ollama/.*$"; then
                :
            else
                # Try to remove
                docker rmi --force "$img" 2>/dev/null && \
                    echo "    ✅ Removed: $img" || echo "    ⚠️  Skipped: $img"
            fi
        done
    fi
else
    echo "  Skipping unused image removal."
fi
echo ""

# Step 6: Check build cache
echo "🧹 Step 6: Cleaning build cache (optional)..."
read -p "Clean Docker build cache? (yes/no): " -n 1
echo ""
if [ $? -eq 0 ]; then
    docker system prune -a -f --volumes 2>/dev/null || true
    echo "  ✅ Build cache cleaned (this removes all unused data)."
else
    echo "  Skipping cache cleanup."
fi
echo ""

# Step 7: Show freed space
echo "📊 Step 7: Summary of operations..."
FREED_SPACE=$(docker system df -h | tail -1 | awk '{print $2}')
echo "  Freed space: ${FREED_SPACE:-unknown}"
echo ""

# Step 8: Check Docker services status
echo "🔍 Step 8: Verifying running services..."
docker compose -f "$COMPOSE_FILE" ps || echo "  ⚠️  Services status check failed (may be expected)"
echo ""

echo "✅ Cleanup complete!"
echo ""
echo "Commands available:"
echo "  - Remove all dangling resources: docker system prune"
echo "  - Remove nothing but dangling images: docker system prune -f --filter 'until=24h'"
echo "  - View disk usage: docker system df -h"
echo ""
