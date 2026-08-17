#!/bin/bash
# Publish agent_call.org as HTML using emacs html-export configuration
# Usage: ./publish_agent_call_org.sh
# Outputs: ../html/agent_call.html from ../agent_call.org
# Runs inside Docker container where emacs is available

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORG_FILE="${SCRIPT_DIR}/../agent_call.org"
HTML_DIR="${SCRIPT_DIR}/../html/"
EMACS_EXEC="emacs"
EMACS_CONF="${SCRIPT_DIR}/../emacs/html-export-conf.el"
OUTPUT_FILE="${HTML_DIR}agent_call.html"

# Check if required files exist
if [ ! -f "$ORG_FILE" ]; then
    echo "ERROR: Org file not found: $ORG_FILE"
    exit 1
fi

if [ ! -f "$EMACS_CONF" ]; then
    echo "ERROR: Emacs config not found: $EMACS_CONF"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$HTML_DIR"

# Export org to HTML using emacs (runs in Docker container)
echo "Converting org file to HTML..."
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting Org to HTML conversion" | tee -a "${HTML_DIR}/.export_log"

# Verify Emacs is available (it should be in the Docker image)
if command -v "$EMACS_EXEC" >/dev/null 2>&1; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Emacs found, proceeding with conversion" | tee -a "${HTML_DIR}/.export_log"

    # Export org to HTML using emacs
    "$EMACS_EXEC" "$ORG_FILE" --batch --load "$EMACS_CONF" -f org-html-export-to-html --kill
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: Emacs not found in container" | tee -a "${HTML_DIR}/.export_log"
    echo "Installing or updating Emacs in container with: apt-get update && apt-get install -y emacs"
    exit 1
fi

# Check if output was created
if [ -f "$OUTPUT_FILE" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Success: HTML file created: $(basename "$OUTPUT_FILE")" | tee -a "${HTML_DIR}/.export_log"
    echo "File: $OUTPUT_FILE" | tee -a "${HTML_DIR}/.export_log"
    echo "Size: $(du -h "$OUTPUT_FILE" | cut -f1)" | tee -a "${HTML_DIR}/.export_log"
    echo "Lines: $(wc -l < "$OUTPUT_FILE")" | tee -a "${HTML_DIR}/.export_log"
    echo "Conversion complete successfully."
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: HTML file was not created: $OUTPUT_FILE" | tee -a "${HTML_DIR}/.export_log"
    exit 1
fi
