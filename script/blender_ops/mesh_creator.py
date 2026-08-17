"""
Mesh Creator Module
Creates planar meshes from parsed SVG data.
Can be combined with Blender later.
"""

import math


def create_planar_mesh_from_points(points):
    """Create a planar mesh from a list of points (closed polygon)."""
    if not points or len(points) < 3:
        return None
    
    # Limit vertices for performance
    max_verts = 512
    points = points[:max_verts]
    
    vertices = []
    for px, py in points:
        vertices.append(mathutils.Vector((px, py, 0)))
    
    # Create mesh
    mesh = bpy.data.meshes.new("SVG_Polygon")
    obj = bpy.data.objects.new("SVG_Polygon", mesh)
    bpy.context.collection.objects.link(obj)
    
    # Generate UV grid and triangulate
    mesh.from_pydata(
        vertices=[v.co for v in vertices],
        edges=[(i, (i + 1) % len(vertices)) for i in range(len(vertices) - 1)] + [(len(vertices) - 1, 0)],
        faces=[[i, (i + 1) % len(vertices), (i + 2) % len(vertices)] for i in range(len(vertices))]
    )
    mesh.update()
    
    return obj


def create_circle_mesh_from_data(cx, cy, radius):
    """Create a circle mesh with circular vertices."""
    # Create circle using primitive
    bpy.ops.mesh.primitive_circle(num_segments=32)
    circle_obj = bpy.context.object
    
    circle_obj.location = (cx, cy, 0)
    circle_obj.scale = (radius, radius, 1)
    
    bpy.context.view_layer.objects.active = circle_obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    return circle_obj


import mathutils


def create_mesh_from_dict(points_data):
    """Create mesh from parsed SVG object data (path, rect, etc)."""
    if not points_data:
        return None
    
    point_type = points_data.get('type', 'path')
    
    if point_type == 'path':
        return create_planar_mesh_from_points(points_data.get('points', [[0, 0]]))
    elif point_type == 'rect':
        # Rect has special handling
        points = points_data.get('points', [[0, 0], [1, 0], [1, 1], [0, 1]])
        return create_planar_mesh_from_points(points)
    elif point_type == 'circle':
        return create_circle_mesh_from_data(
            points_data.get('cx', 0),
            points_data.get('cy', 0),
            points_data.get('r', 10)
        )
    
    return None
