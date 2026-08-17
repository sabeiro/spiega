#!/bin/bash
# Wrapper script to run the Blender MCP tools for pi-coding-agent
# Usage: blender_mcp_wrapper.sh [command] [args]
#
# Available commands:
#   start  - Start the MCP server
#   list   - List available tools
#   help   - Show help

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PYTHON_SCRIPT="${SCRIPT_DIR}/blender_mcp_tool.py"

case "${1:-start}" in
    start)
        exec python3 -m ${PYTHON_SCRIPT} "$@"
        ;;
    list)
        echo "Available Blender MCP tools:"
        echo "  1. add_cube     - Add a cube to the scene"
        echo "  2. add_sphere   - Add a sphere object"
        echo "  3. add_plane    - Add a plane surface"
        echo "  4. list_objects - List all objects in the scene"
        echo "  5. add_material - Add a new material to the shader"
        echo "  ..."
        ;;
    help)
        echo "Blender MCP Tool Wrapper"
        echo "Usage: $0 [start|list|help]"
        echo ""
        echo "Commands:"
        echo "  start  - Start the MCP server (default)"
        echo "  list   - List available tools"
        echo "  help   - Show this help"
        ;;
    *)
        python3 -m ${PYTHON_SCRIPT} "$@"
        ;;
esac
