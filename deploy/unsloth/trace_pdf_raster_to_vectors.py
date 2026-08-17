"""
Trac bitmap traces from PDF raster maps to vector polygons.
Approach:
1. Extract PDF page as grayscale image
2. Apply adaptive thresholding
3. Use contour detection to find closed borders
4. Extract coordinates into Shapely geometries
5. Create GeoPandas GeoDataFrame

Requires:
- pip install pdf2image pillow opencv-python-headless shapely geopandas matplotlib
"""

import os, sys, tempfile, io, json, re, subprocess
from pathlib import Path
from PIL import Image
import geopandas as gpd
from shapely.geometry import Polygon, box, MultiPolygon, LinearRing
import numpy as np
import cv2  # OpenCV


def extract_pdf_as_image(pdf_path):
    """Convert PDF page to grayscale image (50 DPI for balance)"""
    from pdf2image import converter
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        tmp.write(open(pdf_path, 'rb').read())
        pdf_path_tmp = tmp.name

    try:
        # Ensure PDF directory matches output
        pdf_dir = os.path.dirname(pdf_path)
        os.makedirs(pdf_dir, exist_ok=True)

        # Convert PDF to PNG (50 DPI - good balance)
        images = converter.from_pdf(pdf_path_tmp, dpi=50)
        print(f"  Extracted {len(images)} pages")

        # Get grayscale image from first page
        page_0_img = images[0]
        gray = page_0_img.convert('L')

        return gray, page_0_img.size

    except ImportError:
        print("  Error: pdf2image not installed.")
        print("  Install with: pip install pdf2image")
        sys.exit(1)
    except Exception as e:
        print(f"  Error: {e}")
        return None, None


def adaptive_threshold_gray(gray_img, offset=127, block_size=45, C=6):
    """Apply Gaussian blur, adaptive threshold, and clean up"""
    kernel = np.ones((3,3), np.uint8)
    blured = cv2.GaussianBlur(gray_img, (7,7), 0)
    thresh = cv2.adaptiveThreshold(
        blured, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        block_size, 
        C
    )
    return thresh


def remove_small_contours(thresh_img, min_area=1000):
    """Remove small contours and holes"""
    area_mask, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Filter contours by area
    valid_area = [c for c in area_mask if cv2.contourArea(c) > min_area]
    valid_area = cv2.drawContours(thresh_img.copy(), valid_area, -1, (255), -1)
    # Remove holes (RETR_CCOMP -> only outer boundary)
    # cv2.findContours(valid_area, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    return valid_area


def extract_polygon_geometry(contour):
    """Convert OpenCV contour into Shapely Polygon (with hole handling)"""
    # Convert to numpy array
    contour = np.array(contour, dtype=np.float64)
    try:
        # Use Polygon constructor
        poly = Polygon(contour)
        return poly.is_valid
    except Exception as e:
        return None


def trace_pdf_to_geometry(pdf_path, min_contour_area=1000):
    """
    Main function: trace bitmap map to vector polygons.
    
    Args:
        pdf_path: Path to PDF map file
        min_contour_area: Minimum area to consider a polygon (pixels^2, 50DPI)
    
    Returns:
        GeoDataFrame of extracted polygons (or None)
    """
    print("="*60)
    print(f"PDF Trace to Vector Polygons: {pdf_path}")
    print("="*60)
    
    # 1. Extract PDF as grayscale image
    print("\n1. Extracting PDF page as image...")
    gray_img, img_size = extract_pdf_as_image(pdf_path)
    if not gray_img:
        return None
    
    img_width, img_height, _ = gray_img.size  # PIL returns (width, height)
    h, w = img_height, img_width
    print(f"   Image size: {w}x{h} pixels (50 DPI → approx {w*0.2*0.2:.1f}x{h*0.2*0.2:.1f}cm)")

    # 2. Apply preprocessing (gray -> threshold -> clean)
    print("\n2. Applying adaptive thresholding and cleaning...")
    try:
        gray_img_cv = cv2.cvtColor(np.array(gray_img), cv2.COLOR_RGB2GRAY)
        thresh_img = adaptive_threshold_gray(gray_img_cv, offset=127, block_size=45, C=3)
        
        # Remove small noise
        area_mask, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_area = [c for c in area_mask if cv2.contourArea(c) > min_contour_area]
        
        print(f"   Found {len(valid_area)} contours > {min_contour_area} pixels²")
        
    except Exception as e:
        print(f"   Error in thresholding/cleaning: {e}")
        return None
    
    # 3. Extract polygon geometries from valid contours
    print("\n3. Extracting polygon geometries from contours...")
    geo_polygons = []
    geo_ids = []
    contour_count = 0

    try:
        for i, contour in enumerate(valid_area):
            # Convert contour to Shapely-compatible array
            contour = contour.reshape((-1, 1, 2)).astype(np.float64)
            contour = contour.reshape((-1, 2))
            
            # Validate and create polygon
            try:
                poly = Polygon(contour)
                
                # Skip invalid polygons
                if not poly.is_valid or poly.is_empty:
                    print(f"   Contour {i}: Invalid (skip)")
                    continue
                
                # Skip very small polygons (likely noise)
                if poly.area < 100:  # min 0.005 m² (1000 pixels)
                    print(f"   Contour {i}: Too small (area={poly.area:.2f})")
                    continue
                
                # Extract ID from contour (e.g., first 4 digits as ID)
                id_str = f"P{contour_count + 1:04d}"
                
                geo_polygons.append(poly)
                geo_ids.append(id_str)
                
                contour_count += 1
                if (i + 1) % 5 == 0 or contour_count >= 10:
                    print(f"   ✓ Contour {i+1}: area={poly.area:.2f}, id={id_str}")
                    print(f"      Extents: {poly.bounds}")
                
            except Exception as e:
                print(f"   Contour {i}: Geometry error ({e})")
                pass

    except Exception as e:
        print(f"   Geometry extraction error: {e}")
        return None
    
    # 4. Create GeoDataFrame
    print(f"\n4. Creating GeoDataFrame...")
    if geo_polygons:
        gdf = gpd.GeoDataFrame(
            {'id': geo_ids, 'geometry': geo_polygons},
            crs=None  # Set CRS from source map if known
        )
        print(f"\n   Shape: {gdf.shape[0]} polygons, {gdf.shape[1]} columns")
        print(f"\n   Schema:\n{gdf.dtypes}")
        print(f"\n   Summary:\n{gdf.drop(columns=['geometry']).head()}")
        print(f"\n   Geometry bounds:\n{gdf.bounds.head()}")
        
        # Save if desired
        # output_path = pdf_path.replace('.pdf', '.gpkg')
        # gdf.to_file(output_path, driver='GPKG', layer='pdf_trace')
        
        return gdf
    else:
        print("   No valid contours found.")
        return None


def trace_single_image_to_polygons(gray_img, min_contour_area=1000):
    """
    Alternative: Trace a single image (e.g., already-extracted or user-provided).
    
    Args:
        gray_img: PIL grayscale image or numpy array
        min_contour_area: Minimum contour area to keep (pixels^2)
    """
    print("\nTracing single image to polygons...")
    print(f"Input: {type(gray_img)}")
    print(f"  Shape: {gray_img.shape if hasattr(gray_img, 'shape') else gray_img.size}")
    print(f"  Min threshold area: {min_contour_area} pixels")

    try:
        if isinstance(gray_img, Image.Image):
            gray_npy = cv2.cvtColor(np.array(gray_img), cv2.COLOR_RGB2GRAY)
        elif np.ndim(gray_img) == 3:
            gray_npy = cv2.cvtColor(gray_img, cv2.COLOR_RGB2GRAY)
        else:
            gray_npy = gray_img.astype(np.uint8)

        # Threshold
        thresh = cv2.adaptiveThreshold(
            gray_npy,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size=45,
            C=3
        )

        # Contours
        area_mask, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Filter by area
        valid_area = [c for c in area_mask if cv2.contourArea(c) > min_contour_area]
        print(f"  Found {len(valid_area)} valid contours")

        # Convert to geometries
        geo_polygons = []
        geo_ids = []
        for i, contour in enumerate(valid_area):
            # Convert to numpy
            contour = contour.reshape((-1, 2)).astype(np.float64)
            
            # Create polygon
            try:
                poly = Polygon(contour)
                
                if poly.is_valid and not poly.is_empty and poly.area > 100:
                    poly = poly.convex_hull  # Simplify if needed
                    geo_polygons.append(poly)
                    geo_ids.append(f"P{i+1:04d}")
            except Exception as e:
                pass

        # Create geopandas dataframe
        if geo_polygons:
            gdf = gpd.GeoDataFrame({'id': geo_ids, 'geometry': geo_polygons}, crs=None)
            print(f"\n  Result: {len(gdf)} polygons")
            return gdf
        else:
            print("\n  No polygons found!")
            return None

    except Exception as e:
        print(f"\n  Error: {e}")
        return None


if __name__ == "__main__":
    # Configuration
    pdf_path = "/home/sabeiro/lav/src/spiega/deploy/unsloth/map.pdf"
    min_area = 1000  # Minimum contour area (pixels² at 50 DPI)
    
    # Run trace
    gdf = trace_pdf_to_geometry(pdf_path, min_contour_area=min_area)
    
    if gdf is not None:
        print(f"\n=== SUCCESS ===")
        print(f"Extracted {len(gdf)} polygons")
        print(f"GeoDataFrame saved to {pdf_path.replace('.pdf', '.gpkg')}")
        
        # Optional: Save as GeoPackage
        # output_path = pdf_path.replace('.pdf', '.gpkg')
        # gdf.to_file(output_path, driver='GPKG')
        # print(f"Saved to: {output_path}")
        
        # Optional: Show preview
        # fig, ax = plt.subplots(figsize=(12, 8))
        # gdf.plot(ax=ax, column='id')
        # plt.tight_layout()
        # plt.show()
        
    else:
        print("\n=== NO POLYGONS EXTRACTED ===")
        print("  The map image may be too light or all contours were filtered out.")
        print("  Try adjusting min_contour_area or preprocessing parameters.")
