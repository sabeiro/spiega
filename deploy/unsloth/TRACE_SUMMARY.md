# Bitmap-to-Vector Trace Summary

## Overview

Created `trace_bitmap_inkscape_style.py` for converting raster maps (PDFs or images) to vector GeoJSON polygons compatible with GIS systems.

## Key Features

- **Tracing Algorithm**: Simplified Inkscape-style bitmap tracing
  - Threshold → Contours → Simplify → Optimize
  - Remove border artifacts and tiny details
- **Area Filtering**: Configurable minimum polygon area
- **Multi-format Support**: PDF, PNG, JPG, JPEG
- **Multiple Extraction Methods**: 
  - `pdf2image` (standard)
  - `qpdf` + `convert` fallback
  - `gs` (Ghostscript) fallback

## Installation

```bash
pip install pdf2image geopandas shapely
# Install pdf2image: pip install pdf2image
```

## Usage

### Command Line

```bash
python trace_bitmap_inkscape_style.py map.pdf 150 50000
```

Arguments:
- PDF/image path
- DPI (default: 150)  
- Min area in pixels (default: 50000, ~2 m²)

### Import and Use

```python
import sys
sys.path.insert(0, 'trace_bitmap_inkscape_style.py')

from trace_bitmap_inkscape_style import trace_bitmap_to_polygons

# Convert to GeoJSON
gdf = trace_bitmap_to_polygons(
    input_path='map.png',
    min_area=50000,  # pixels
    dpi=150,
    simplify_tolerance=5.0
)

# Print results
print(len(gdf), 'polygons extracted')
print(gdf.to_file('output.gjson'))
```

## File List

- `trace_bitmap_inkscape_style.py` - **Main script**
- `README.md` - Documentation
- `test_trace.py` - Test/verification script

## Output Format

GeoJSON with:
- Polygon geometries
- Properties: id, area_px, area_m2
- Ready for QGIS/ArcGIS import

## Technical Notes

- Uses OpenCV + Shapely for contour detection & simplification
- Handles multiple PDF page extraction methods
- Converts area to real-world units based on DPI

## Next Steps

1. Test with sample map files
2. Tune `min_area_threshold` for your maps
3. Batch process multiple files (add loop)
