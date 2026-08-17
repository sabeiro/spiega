# How to See a Cube in Blender

## Quick Steps

1. **Open Blender** (from terminal or app):
```bash
blender
```

2. **Open a blank project** or existing `.blend` file

3. **Open Python script**:
```bash
code /home/sabeiro/lav/src/blender_twin/deploy/mcp_client/EMACS/add_cube_script.py
```

4. **Copy this code into Blender's Text Editor** (File → Script)

5. **Run the script** (`Ctrl+F3` in Blender)

## Terminal Method (if Blender is installed)

To run Blender via command-line, use:

```bash
blender --background --python /home/sabeiro/lav/src/blender_twin/deploy/mcp_client/EMACS/add_cube_script.py
```

But this runs in headless mode, not GUI.

## Interactive Method

1. Start Blender
2. Press `Ctrl+F3` to open Python Console
3. Copy paste code:
```python
import bpy

# Add cube
bpy.ops.mesh.primitive_cube_add(location=(5.0, 5.0, 5.0))
bpy.context.view_layer.objects.active = bpy.context.active_object
bpy.ops.object.select_all(action='SELECT')
```

## Visual Confirmation

The cube will appear in:
- 3D Viewport
- Outliner (Object list)
- 3D Cursor location

---

For Emacs integration, use the extension code that runs in Emacs Python buffers.
