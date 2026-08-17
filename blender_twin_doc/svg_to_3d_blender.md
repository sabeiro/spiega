# SVG to 3D Blender Model Converter

Convert SVG diagram files into 3D Blender models with extrusion, beveling, and materials applied based on object ID types.

## Features

- Parses SVG files containing paths, rectangles, circles, and other shapes
- Converts 2D SVG paths into 3D mesh objects
- Extrudes objects with customizable depth
- Applies bevels for smooth edges
- Creates materials with color from fill attributes
- Supports stroke-based glossy materials
- Organizes objects by their SVG-defined IDs

## Usage

### Command Line

```bash
blender --background --python svg_to_3d_model.py -- \
    --svg-path=path/to/your_diagram.svg \
    --output=output_model.blend \
    --scale 1.0 \
    --extrude 0.1 \
    --bevel 2
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--svg-path` | Path to input SVG file (required) | - |
| `--output` | Output blend file path | No save |
| `--scale` | Overall scale multiplier | 1.0 |
| `--extrude` | Extrusion depth | 0.1 |
| `--bevel` | Bevel segment count | 2 |

### Quick Start

```bash
# Convert a single SVG
blender --background \
    --python /home/sabeiro/lav/src/blender_twin/scripts/svg_to_3d_model.py \
    -- --svg-path=diagrams/sample.svg --output=sample_3d.blend
```

## Requirements

- Blender 3.2+ with Python scripting
- Python 3.x standard library

## SVG Requirements

The SVG file should contain:

```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <!-- Elements with fill/color and optional id attributes -->
  <rect id="box-1" x="10" y="10" width="100" height="50" fill="#ff0000"/>
  <path id="curve-1" d="M 10 60 C ..." fill="#00ff00" stroke="#000000" stroke-width="1"/>
  <circle id="point-1" cx="200" cy="100" r="20" fill="#0000ff"/>
</svg>
```

Elements are identified by:
- `id` attribute (preferred)
- `class` attribute (first token used if no id)

## Object Mapping

| SVG Element | 3D Object Type |
|-------------|----------------|
| `path` | Extruded mesh from path points |
| `rect` | Quad planar mesh |
| `circle` | Spherical mesh |

## Material Application

Materials are created based on fill colors:

- **Fill color**: Applied to base Principled BSDF as base_color
- **Stroke**: Can trigger glossy shader component (optional)
- **Color format**: Hex (#RGB or #RRGGBB) or RGB tuple

## Examples

### Example 1: Basic Conversion

```python
from svg_to_3d_model import main

# Convert and save
main(
    svg_path="diagrams/block_diagram.svg",
    output_path="models/block_3d.blend",
    scale=1.5,
    extrude_depth=0.15,
    bevel_segments=2
)
```

### Example 2: Batch Processing

```python
import glob

svg_files = glob.glob("diagrams/*.svg")
for svg_file in svg_files:
    base_name = Path(svg_file).stem
    output_path = f"models/{base_name}_3d.blend"
    
    create_3d_model(
        path=svg_file,
        output=output_path,
        scale=2.0,
        extrude=0.1
    )

print("Batch conversion complete!")
```

## API Reference

### main(svg_path, output_path=None, scale=1, extrude_depth=0.1, bevel_segments=2)

Convert SVG file to 3D model.

**Parameters:**
- `svg_path`: Path to SVG file (str, required)
- `output_path`: Output BLEND file (str, optional)
- `scale`: Scale multiplier (float, default: 1.0)
- `extrude_depth`: Extrusion depth (float, default: 0.1)
- `bevel_segments`: Bevel resolution (int, default: 2)

**Returns:**
- Dictionary mapping object IDs to created Blender objects {}

### parse_svg_paths(svg_path)

Parse SVG file into object dictionaries.

**Returns:**
- Dictionary mapping IDs to object attributes dict

### clear_scene()

Clear existing scene objects and materials.

**Use:** Always call before creating new models.

### create_mesh_from_dict(points_data)

Create 3D mesh from parsed SVG data.

**Returns:**
- Blender mesh object or None

## Troubleshooting

### No objects created
- Check SVG file is valid XML
- Verify elements have `id` or `class` attributes
- Use `--debug` flag to see parsing errors

### Materials not appearing
- Ensure Blender uses Cycles or Eevee renderer
- Check material output node is active
- Material names may be duplicated; script handles unique IDs

### Extrusion depth too small
- Increase `--extrude` or scale parameter
- Increase `--scale` for better visibility

## License

This script is part of the LAV project and follows the project's license terms.

## Contributing

To extend this script:
1. Add support for new SVG elements (`polyline`, `polygon`, etc.)
2. Implement texture mapping from SVG images
3. Add lighting based on SVG stroke colors
4. Support multiple SVG files in one scene

## Additional Resources

- [Blender Python API](https://docs.blender.org/api/current/bpy.html)
- [SVG Path Data Commands](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths)
- [Blender Nodes](https://wiki.blender.org/index.php/Advanced Techniques/Shader_Node_Editing)
