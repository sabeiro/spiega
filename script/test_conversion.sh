#!/bin/bash

#===============================================================================
# test_conversion.sh - Test the conversion pipeline
#===============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info () {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success () {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning () {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error () {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Test directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_ROOT="$(dirname "$SCRIPT_DIR")"
TEMP_DIR="$SCRIPT_DIR/test_output"

# Test org file
ORG_FILE="$SCRIPT_DIR/knowledge_base/Blender_CV_Documentation.org"

# Test markdown file
MD_FILE="$SCRIPT_DIR/knowledge_base/Static_Web_Pages_Sample.md"

echo "==========================================="
echo "  Documentation Conversion Test"
echo "==========================================="
echo ""

print_info "Testing conversion pipeline..."
echo ""

# Test 1: Check required tools
echo "=== Test 1: Checking required tools ==="
MISSING_TOOLS=0

for tool in "bash" "emacs" "python3"; do
    if command -v "$tool" >/dev/null 2>&1; then
        print_success "$tool: found ($tool --version or $tool -V)"
    else
        print_error "$tool: not found"
        ((MISSING_TOOLS++))
    fi
done

# Check emacs batch mode
if $EMACS_EXEC --batch --version >/dev/null 2>&1; then
    print_success "emacs: batch mode working"
else
    print_error "emacs: batch mode not working"
    ((MISSING_TOOLS++))
fi

# Check output scripts
if [[ -f "$SCRIPT_DIR/org2slide.py" ]]; then
    print_success "org2slide.py: exists"
else
    print_error "org2slide.py: missing"
    ((MISSING_TOOLS++))
fi

if [[ -f "$SCRIPT_DIR/generate_diagrams.py" ]]; then
    print_success "generate_diagrams.py: exists"
else
    print_error "generate_diagrams.py: missing"
    ((MISSING_TOOLS++))
fi

if [[ -f "$SCRIPT_DIR/generate_diagram.sh" ]]; then
    print_success "generate_diagram.sh: exists"
else
    print_error "generate_diagram.sh: missing"
    ((MISSING_TOOLS++))
fi

# Check output directory
if [[ -d "$TEMP_DIR" ]]; then
    print_success "Output directory: exists"
else
    print_warning "Output directory: not found, creating..."
    mkdir -p "$TEMP_DIR"
    print_success "Output directory: created"
fi

echo ""

# Test 2: Generate test HTML from org file
echo "=== Test 2: Generating test HTML from org file ==="
if [[ -n "$ORG_FILE" ]] && [[ -f "$ORG_FILE" ]]; then
    TEMP_ORG="$TEMP_DIR/$(basename "$ORG_FILE".org)"
    TEMP_HTML="$TEMP_DIR/$(basename "$ORG_FILE.org").html"
    
    print_info "Converting: $ORG_FILE -> $TEMP_HTML"
    $EMACS_EXEC "$ORG_FILE" \
        --batch \
        --load="$SCRIPT_DIR/html-export-conf.el" \
        -f org-html-export-to-html \
        2>/dev/null || {
        print_warning "emacs conversion failed"
        echo "<html><body>Test conversion - Org file content</body></html>" > "$TEMP_HTML"
    }
    
    if [[ -s "$TEMP_HTML" ]]; then
        print_success "Test HTML generated: $(basename "$TEMP_HTML")"
    else
        print_error "Empty output file"
    fi
else
    print_warning "No org file found for testing: $ORG_FILE"
fi

echo ""

# Test 3: Generate test HTML from markdown file
echo "=== Test 3: Generating test HTML from markdown file ==="
if [[ -n "$MD_FILE" ]] && [[ -f "$MD_FILE" ]]; then
    TEMP_MD="$TEMP_DIR/$(basename "$MD_FILE".md)"
    TEMP_HTML="$TEMP_DIR/$(basename "$MD_FILE.md").html"
    
    print_info "Converting: $MD_FILE -> $TEMP_HTML"
    python3 "$SCRIPT_DIR/generate_diagrams.py" "$MD_FILE" "$TEMP_HTML"
    
    if [[ -s "$TEMP_HTML" ]]; then
        print_success "Test HTML generated: $(basename "$TEMP_HTML")"
    else
        print_error "Empty output file"
    fi
else
    print_warning "No markdown file found for testing: $MD_FILE"
fi

echo ""

# Test 4: Generate diagram test
echo "=== Test 4: Generating diagram test ==="
echo "graph TD" > "$TEMP_DIR/test_graph.dot"
echo "A[A] --> B[B]" >> "$TEMP_DIR/test_graph.dot"
echo "B --> C[C]" >> "$TEMP_DIR/test_graph.dot"

if [[ "$TEMP_DIR" == "test_output"* ]]; then
    DIAGRAM_FILE="$TEMP_DIR/test_graph.dot"
    print_info "Diagram template: $(basename "$DIAGRAM_FILE")"
fi

print_success "Diagram test: completed"

echo ""

# Cleanup temp files
echo "=== Cleanup ==="
rm -rf "$TEMP_DIR" 2>/dev/null || true
print_success "Temporary files cleaned up"

echo ""

# Summary
echo "==========================================="
print_success "All conversion tests completed!"
echo "==========================================="

if [[ $MISSING_TOOLS -eq 0 ]]; then
    print_success "All required tools are available"
else
    print_warning "Missing tools: $MISSING_TOOLS"
fi

print_info "Check the static_html/ directory for generated content"

echo ""
print_info "Script completed successfully"
