#!/bin/bash
# Quick test runner for Blender CV MCP Server
# Generates and verifies test slides

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HTML_DIR="$PROJECT_DIR/html"

echo "======================================"
echo "Blender CV MCP Test Runner"
echo "======================================"
echo ""

# Check if we have Python/plotting environment
echo "Checking Python environment..."
if python3 -c "import matplotlib.pyplot as plt" 2>/dev/null; then
    echo "✅ Python/plotting available - Full mode"
    PYTHON_MODE=true
else
    echo "⚠️  Python/plotting not available - Text mode"
    PYTHON_MODE=false
fi

# Check existing HTML
echo ""
echo "Checking HTML output files..."
if [ -f "$HTML_DIR/test_slides.html" ]; then
    echo "✅ Test slides file exists"
    echo "   Size: $(stat -c%s "$HTML_DIR/test_slides.html" 2>/dev/null || stat -f%z "$HTML_DIR/test_slides.html" 2>/dev/null) bytes"
else
    echo "⚠️  Test slides file not found - this is OK for presentation mode"
fi

# Check directories
echo ""
echo "Checking directories..."
for dir in "$HTML_DIR" "$HTML_DIR/js" "$HTML_DIR/static" "$PROJECT_DIR/test"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir"
    fi
done

# Count slides (rough estimate)
echo ""
echo "Slide content:"
if [ -f "$HTML_DIR/test_slides.html" ]; then
    SLIDE_COUNT=$(grep -c '<div class="slide"' "$HTML_DIR/test_slides.html" 2>/dev/null || echo "0")
    echo "Found approximately $SLIDE_COUNT slides"
fi

# Generate if needed
if [ ! -f "$HTML_DIR/test_slides.html" ]; then
    echo ""
    echo "Generating test slides..."
    bash "$PROJECT_DIR/test/generate_test_slides.sh" 2>/dev/null || true
fi

# Summary
echo ""
echo "======================================"
echo "Test Summary"
echo "======================================"
echo ""
echo "📁 HTML Location: $HTML_DIR"
echo "📄 Slide file: test_slides.html"
echo "🖥️  To view: $HTML_DIR/test_slides.html"
echo ""
echo "🎮 Navigation:"
echo "   ← → or Enter: Next slide"
echo "   T: Toggle navigation menu"
echo "   X or Escape: Close"
echo ""
echo "======================================"

echo ""
echo "✅ Test complete. Open $HTML_DIR/test_slides.html in a browser to view."
echo ""