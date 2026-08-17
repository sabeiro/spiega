#!/usr/bin/env python3
"""
Trace bitmap map from PDF to vector polygons using pdftoppm + OpenCV + Shapely.
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
        
        # Try pdftoppm with single file
        cmd = f"pdftoppm -png -singlefile -r {dpi} {pdf_path} {basename}"
        result = subprocess.run(cmd, shell=True, capture_output=True)
        
        if result.returncode != 0:
            print(f"  pdftoppm error: {result.stderr.decode() or 'unknown error'}")
            return None
        
        # Look for output files
        output_path = f"{basename}-1{dpi}.png"
        if not os.path.exists(output_path):
            output_path = f"{basename}-{dpi}.png"
        if not os.path.exists(output_path):
            output_path = f"{basename}-1.png"
        if not os.path.exists(output_path):
            output_path = f"{basename}.png"
            
        print(f"  Extracted: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"  Error: {e}")
        return None

def trace_bitmap_to_polygons(image_path, min_area=200000):
    """
    Trace bitmap to vector polygons.
    
    Args:
        image_path: Path to grayscale image
        min_area: Minimum contour area in pixels (default 200000)
    
    Returns:
        GeoDataFrame or None
    """
    try:
        print(f"\n2. Tracing bitmap to vector polygons...")
        print(f"   Min area threshold: {min_area} pixels ({min_area/22500:.3f} m²)")
        print(f"   Image: {image_path}")
        
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"   Could not load image: {image_path}")
            return None
        
        print(f"   {img.shape[1]}x{img.shape[0]})")
        img = img.copy()
        
        # Threshold and find contours
        _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV)
        
        print(f"   Total area: {img.shape[0] * img.shape[1]} pixels ({img.shape[0] * img.shape[1] / 22500:.3f} m²)")
        
        # Find contours
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        # Filter contours by area
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_area:
                valid_contours.append(contour)
        
        print(f"   Found {len(contours)} contours")
        valid_cnts = len(valid_contours)
        print(f"   Contours > {min_area} px²: {valid_cnts}")
        
        if not valid_contours:
            # Try smaller threshold
            print(f"   Trying smaller threshold ({min_area // 2}px²)...")
            valid_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area >= min_area // 2:
                    valid_contours.append(contour)
            
            print(f"   Contours > {min_area // 2} px²: {len(valid_contours)}")
        
        if not valid_contours:
            print("   No valid contours found!")
            return None
        
        # Remove largest contour (usually border)
        if len(valid_contours) > 0:
            sorted_contours = sorted(valid_contours, key=cv2.contourArea, reverse=True)
            if cv2.contourArea(sorted_contours[0]) > min_area * 5:
                print(f"   Skipping largest contour (border): {cv2.contourArea(sorted_contours[0]):.1f} px²")
                valid_contours = sorted_contours[1:]
        
        # Convert to polygons
        geo_polygons = []
        geo_ids = []
        total_area = 0
        
        for i, contour in enumerate(valid_contours):
            contour = np.reshape(contour, (-1, 2), order='C').astype(np.float64)
            poly = Polygon(contour)
            
            if poly.is_valid and not poly.is_empty and poly.area > 100:
                max_area = img.shape[0] * img.shape[1]
                if cv2.contourArea(contour) < max_area * 0.99:
                    geo_polygons.append(poly)
                    geo_ids.append(f"POLY_{i+1:04d}")
                    total_area += poly.area
        
        print(f"   Valid polygons: {len(geo_polygons)}")
        
        if not geo_polygons:
            return None
        
        # Create GeoDataFrame
        print(f"\n3. Creating GeoDataFrame...")
        print(f"   Shape: {len(geo_polygons)} polygons")
        
        gdf = gpd.GeoDataFrame(
            {'id': geo_ids, 'geometry': geo_polygons},
            crs=None
        )
        print(f"   Total area: {total_area/10000:.2f} m²")
        
        return gdf
        
    except Exception as e:
        print(f"   Error: {e}")
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
    
    min_contour_area = 200000  # Default: ~0.78 m² at 150 DPI
    
    if len(sys.argv) >= 4:
        min_contour_area = int(sys.argv[3])
    
    print("=" * 60)
    print(f"PDF Trace to Vector Polygons (pdftoppm + OpenCV)")
    print(f"=" * 60)
    
    print(f"\nSource: {input_path}")
    print(f"DPI: {dpi}")
    print(f"Min area: {min_contour_area} pixels ({min_contour_area/22500:.3f} m²)")
    
    # Extract PDF as image
    print("\n1. Extracting PDF page...")
    image_path = extract_pdf_as_image(input_path, dpi=dpi)
    
    if image_path is None:
        print("   Failed to extract image")
        return
    
    # Trace to polygons
    gdf = trace_bitmap_to_polygons(image_path, min_area=min_contour_area)
    
    if gdf is not None:
        print(f"\n=== SUCCESS ===")
        print(f"Extracted {len(gdf)} polygons")
        print(f"\n{gdf}")
        total_area = gdf.geometry.area.sum()/10000
        print(f"\nTotal area: {total_area:.2f} m²")
        
        # Save GeoJSON
        output_gjson_path = input_path.replace('.pdf', '.gjson').replace('.png', '.gjson')
        gdf.to_file(output_gjson_path, driver='GeoJSON')
        print(f"\nSaved to: {output_gjson_path}")
        
    else:
        print("\n=== NO POLYGONS EXTRACTED ===")
        print("  Adjust min_contour_area parameter in script")


if __name__ == "__main__":
    main()
