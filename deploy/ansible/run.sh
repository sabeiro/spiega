#!/usr/bin/env bash
# Run Ansible playbook for webui Docker Compose operations.
# Usage:
#   ./run.sh rebuild [service] [--no-cache]
#   ./run.sh restart [service]
#   ./run.sh start [service]
#   ./run.sh stop [service]
#   ./run.sh logs [service] [--tail N] [--follow]
#   ./run.sh test
#   ./run.sh vision            # fetch screenshot + describe_vision to vision_output/ for YOLO vs human comparison
# Examples:
#   ./run.sh rebuild mcp
#   ./run.sh restart nginx     # restart nginx and test https://ollama.jetson/mcp/api/screenshot
#   ./run.sh test              # test API endpoints only (no restart)
#   ./run.sh vision            # saves vision_output/screenshot.png and describe_vision.txt
#   ./run.sh logs mcp --tail 500
#   ./run.sh logs mcp --follow

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

INVENTORY="inventory.yml"
PLAYBOOK="playbook.yml"

ACTION="${1:?Usage: $0 rebuild|restart|start|stop|logs|test|vision [service] [options]}"
# Accept "build" as alias for "rebuild"
[[ "$ACTION" == "build" ]] && ACTION=rebuild
shift || true
SERVICE=""
NO_CACHE="false"
LOGS_TAIL="200"
LOGS_FOLLOW="false"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-cache)
      NO_CACHE="true"
      shift
      ;;
    --tail)
      LOGS_TAIL="$2"
      shift 2
      ;;
    --follow)
      LOGS_FOLLOW="true"
      shift
      ;;
    nginx|ollama|mcp)
      SERVICE="$1"
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

EXTRA_VARS=(-e "action=$ACTION")
[[ -n "$SERVICE" ]] && EXTRA_VARS+=(-e "service=$SERVICE")
[[ "$ACTION" == "rebuild" && "$NO_CACHE" == "true" ]] && EXTRA_VARS+=(-e "no_cache=true")
[[ "$ACTION" == "logs" ]] && EXTRA_VARS+=(-e "logs_tail=$LOGS_TAIL" -e "logs_follow=$LOGS_FOLLOW")

ansible-playbook -i "$INVENTORY" "$PLAYBOOK" "${EXTRA_VARS[@]}"
