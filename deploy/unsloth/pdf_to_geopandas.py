"""
Script to load polygons and their IDs from a PDF map into a GeoPandas DataFrame.

Supports PDF maps containing:
- Embedded vector graphics (SVG-like shapes)
- PDF annotations (polygons)
- Text labels with ID information

Requirements:
- pip install pymupdf geopandas matplotlib
- pip install shapely fiona rasterio (optional, for more complex cases)
"""

import re
import json
import tempfile
import fitz  # PyMuPDF
import geopandas as gpd
from shapely.geometry import Point, Polygon, box
from shapely.ops import split
import numpy as np


def extract_pdf_metadata(pdf_path):
    """Extract basic metadata from PDF"""
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    print(f"\nPDF Metadata:")
    print(f"  Title: {metadata.get('Title', 'N/A')}")
    print(f"  Author: {metadata.get('Author', 'N/A')}")
    print(f"  Creator: {metadata.get('Creator', 'N/A')}")
    print(f"  Pages: {len(doc)}")
    doc.close()


def extract_annotations_polygon(pdf_path):
    """
    Extract polygon annotations from PDF.
    Many CAD/PDF maps use annotation features to define areas.
    """
    doc = fitz.open(pdf_path)
    polygons = []
    polygon_ids = []
    
    print("\nSearching for polygon annotations...")
    
    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get all annotations on the page
            annots = page.annots()
            
            if annots:
                for annot in annots:
                    # Check if annotation is a polygon
                    if annot.type == fitz.PDF_ANNOT_POLYGON:
                        # Get annotation data
                        annot_obj = annot.info
                        annot_data = annot_obj.get("Contents", "")
                        
                        # Try to extract coordinates
                        # Format might vary: "x1,y1,x2,y2,x3,y3,x4,y4" or similar
                        if "," in annot_data:
                            try:
                                coords = re.findall(r'[-\d\.]+', annot_data)
                                if len(coords) >= 6:  # Need at least 3 points
                                    x_coords = [float(c) for c in coords[0::2]]
                                    y_coords = [float(c) for c in coords[1::2]]
                                    
                                    # Fit rectangle if only 4 points
                                    if len(x_coords) >= 4:
                                        minx, miny = min(x_coords), min(y_coords)
                                        maxx, maxy = max(x_coords), max(y_coords)
                                        
                                        # Extract ID from text if available
                                        id_match = re.search(r'ID\s*[:\s]*([A-Z0-9_-]+)', annot_data, re.IGNORECASE)
                                        annot_id = id_match.group(1) if id_match else f"ID_{page_num}_{len(polygons)}"
                                        
                                        polygons.append(box(minx, miny, maxx, maxy))
                                        polygon_ids.append(annot_id)
                                        
                            except Exception as e:
                                print(f"  Warning: Could not parse annotation coords: {e}")
                        continue
                    
                    # Also check for line annotations (rectangles with width=0)
                    elif annot.type in [fitz.PDF_ANNOT_FREE_TEXT, fitz.PDF_ANNOT_TEXT]:
                        # Check if text contains coordinate strings
                        annot_obj = annot.info
                        annot_data = annot_obj.get("Contents", "")
                        
                        if "POLYGON" in annot_data.upper():
                            try:
                                # Extract potential polygon data from text
                                coords = re.findall(r'[-\d\.]+', annot_data)
                                if len(coords) >= 6:
                                    x_coords = [float(c) for c in coords[0::2]]
                                    y_coords = [float(c) for c in coords[1::2]]
                                    
                                    minx, miny = min(x_coords), min(y_coords)
                                    maxx, maxy = max(x_coords), max(y_coords)
                                    
                                    polygons.append(box(minx, miny, maxx, maxy))
                                
                                    # Extract ID if present
                                    id_match = re.search(r'ID[:\s]*([A-Z0-9_-]+)', annot_data, re.IGNORECASE)
                                    annot_id = id_match.group(1) if id_match else f"ANNOT_{page_num}"
                                    polygon_ids.append(annot_id)
                            except Exception as e:
                                print(f"  Warning: Annotation parsing error: {e}")
            
            print(f"  Page {page_num + 1}: Checked {len(page.annots())} annotations")
            
    except Exception as e:
        print(f"  Error extracting annotations: {e}")
    
    doc.close()
    
    print(f"\nExtracted {len(polygons)} polygon annotations\n")
    return polygons, polygon_ids


def extract_vector_shapes(pdf_path):
    """
    Attempt to extract embedded vector shapes from PDF.
    This works for PDFs with embedded vector graphics.
    """
    doc = fitz.open(pdf_path)
    polygons = []
    polygon_ids = []
    
    print("\nSearching for embedded vector shapes...")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_rect = page.rect
        
        # Try to extract text and find potential shape coordinates
        try:
            text = page.get_text("text")
            
            # Look for coordinate patterns that might be part of vector data
            # Some PDFs include SVG or vector coordinate data in comments/text
            coord_patterns = re.findall(
                r'(\[?[-\d,\.]+[-\d,\.]+?])',
                text
            )
            
            for coord_group in coord_patterns:
                try:
                    # Parse coordinate list
                    coords = re.findall(r'-?[\d,\.]+', coord_group)
                    if len(coords) >= 6:  # Need at least 3 points
                        # Filter for reasonable coordinates (within page bounds)
                        coords = [float(c) for c in coords]
                        coords = [c for c in coords if minx <= c <= maxx and miny <= c <= maxy]
                        if len(coords) >= 6:
                            # Form polygon
                            x_coords = coords[0::2]
                            y_coords = coords[1::2]
                            
                            # Try to extract ID from nearby text
                            id_match = re.search(r'[A-Z]{1,3}[-\d]+', text[max(0, page_num * 1000):min(page_num * 1000 + 500)])
                            shape_id = id_match.group(0) if id_match else f"SHAPE_{page_num}"
                            
                            polygons.append(box(coords[0], coords[1], coords[2], coords[3]))
                            polygon_ids.append(shape_id)
                            
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"  Page {page_num + 1} error: {e}")
    
    doc.close()
    
    print(f"  Extracted {len(polygons)} vector shapes\n")
    return polygons, polygon_ids


def create_simple_geometry_from_text(pdf_path, doc_path, shapefile_path=None):
    """
    Alternative approach: If PDF contains ID lists, try to infer simple rectangular zones.
    
    This method:
    1. Extracts all text from the PDF
    2. Identifies ID patterns (like AREA_A, PARCEL_123, etc.)
    3. Creates default rectangular geometries (need to be replaced with real coordinates)
    
    Note: For real polygon coordinates, you'd need either:
    - A georeferenced PDF with embedded coordinate systems
    - Manual conversion from raster to vector (requires image processing)
    - A shapefile/geopackage that the PDF was exported from
    """
    
    doc = fitz.open(pdf_path)
    polygons = []
    polygon_ids = []
    
    print("\nSearching for ID labels in text content...")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_rect = page.rect
        text = page.get_text("text")
        
        # Extract ID patterns (common formats)
        id_patterns = [
            r'\bPARCEL\s*\d+',  # PARCEL_123
            r'\bAREA\s*[A-Z0-9_-]+',  # AREA_A1, AREA_2
            r'\bZONE\s*[A-Z0-9_-]+',  # ZONE_NORTH
            r'\bFOLIO\s*\d+',  # Common in cadastral PDFs
            r'\bSEZIONE\s*\w*',  # Italian cadastral sections
            r'\bPARTIT\w+',  # French cadastral
        ]
        
        for pattern in id_patterns:
            ids = re.findall(pattern, text, re.IGNORECASE)
            for id_text in ids:
                # Clean up ID
                cleaned_id = re.sub(r'[:\s\*]', '', id_text)
                
                # For cadastral maps (like your map.pdf), IDs might be on labels
                # Create placeholder geometry (you'll need to replace with real coordinates)
                # Placeholder: center of page
                cx = page_rect.cx
                cy = page_rect.cy
                
                # Calculate grid if ID contains numeric part
                numeric_match = re.search(r'(\d+)', id_text)
                if numeric_match:
                    idx = int(numeric_match.group(1))
                    # Simple grid spacing (example: 1000 units)
                    grid_size = 1000
                    x = cx + (idx - 1) * grid_size / 10
                    y = cy - grid_size / 2
                    
                    # Create small polygon for demonstration
                    half_size = 250
                    polygons.append(box(
                        x - half_size, 
                        cy - half_size + 500,
                        x + half_size, 
                        cy + half_size + 500
                    ))
                    polygon_ids.append(cleaned_id)
                    break  # Only one per ID for now
    
    doc.close()
    
    print(f"  Found {len(polygon_ids)} ID labels\n")
    return polygons, polygon_ids


def load_as_geopandas_dataframe(pdf_path):
    """
    Main function to load PDF polygons into GeoDataFrames.
    
    Tries in order:
    1. Extract polygon annotations
    2. Extract vector shapes
    3. Infer from ID labels (georef required for accurate coords)
    
    Returns a GeoDataFrame when successful, None otherwise.
    """
    
    print("=" * 60)
    print(f"Loading PDF: {pdf_path}")
    print("=" * 60)
    
    # Metadata
    extract_pdf_metadata(pdf_path)
    
    # Try extraction methods
    polygons = []
    ids = []
    
    # Method 1: Polygon annotations
    ann_polys, ann_ids = extract_annotations_polygon(pdf_path)
    polygons.extend(ann_polys)
    ids.extend(ann_ids)
    
    # Method 2: Vector shapes (only if no annotations found)
    if not polygons:
        vec_polys, vec_ids = extract_vector_shapes(pdf_path)
        polygons.extend(vec_polys)
        ids.extend(vec_ids)
    
    # Method 3: ID labels from text (fallback)
    if not polygons:
        text_labels, text_ids = create_simple_geometry_from_text(pdf_path)
        polygons.extend(text_labels)
        ids.extend(text_ids)
    
    # Create GeoDataFrame
    if polygons:
        gdf = gpd.GeoDataFrame(
            {'id': ids, 'geometry': polygons, 'source': 'PDF'},
            crs=None  # Set CRS from map reference if known
        )
        gdf = gdf.set_index('id')
        
        print("\n=== GeoDataFrame Created ===")
        print(f"\nShape: {gdf.shape[0]} features, {gdf.shape[1]} columns")
        print(f"\nSchema:\n{gdf.dtypes}")
        print(f"\nPreview:\n{gdf.drop(columns=['geometry']).head()}")
        print(f"\nGeometry:\n{gdf.geometry}")
        
        # Save to file if desired
        # gdf.to_file(f"{pdf_path}.gpkg", driver="GPKG")
        
        return gdf
    else:
        print("\n⚠️  No polygons could be extracted from the PDF.")
        print("    PDF might be raster-based (image) or lacks polygon definition.")
        print("    Consider manual annotation or converting to vector format first.")
        return None


# Example usage
if __name__ == "__main__":
    # Load PDF into GeoDataFrame
    pdf_path = "/home/sabeiro/lav/src/spiega/deploy/unsloth/map.pdf"
    
    gdf = load_as_geopandas_dataframe(pdf_path)
    
    if gdf is not None:
        # Save results
        output_path = f"{pdf_path}.gpkg"
        gdf.to_file(output_path, driver="GPKG", layer="pdf_polygons")
        print(f"\nSaved GeoDataFrame to: {output_path}")
        
        # Display summary
        print(f"\nSummary:")
        print(f"  Total polygons: {len(gdf)}")
        print(f"  Total ID count: {gdf['id'].sum()}")
