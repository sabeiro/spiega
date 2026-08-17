#!/bin/bash
# =============================================================================
# YOLO Pose Estimation - Ansible Deployment Wrapper
# =============================================================================
# Simple wrapper script for common deployment tasks
#
# Usage:
#   ./deploy.sh [command]
#
# Commands:
#   setup       - Full setup (OpenCV, OF, Python, models)
#   python      - Run Python pose detector
#   of          - Build and run OpenFrameworks app
#   build       - Build both apps without running
#   test        - Test connection to Jetson
#   help        - Show this help
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_ansible() {
    if ! command -v ansible-playbook &> /dev/null; then
        log_error "Ansible not installed. Install with: pip install ansible"
        exit 1
    fi
}

show_help() {
    cat << EOF
YOLO Pose Estimation - Ansible Deployment

Usage: ./deploy.sh [command] [options]

Commands:
  setup       Full setup: OpenCV, OpenFrameworks, Python, models
  opencv      Build OpenCV with CUDA only
  python      Setup Python environment and run detector
  of          Build and run OpenFrameworks app
  build       Build both apps without running
  model       Prepare YOLO models only
  test        Test connection to Jetson
  cleanup     Remove build artifacts
  help        Show this help message

Options:
  --check     Dry run (don't make changes)
  --verbose   Verbose output
  --limit     Limit to specific host

Examples:
  ./deploy.sh setup              # Full installation
  ./deploy.sh python             # Run Python detector
  ./deploy.sh of                 # Run OpenFrameworks app
  ./deploy.sh setup --check      # Dry run
  ./deploy.sh build --verbose    # Build with verbose output

EOF
}

run_playbook() {
    local tags="$1"
    shift
    local extra_args="$@"
    
    check_ansible
    
    log_info "Running playbook with tags: $tags"
    ansible-playbook -i inventory.yml playbook.yml --tags "$tags" $extra_args
    
    if [ $? -eq 0 ]; then
        log_success "Playbook completed successfully"
    else
        log_error "Playbook failed"
        exit 1
    fi
}

case "${1:-help}" in
    setup)
        shift
        run_playbook "setup" "$@"
        ;;
    opencv)
        shift
        run_playbook "opencv" "$@"
        ;;
    python)
        shift
        run_playbook "python,run" "$@"
        ;;
    of|openframeworks)
        shift
        run_playbook "openframeworks,run" "$@"
        ;;
    build)
        shift
        run_playbook "openframeworks,build" "$@"
        ;;
    model)
        shift
        run_playbook "model" "$@"
        ;;
    test|ping)
        check_ansible
        log_info "Testing connection to Jetson..."
        ansible jetson -i inventory.yml -m ping
        ;;
    cleanup)
        shift
        run_playbook "cleanup" "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

