"""
Mesh Exuder Module
Handles extrusion and beveling of Blender meshes.
Can be tested independently.
"""


def prepare_mesh_for_extrude(obj, depth=0.1, segments=2):
    """Prepare mesh object for extrusion with bevel."""
    if not obj or not obj.data:
        return False
    
    # Set bevel settings
    obj.data.bevel_depth = depth * 0.1
    obj.data.bevel_resolution = segments
    obj.data.use_bevel = True
    
    # Scale to proper dimensions
    scale_y = 0.02  # Scale for extrusion
    obj.scale = (1, scale_y, 1)
    
    obj.data.update()
    return True


def extrude_simple_object(obj, depth=0.1, segments=2, apply_material=True):
    """
    Simple extrusion function for testing.
    
    Args:
        obj: Blender object to extrude
        depth: Extrusion depth
        segments: Bevel segments
        apply_material: Whether to apply material (default False for testing)
        
    Returns:
        True if extrusion successful
    """
    if not obj or not obj.data:
        print(f"Error: Object {obj} has no mesh data")
        return False
    
    # Set bevel settings
    obj.data.bevel_depth = depth * 0.1
    obj.data.bevel_resolution = segments
    obj.data.use_bevel = True
    
    bpy.ops.mesh.extrude_region_move()
    
    # Scale to proper dimensions
    scale_y = 0.02  # Scale for extrusion
    obj.scale = (1, scale_y, 1)
    
    obj.data.update()
    
    return True
