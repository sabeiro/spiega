# Documentation Conversion System - Complete ✓

## Overview

The documentation conversion pipeline is now complete with all necessary scripts and supporting files. This system converts org-mode and markdown files to static HTML pages with professional styling and diagram support.

## File Structure

```
docs/
├── script/
│   ├── convert_md.sh           # Main conversion script
│   ├── org2slide.py            # Org file to HTML slides converter
│   ├── generate_diagrams.py    # Generate diagrams from markdown
│   ├── generate_diagram.sh     # Shell script for diagram generation
│   ├── generate_diagram_*.py   # Diagram generators for different formats
│   └── test_conversion.sh      # Test script for validation
├── static_html/                # Generated HTML output directory
└── knowledge_base/             # Source documentation files
    ├── Blender_CV_Documentation.org
    └── Static_Web_Pages_Sample.md
```

## Usage

### Convert Org Files to HTML

```bash
# Export org files with emacs
emacs <file>.org --batch --load=script/html-export-conf.el \
  -f org-html-export-to-html

# Copy to output
cp <temp_file> static_html/$(basename <file>.html)

# Generate slides
python3 script/org2slide.py static_html/<file>.html static_html/<file>_slideshow.html
```

### Convert Markdown Files to HTML

```bash
# Generate diagrams for markdown file
bash script/generate_diagram.sh <file>.md <output>.html

# Convert simple markdown
python3 script/generate_diagrams.py <file>.md <output>.html
```

### Process Multiple Files

```bash
# Convert org directory
./convert_md.sh -p <plan_name> -o static_html/
bash ./convert_md.sh ./script/org2slide.py

# Convert markdown with diagrams
bash convert_md.sh ./script/generate_diagrams.py
```

## Generated Assets

The following assets are generated:

1. **Static HTML files** from org exports
2. **Slide presentations** from org files
3. **Diagram templates** (mermaid/graphviz/plantuml)
4. **Combined HTML documents** for markdown files

## Testing

Run the test script to validate the setup:

```bash
bash script/test_conversion.sh
```

This will:
- Check all required tools are available
- Test org file conversion
- Test markdown file conversion
- Verify diagram generation
- Clean up temporary files

## Next Steps

1. **Add source files** to `knowledge_base/`
2. **Build documentation** using `convert_md.sh`
3. **Review generated HTML** in `static_html/`
4. **Iterate** on org file structure and styles
5. **Export** to static web directory when ready

## Notes

- The system generates self-contained HTML files
- CSS/styles are embedded for portability
- Diagrams are extracted and included
- Conversion preserves formatting from source files

## Authoring Guidelines

1. **For org files**:
   - Use `#+STARTUP:` for emacs configuration
   - Export with emacs to static files
   - Run org2slide.py for slide generation

2. **For markdown files**:
   - Use code blocks for diagrams
   - Include mermaid/graphviz syntax
   - Convert with generate_diagrams.py

3. **Styling**:
   - Use CSS classes: `slide`, `slide-title`, `slide-content`
   - Customize via style.css
   - Use variables in theme files

## Support

For issues or questions:
- Check the `test_conversion.sh` script
- Review generated files in `static_html/`
- Examine source files in `knowledge_base/`

---

**Status**: All conversion scripts complete
**Date**: $(date +%Y-%m-%d)
**Test**: Pending (run test_conversion.sh)