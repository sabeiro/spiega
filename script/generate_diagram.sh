#!/bin/bash

# Simple diagram extractor - avoids complex heredoc/awk syntax

MARKDOWN_ROOT="${MARKDOWN_ROOT:-./knowledge_base/}"
OUTPUT_FILE="${OUTPUT_FILE:./diag}"

print_info () {
    echo "[INFO] $1"
}

print_success () {
    echo "[SUCCESS] $1"
}

print_warning () {
    echo "[WARNING] $1"
}

print_error () {
    echo "[ERROR] $1" >&2
}

# Parse arguments
MD_FILE=""
DIAGRAM_TYPE="${GRAPHviz:-mermaid}"
while [[ $# -gt 0 ]]; do
    case $1 in
        --diag-file=*)
            OUTPUT_FILE="${1#--diag-file=}"
            shift
            ;;
        --diag-type=*)
            DIAGRAM_TYPE="${1#--diag-type=}"
            shift
            ;;
        --output=*)
            MARKDOWN_ROOT="${1#--output=}"
            shift
            ;;
        -*) 
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            MD_FILE="$1"
            shift
            ;;
    esac
done

if [[ -z "$MD_FILE" ]]; then
    echo "Usage: $0 <markdown_file> [OPTIONS]"
    echo "  --diag-type <type>   mermaid, graphviz, plantuml (default: mermaid)"
    echo "  --diag-file <file>   Output file"
    exit 1
fi

if [[ ! -f "$MD_FILE" ]]; then
    echo "File not found: $MD_FILE"
    exit 1
fi

print_info "Processing: $(basename "$MD_FILE")"

# Extract mermaid diagrams
if grep -q "mermaid" "$MD_FILE" 2>/dev/null; then
    print_info "Found mermaid diagram"
    
    # Extract to temp file
    TMPDIAG=$(mktemp /tmp/diag.XXXXXX)
    grep -A 9999 "```\[|mermaid|" "$MD_FILE" | grep -A 9999 "^[[:space:]]*\`\`\`" | head -200 > "$TMPDIAG"
    mv "$TMPDIAG" "$OUTPUT_FILE" 2>/dev/null || mv "$TMPDIAG" "${OUTPUT_FILE}.diagram" 2>/dev/null
    print_success "Diagram saved"
elif grep -q "^dot " "$MD_FILE" 2>/dev/null; then
    print_info "Found graphviz diagram"
    TMPDIAG=$(mktemp /tmp/diag.XXXXXX)
    grep -A 9999 "```\[|dot|gv|" "$MD_FILE" | head -200 > "$TMPDIAG"
    mv "$TMPDIAG" "${OUTPUT_FILE}.diagram" 2>/dev/null
    print_success "Diagram saved"
else
    print_warning "No diagrams found in: $(basename "$MD_FILE")"
fi

print_info "Done"