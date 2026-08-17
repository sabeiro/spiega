# Test Utilities for Blender CV MCP Server

This directory contains test utilities and scripts for testing the Blender CV MCP Server configurations.

## Test Files

### 1. Test HTML Files

**test_slides.html** - Main output test slide show

### 2. Test Scripts

**generate_test_slides.sh** - Bash script to generate test slide HTML
- Uses Python if available for code examples
- Creates static HTML with navigation controls

**test_*.sh** - Various connection and environment tests

### 3. Python Utilities

**parse_org_to_html.py** - Parse OrgMode files to generate HTML

## Running Tests

```bash
# Generate test slides
cd /home/sabeiro/lav/src/blender_cv/mcp_server/test
bash generate_test_slides.sh

# Or run individual tests
bash test_connection.sh          # Test Python/ML libraries
bash test_network.sh             # Test network connectivity
bash test_cuda.sh                # Test GPU availability
```

## Environment Testing

The slide show works in two modes:

1. **With Python ML Environment** (ideal)
   - Can display Python code examples
   - Can generate plots inline
   - Full visualization capabilities

2. **Without Python ML Environment** (fallback)
   - Text-based content
   - Still fully functional navigation
   - Works on any system (even without Python)

## Testing Workflow

1. **Generate test slides:**
   ```bash
   bash test_slides.sh
   ```

2. **Find generated HTML:**
   ```bash
   find . -name "*.html" -path "*/html/*"
   ```

3. **Open in browser:**
   ```bash
   xdg-open html/test_slides.html
   # Or on macOS:
   open html/test_slides.html
   # Or on Windows:
   start html\test_slides.html
   ```

4. **Test navigation:**
   - Press ← → arrows or Enter
   - Press X to close
   - Press T for navigation menu

## Requirements

See requirements.txt for Python environment needs.

The slide show works without Python - just a simple HTML file!

## Output Location

Test HTML files are generated in:
- `html/test_slides.html` (main test slide show)
- `html/` subdirectory

## Debugging

If slides don't load properly:

1. Check browser console (F12)
2. Verify CSS loads: `html/static/style.css`
3. Verify JavaScript: `html/js/script.js`

Try opening the HTML file directly:
```bash
# On Linux
firefox html/test_slides.html

# On macOS/Safari
open html/test_slides.html
```

## Tips

- Press **?** for help
- Press **T** for navigation menu
- Press **X** or **Escape** to close
- Enable auto-slide via the toggle button