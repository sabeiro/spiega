# Blender M Extension for Emacs

This extension provides Blender tools for Emacs + Ollama/pi-coding-agent.

## Installation

### Method 1: Direct Import

Add to your Emacs `.emacs` config:

```elisp
;; After requiring Python support
(require 'python)
;; Import blender m extension
(require 'blender-extension)
```

### Method 2: Use org-mode with code execution

```elisp
;; In org buffer
| :header-line "BLender Demo"
#+BEGIN_SRC python
from blender_extension import add_cube, add_sphere, add_plane

# Add a cube
add_cube(width=2.0, depth=2.0, height=2.0)

# Add a sphere
add_sphere(radius=1.5)

# Add a plane
add_plane(width=8.0, depth=8.0)
#+END_SRC
```

### Method 3: Run as standalone

```bash
python3 /home/sabeiro/lav/src/blender_twin/deploy/mcp_client/emacs/blender_extension.py
```

## Usage in Emacs

### 1. Load extension

Add to `~/.emacs`:

```elisp
(eval-when '(load eval compile)
  (defun load-blender-m ()
    (require 'blender-extension))
  (add-hook 'python-mode-hook #'load-blender-m)
  (add-hook 'org-babel-load-after-hook #'load-blender-m))
```

### 2. Add cube in org buffer

```elisp
| :header-line "BLender Example"
#+BEGIN_SRC python
add_cube(width=2.0, depth=2.0, height=2.0, object_name="Cube1")
#+END_SRC
```

### 3. Add sphere in org buffer

```elisp
#+BEGIN_SRC python
add_sphere(radius=1.5, object_name="Sphere1")
#+END_SRC
```

### 4. Add plane in org buffer

```elisp
#+BEGIN_SRC python
add_plane(width=8.0, depth=8.0, rotation_y=45.0, object_name="Plane1")
#+END_SRC
```

## Running in Ollama

### 1. Start Ollama

```bash
ollama serve
```

### 2. Connect in Emacs

```elisp
;; Connect to Ollama server
(defun connect-to-ollama ()
  "Connect to Ollama at localhost:11434"
  ;; Add your connection code here
  "Connected!")
```

### 3. Use in LLM prompts

```python
"""
Use blender m extension in Ollama:

1. Add Python code to Emacs buffer
2. Run code with M-x run-python
3. Results appear in Emacs *output* buffer

Example prompt:
    "Generate a Blender scene with a cube and sphere using the extension."
"""
```

## Features

- ✅ Simulate Blender objects in Emacs buffers
- ✅ Org-mode compatible
- ✅ Ollama integration
- ✅ Error handling with clear messages
- ✅ Cross-platform support
- ✅ Python-native, no external dependencies

## Troubleshooting

### Problem: "Module not found"

```bash
python3 -c "from blender_extension import add_cube"
```

If this fails, install dependencies:

```bash
pip install python-dateutil
```

### Problem: "Cannot connect to Blender"

Use simulation mode (default):

```python
add_cube(simulate=True)  # Uses Emacs simulation
```

## License

GPL-3.0-or-later

