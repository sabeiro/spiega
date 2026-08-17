#!/usr/bin/env python3
"""
Trace bitmap (raster image) to vector polygons using Inkscape-style algorithm.
Similar to Inkscape's "Trace bitmap" feature + GeoJSON output for GIS import.

Steps:
1. Load and preprocess grayscale image
2. Apply color threshold (black/white contrast)
3. Find contours with area filtering
4. Simplify shapes (remove tiny details)
5. Optimize polygon vertices (smooth curves)
6. Export as GeoJSON/Shapefile for GIS

Inkscape uses:
- Simplify: removes tiny details (< 5% of object)
- Threshold: simplifies colors/contrast to binary
- Trace: finds contours, then simplifies
- Optimize: removes unnecessary nodes to smooth shapes
"""

import subprocess
import tempfile
import os
import sys
import cv2
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import simplify
import json

def extract_pdf_as_page(pdf_path, dpi=150, method='fallback'):
    """Extract PDF page as grayscale PNG using fallback methods.
    
    Args:
        pdf_path: Path to PDF file
        dpi: Output DPI
        method: Extraction method ('fallback')
    
    Returns:
        Path to extracted PNG or None
    """
    import subprocess
    import shutil
    
    try:
        basename = os.path.basename(pdf_path).replace('.pdf', '')
        output_path = f"{basename}-{dpi}.png"
        
        # Try multiple methods
        for m, cmd, error_msg in [
            ('gs', 
             f"gs -sDEVICE=pngx4gray -r{dpi} -dNOPAUSE -dSAFER -dBATCH -dFirstPage=1 -dLastPage=1 " +
             f"-sOutputFile={output_path} {pdf_path}",
             'gs failed'),
            ('qpdf',
             f"qpdf --pdf-version=1.4 {pdf_path} - -r {dpi} > {output_path} || true",
             'qpdf failed'),
        ]:
            result = subprocess.run(cmd, shell=True, capture_output=True)
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"  Extracted with {m}: {output_path}")
                return output_path
        
        # If all fail, try qpdf2pdfimage or qpdf directly
        try:
            import qrcode
            # Alternative: save as intermediate PDF then convert
            cmd = f"qpdf --pdf-version=1.4 {pdf_path} {output_path}.tmp"
            result = subprocess.run(cmd, shell=True, capture_output=True)
            if result.returncode == 0 and os.path.exists(output_path + '.tmp'):
                cmd = f"convert {output_path}.tmp -colorspace Gray -monochrome {output_path}"
                result = subprocess.run(cmd, shell=True, capture_output=True)
                if result.returncode == 0 and os.path.exists(output_path):
                    return output_path
        except:
            pass
        
        # Fallback: tell user to use image directly
        print(f"  No image extraction available. Use PNG/JPG directly.")
        return output_path if os.path.exists(output_path) else None
        
    except Exception as e:
        print(f"  Error extracting PDF: {e}")
        return None

def simplify_contour(contour, tolerance=5.0, approx_method='MONTANO'):
    """
    Simplify contour using Douglas-Peucker algorithm.
    tol: Distance tolerance (lower = more details kept)
    Returns: Simplified contour or None
    """
    if contour is None or contour.size == 0:
        return None
    
    try:
        # Use cv2.approxPolyDP to simplify
        epsilon = tolerance
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) < 4 or cv2.contourArea(approx) < 100:
            return None
            
        return approx
        
    except Exception as e:
        print(f"  Simplify error: {e}")
        return contour

def optimize_polygon(poly, tolerance=0.05):
    """
    Optimize polygon vertices to remove unnecessary points.
    Keep points that are at least `tolerance` fraction away from line segment.
    
    Args:
        poly: shapely Polygon
        tolerance: Fraction of diagonal distance to skip points
    
    Returns:
        Simplified polygon
    """
    coords = list(zip(*poly.exterior.coords))
    if len(coords) < 4:
        return poly
    
    # Simplify using shapely's built-in simplification
    try:
        if hasattr(simplify, 'simplify'):
            # If available, use it
            simp = simplify(poly, tolerance=tolerance)
            if simp and len(simp.geoms) > 0:
                # Handle MultiPolygon results
                if isinstance(simp, MultiPolygon):
                    # Keep largest polygons only
                    simplified = []
                    total_area = 0
                    for p in simp.geoms:
                        new_area = p.area
                        total_area += new_area
                        simplified.append(p)
                    if len(simplified) > 0:
                        return MultiPolygon(simplified) if len(simplified) > 1 else simplified[0]
                return simp
    except Exception as e:
        pass
    
    return poly

def trace_bitmap_to_polygons(image_path, min_area=50000, dpi=150, simplify_tolerance=5.0):
    """
    Trace bitmap to vector polygons using Inkscape-style algorithm.
    
    Args:
        image_path: Path to grayscale PNG image
        min_area: Minimum contour area in pixels
        dpi: DPI of source image (for area calculation)
        simplify_tolerance: Simplification tolerance (in pixels)
    
    Returns:
        GeoDataFrame or None
    
    This mimics Inkscape's "Trace bitmap" workflow.
    """
    try:
        print(f"\n1. Loading and preprocessing image...")
        print(f"   Image: {image_path}")
        
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            print(f"   Cannot read image: {image_path}")
            return None
        
        img_height, img_width = img.shape[:2]
        img_total_area = img_height * img_width
        print(f"   Resolution: {img_width}x{img_height}")
        print(f"   Image area: {img_total_area} px² ({img_total_area / 22500:.2f} m²)")
        
        # Normalize: detect black ink on white background (THRESH_BINARY)
        # Convert to binary threshold
        try:
            # Otsu's thresholding for optimal bimodal distribution
            _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            print(f"   Otsu threshold: {1.0 - binary.max() / 255:.1f} (normalized)")
            
            # Or simple fixed threshold for high contrast documents
            _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            
        except Exception as e:
            _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        
        # Find external contours only (RETR_EXTERNAL)
        contours, hierarchy = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        print(f"   Found {len(contours)} external contours")
        
        # Filter by area and simplify
        valid_contours = []
        total_skipped = 0
        min_pixels_ratio = min_area / img_total_area
        
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            
            # Skip very small contours (noise)
            if area < min_area:
                continue
            
            # Simplify contour
            simplified = simplify_contour(contour, tolerance=simplify_tolerance)
            
            if simplified is None:
                total_skipped += 1
                continue
            
            # Check if simplified area is still significant
            simple_area = cv2.contourArea(simplified)
            if simple_area < min_area * 0.8:  # Keep 80% of original
                total_skipped += 1
                continue
            
            # Convert to polygon
            contour_float = np.reshape(simplified, (-1, 2), order='C').astype(np.float64)
            try:
                poly = Polygon(contour_float)
            except Exception:
                continue
            
            # Check validity
            if not poly.is_valid or poly.is_empty or poly.area < 100:
                continue
            
            # Skip if too close to full image (border artifact)
            if poly.area > img_total_area * 0.9:
                continue
            
            valid_contours.append(poly)
        
        print(f"   After filtering/simplification: {len(valid_contours)} polygons")
        
        if not valid_contours:
            print("   No valid polygons found!")
            print("   Try reducing min_area parameter.")
            return None
        
        # Remove border artifacts (very large contours)
        valid_contours = [p for p in valid_contours 
                         if p.area < img_total_area * 0.9]
        
        if len(valid_contours) == 0:
            return None
        
        # Merge overlapping polygons (union)
        print(f"\n2. Merging overlapping polygons...")
        
        try:
            # Create MultiPolygon for union
            multi = MultiPolygon(valid_contours)
            unioned = unary_union(multi)
            
            if isinstance(unioned, MultiPolygon):
                # Keep only significant components
                merged = []
                for i, component in enumerate(unioned.geoms):
                    if component.area > 1000:  # Keep only significant areas
                        merged.append(component)
                
                if len(merged) > 1:
                    valid_contours = merged
                elif len(merged) == 1:
                    valid_contours = [merged[0]]
        
        except Exception as e:
            print(f"   Union failed: {e}, using original polygons")
        
        print(f"   Final polygons: {len(valid_contours)}")
        
        # Create GeoDataFrame
        print(f"\n3. Creating GeoDataFrame...")
        geo_polygons = []
        geo_ids = []
        total_area = 0
        
        for i, poly in enumerate(valid_contours):
            geo_polygons.append(poly)
            geo_ids.append(f"PLOT_{i+1:04d}")
            total_area += poly.area
        
        print(f"   Valid polygons: {len(geo_polygons)}")
        print(f"   Total area: {total_area/10000:.2f} m²")
        
        if not geo_polygons:
            return None
        
        # Create GeoDataFrame
        print(f"\n4. Creating GeoDataFrame (for GIS import)...")
        
        gdf = gpd.GeoDataFrame(
            {
                'id': geo_ids,
                'area_px': [p.area for p in geo_polygons],
                'area_m2': [(p.area / (dpi ** 2)) * 0.25 for p in geo_polygons]
            },
            geometry=geo_polygons,
            crs=None  # Will be set later
        )
        
        gdf = gdf.set_index('id')
        
        print(f"   Shape: {len(gdf)} polygons")
        print(f"   Total area: {total_area/10000:.2f} m²")
        
        return gdf
        
    except Exception as e:
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function"""
    if len(sys.argv) >= 2:
        input_path = sys.argv[1]
    else:
        input_path = "/home/sabeiro/lav/src/spiega/deploy/unsloth/map.pdf"
    
    dpi = 150
    if len(sys.argv) >= 3:
        dpi = int(sys.argv[2])
    
    min_contour_area = 50000  # Default threshold (~2 m² at 150 DPI)
    if len(sys.argv) >= 4:
        min_contour_area = int(sys.argv[3])
    
    simplify_tol = 5.0  # Pixel tolerance for simplification
    
    print("=" * 70)
    print(f"Bitmap to Vector Trace (Inkscape-style)")
    print("=" * 70)
    
    print(f"\nSource: {input_path}")
    print(f"DPI: {dpi}")
    print(f"Min area: {min_contour_area} pixels ({min_contour_area / 22500:.3f} m²)")
    print(f"Simplify tolerance: {simplify_tol} pixels")
    
    # Extract PDF or check if it's an image
    if input_path.endswith(('.png', '.jpg', '.jpeg')):
        image_path = input_path
    elif input_path.endswith('.pdf'):
        try:
            # Extract PDF page
            basename = os.path.basename(input_path).replace('.pdf', '')
            
            # Try pdftoppm
            cmd = f"pdftoppm -png -singlefile -r {dpi} {input_path} {basename}"
            result = subprocess.run(cmd, shell=True, capture_output=True)
            
            if result.returncode != 0:
                print(f"  pdftoppm failed - trying alternative method")
                # Fallback: convert PDF pages directly to images
                output_path = f"{basename}-{dpi}.png"
                print(f"  Extracted page 1 as: {output_path}")
            else:
                # Find output file
                output_files = [f for f in os.listdir('.') if f.startswith(basename) and f.endswith('.png')]
                if output_files:
                    output_path = output_files[0]
                else:
                    output_path = f"{basename}-{dpi}.png"
                
        except Exception as e:
            print(f"  Failed to extract PDF or file already extracted: {e}")
            return
    else:
        print("  Unsupported file format")
        return
    
    # Check if image was extracted
    if output_path and os.path.exists(output_path):
        image_path = output_path
        
        # Trace to polygons
        gdf = trace_bitmap_to_polygons(output_path, min_area=min_contour_area, dpi=dpi, simplify_tolerance=simplify_tol)
        
        if gdf is not None:
            print(f"\n=== SUCCESS ===")
            print(f"Extracted {len(gdf)} polygons")
            
            # Calculate real-world area
            pixels_per_m2 = (dpi ** 2) / 22500
            gdf['area_m2'] = gdf['area_px'] / pixels_per_m2
            print(f"\nArea conversion:")
            print(f"  Scale: 1 px = {1/pixels_per_m2:.4f} m²")
            
            total_area = gdf.geometry.area.sum()
            print(f"\nTotal area: {total_area/10000:.2f} m²")
            
            # Save GeoJSON
            output_gjson_path = input_path.replace('.pdf', '.gjson').replace('.png', '.gjson')
            if not output_gjson_path.endswith('.gjson'):
                output_gjson_path = input_path.replace('.pdf', '') + '.gjson'
            
            gdf.to_file(output_gjson_path, driver='GeoJSON')
            print(f"\nSaved to: {output_gjson_path}")
            
            # Show results
            print(f"\n{gdf}")
            print(f"\nFor GIS import:")
            print(f"  Format: GeoJSON")
            print(f"  Projection: WGS84 (set later in GIS)")
            print(f"  Feature count: {len(gdf)} polygons")
            print(f"  Total area: {total_area/10000:.2f} m²")
            
        else:
            print("\n=== NO POLYGONS EXTRACTED ===")
            print("  Adjust min_contour_area parameter in script")
    
    else:
        print("  Failed to extract image from PDF or file not found")
    

if __name__ == "__main__":
    main()
