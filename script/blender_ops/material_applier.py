"""
Material Applier Module
Creates and applies materials to Blender objects.
Can be tested independently.
"""


def apply_material_to_object(
    obj,
    mat_name,
    fill_color,
    stroke=False,
    stroke_width=1.0
):
    """
    Create shader nodes and assign material to an object.
    
    Args:
        obj: Blender object
        mat_name: Material name (will be appended with ID if duplicate)
        fill_color: Fill color (rgb tuple or hex string)
        stroke: Whether to add stroke/glossy layer
        stroke_width: Stroke thickness
        
    Returns:
        Assigned material
    """
    color = fill_color
    if isinstance(fill_color, str):
        if fill_color.startswith('#') and len(fill_color) >= 7:
            hex_color = fill_color[3:7].upper()
            color = [
                int(hex_color[0:2], 16) / 255.0,
                int(hex_color[2:4], 16) / 255.0,
                int(hex_color[4:6], 16) / 255.0
            ]
        else:
            color = [0.3, 0.3, 0.3]
    
    # Create or get material
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(name=mat_name)
    
    mat.use_nodes = True
    outputs = mat.node_tree.nodes.get('Output Material')
    if not outputs:
        outputs = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
        outputs.is_active = True
    
    # Create Principled BSDF
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if not bsdf:
        bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.inputs['base_color'].default_color = color
        bsdf.inputs['alpha'].default_value = 1.0
    
    # Ensure connection
    if not bsdf.outputs['bsdf'].links:
        connections = mat.node_tree.links.new(
            bsdf.outputs['bsdf'],
            outputs.inputs['surface']
        )
    
    # Apply glossy node for stroke
    if stroke:
        glossy = mat.node_tree.nodes.get('Glossy BSDF')
        if not glossy:
            glossy = mat.node_tree.nodes.new('ShaderNodeBsdfGlossy')
        glossy.inputs['color'].default_color = (0.1, 0.1, 0.1, 1.0)
        glossy.inputs['roughness'].default_value = 0.3
        glossy.inputs['IOR'].default_value = 1.47
        bsdf.inputs['specular_iOR'].default_value = 0.6
    
    return mat
