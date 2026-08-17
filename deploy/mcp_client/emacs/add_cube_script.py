import bpy
import os

# Add cube directly in Blender
bpy.ops.mesh.primitive_cube_add(location=(5.0, 5.0, 5.0))
cube = bpy.context.active_object
cube.name = "MyCube"
cube.dimensions = (2.0, 2.0, 2.0)
cube.rotation_euler = (45.0, 0.0, 0.0)

print(f"Added cube: {cube.name} at {cube.location}")
print(f"Dimensions: {cube.dimensions}")

# Select it
bpy.context.view_layer.objects.active = cube

# Show info
with open('/home/sabeiro/lav/src/blender_twin/deploy/mcp_client/EMACS/.blender_status.json', 'w') as f:
    f.write(f"Cube added: {cube.name}\nLocation: {cube.location}\n\n")
