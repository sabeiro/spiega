# Bitmap-to-Vector Trace for GIS

Convert PDF or image maps to vector GeoJSON using Inkscape-style tracing algorithm.

## Workflow

1. **Extract** PDF page as grayscale PNG
2. **Trace** bitmap to vectors (Inkscape algorithm)
   - Simplify contours (< 5% details removed)
   - Optimize polygon vertices
   - Remove border artifacts
3. **Export** as GeoJSON for GIS import

## Available Scripts

- `trace_bitmap_inkscape_style.py` - Main tracing script
- `trace_pdf_bitmap.py` - Simpler OpenCV-only version
- `trace_clean.py` - Post-processing utility

## Installation

```bash
pip install pdf2image geopandas shapely
```

PDF tools must be installed system-wide:
- `pdftoppm`
- `pdftocairo`
- `pdftohtml`

## Usage

```bash
# Convert PDF to GeoJSON
python trace_bitmap_inkscape_style.py map.pdf 150 50000

# Arguments:
#   1. PDF or image path
#   2. DPI (default: 150)
#   3. Min area in pixels (default: 50000)
```

## Output

Produces:
- `filename.gjson` - GeoJSON file with polygon geometries
- Each polygon has properties: id, area_px, area_m2

## For GIS

The GeoJSON can be directly imported into:
- QGIS
- ArcGIS
- PostGIS
- Leaflet/Mapbox

Set CRS to WGS84 (EPSG:4326) or appropriate coordinate system.
