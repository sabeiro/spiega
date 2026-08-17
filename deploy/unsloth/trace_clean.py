"""
Trace bitmap map from PDF to vector polygons using pdftoppm + OpenCV.

Usage:
    python trace_pdf_bitmap.py <pdf_path> [dpi] [min_area]
    or
    python trace_pdf_bitmap.py <map_path>   (if already PNG)

Dependencies:
    - pdftoppm (from poppler-utils) - for PDF to image
    - convert / identify (ImageMagick) - for image conversion
    - Python + OpenCV + geopandas + shapely

Example:
    # From PDF (default 150 DPI)
    python trace_pdf_bitmap.py /path/to/map.pdf

    # From PNG (default 150 DPI, min area 200000 pixels2)
    python trace_pdf_bitmap.py /path/to/map.png

    # Custom DPI and area
    python trace_pdf_bitmap.py /path/to/map.pdf 300 200000
"""

import subprocess
import tempfile
import os
import sys
import cv2
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon


def extract_pdf_as_image(pdf_path, dpi=150):
    """Extract first page of PDF as grayscale PNG using pdftoppm"""
    try:
        pdf_path = os.path.abspath(pdf_path)
        basename = os.path.basename(pdf_path).replace('.pdf', '')

        # Use pdftoppm to extract PNG (monochrome)
        # -singlefile: write only the first page
        cmd = f"pdftoppm -png -singlefile -r {dpi} {pdf_path} {basename}"

        result = subprocess.run(cmd, shell=True, capture_output=True)

        if result.returncode != 0:
            print(f"  pdftoppm error: {result.stderr.decode() or 'unknown error'}")
            return None

        # Look for output files
        output_path = f"{basename}-1{dpi}.png"

        if not os.path.exists(output_path):
            # Maybe singlefile didn't work, try without
            output_path = f"{basename}-1.png"

        if not os.path.exists(output_path):
            print(f"  Error: Image not found in:")
            for p in [f"{basename}-1.png", f"{basename}-1{dpi}.png", f"{basename}.png"]:
                if os.path.exists(p):
                    print(f"    Found: {p} <- using this instead")
                    output_path = p
                    break
            else:
                print(f"    None found")
                return None

        print(f"  Extracted: {output_path}")
        return output_path

    except Exception as e:
        print(f"  Error: {e}")
        return None


def detect_image_brightness(image_path):
    """Detect if foreground is dark or light (for adaptive threshold)"""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    # Check pixel statistics
    mean_val = np.mean(img)
    min_val, max_val = img.min(), img.max()

    # Background is white (255) if dark polygons: mean < 100
    # Background is dark (0) if white polygons: mean > 200
    if mean_val < 100:
        print(f"  Dark foreground on light background (mean={mean_val:.1f})")
        return 'light'  # Use THRESH_BINARY_INV
    elif mean_val > 200:
        print(f"  Light foreground on dark background (mean={mean_val:.1f})")
        return 'dark'  # Use THRESH_BINARY
    else:
        print(f"  Mixed content (mean={mean_val:.1f})")
        return 'mixed'


def trace_bitmap_to_polygons(image_path, min_contour_area=200000, target_area_m2=None):

        total_area = 0
        for i, contour in enumerate(valid_contours):
            contour = contour.reshape((-1, 2)).astype(np.float64)
            try:
                poly = Polygon(contour)
                poly_contour = cv2.contourArea(contour)
                poly_shapely = poly

                if poly_shapely.is_valid and not poly.is_empty and Polygon.contour_area(contour) > 100:
                    # Skip if polygon is extremely large (likely the whole image)
                    max_area = img.shape[0] * img.shape[1]
                    if Polygon.contour_area(contour) < max_area * 0.99:  # Not nearly the whole image
                        geo_polygons.append(poly)
                        geo_ids.append(f"POLY_{i+1:04d}")
                        total_area += Polygon.contour_area(contour)

            except Exception as e:
                continue  # Skip contours with geometry errors

        print(f"   Valid polygons: {len(geo_polygons)}")

        if not geo_polygons:
            return None

    except Exception as e:
        print(f"   Error: {e}")
        return None

    # Create GeoDataFrame
    print(f"\n3. Creating GeoDataFrame...")
    print(f"   Shape: {len(geo_polygons)} polygons")
    if geo_polygons:
        print(f"   Avg area: {total_area/len(geo_polygons):.2f} pixels2")

    gdf = gpd.GeoDataFrame(
        {'id': geo_ids, 'geometry': geo_polygons},
        crs=None
    )
    print(f"   Schema:\n{gdf.dtypes}")
    print(f"   Total area: {total_area/10000:.2f} m2")

    return gdf


def main():
    """Main function"""
    if len(sys.argv) >= 2:
        pdf_path = sys.argv[1]
    else:
        # Default from context
        pdf_path = "/home/sabeiro/lav/src/spiega/deploy/unsloth/map.pdf"

    dpi = 150
    if len(sys.argv) >= 3:
        dpi = int(sys.argv[2])

    min_contour_area = 50000  # Default: 0.22 m2

    if len(sys.argv) >= 4:
        min_contour_area = int(sys.argv[3])

    print("=" * 60)
    print(f"PDF Trace to Vector Polygons (pdftoppm + OpenCV)")
    print("=" * 60)

    print(f"\nSource: {pdf_path}")
    print(f"DPI: {dpi}")
    print(f"Min area: {min_contour_area} pixels ({min_contour_area/22500:.3f} m2)")

    # Extract PDF as image
    print("\n1. Extracting PDF page...")
    image_path = extract_pdf_as_image(pdf_path, dpi=dpi)

    if image_path is None:
        print("   Failed to extract image")
        return

    # Trace to polygons
    gdf = trace_bitmap_to_polygons(image_path, min_contour_area=min_contour_area)

    if gdf is not None:
        print(f"\n=== SUCCESS ===")
        print(f"Extracted {len(gdf)} polygons")
        print(f"\n{gdf}")
        print(f"\nTotal area: {gdf.geometry.area.sum()/10000:.2f} m²")
        
        # Save GeoJSON
        output_gjson_path = pdf_path.replace('.pdf', '.gjson').replace('.png', '.gjson')
        gdf.to_file(output_gjson_path, driver='GeoJSON')
        print(f"\nSaved to: {output_gjson_path}")
        
    else:
        print("\n=== NO POLYGONS EXTRACTED ===")
        print("  Adjust min_contour_area parameter in script")


if __name__ == "__main__":
    main()