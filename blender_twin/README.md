# Blender Twin Documentation

## Overview

Blender Twin is a project directory for Blender-related development work.

## Directory Structure

```
blender_twin/
├── docs/
│   ├── README.md         # This file
│   ├── text2svg/        # SVG text-to-paths tools
│   │   ├── text2svg.md
│   │   └── text2svg.py
│   └── ...
├── src/
│   ├── blender_twin/
│   │   ├── main.py       # Main entry point
│   │   └── ...
│   └── ...
└── ...
```

## Documentation Tools

This directory contains:

1. **SVG Converter Tools** (`text2svg/`)
   - Pure Python SVG text-to-paths converter
   - No external dependencies
   - See [`text2svg.md`](text2svg.md) for usage

2. **Generated Resources**
   - Icon SVGs
   - Documentation assets
   - Test files

## Usage

### SVG Text to Paths

```bash
python3 text2svg.py input.svg -o output.svg
```

### Running Blender Twin

```bash
python3 src/blender_twin/main.py
```

## See Also

- [text2svg.md](text2svg.md) - SVG converter documentation
- [/home/sabeiro/lav/src/blender_twin/docs/](../../src/blender_twin/docs/) - All docs

## Contact

For questions or issues, please check the source code or documentation.
