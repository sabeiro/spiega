#!/bin/bash
# Generate a test slide show HTML file

# Set paths
PROJECT_DIR="$SRC_DIR"
HTML_DIR="$PROJECT_DIR/html"
JS_DIR="$HTML_DIR/js"
STATIC_DIR="$HTML_DIR/static"

# Create required directories
mkdir -p "$STATIC_DIR"

# Check if Python environment exists
if ! python3 -c "import matplotlib.pyplot as plt; import numpy as np" 2>/dev/null; then
    echo "Python matplotlib environment not found. Using basic text slides."
    ENV_MISSING=true
else
    ENV_MISSING=false
fi

if "$ENV_MISSING"; then
    # Generate simple text slides
    cat > "$HTML_DIR/test_slides.html" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Slide Show</title>
    <link rel="stylesheet" href="./static/style.css">
</head>
<body>
<div class="content" id="content">
    <div class="slides" id="slides-container">
        <div class="slide" id="slide-1">
            <h2>Welcome to the Slide Show</h2>
            <p>This is a simple test slide.</p>
            <p>Please press Enter or the right arrow to continue.</p>
        </div>
        
        <div class="slide" id="slide-2">
            <h2>Navigation Controls</h2>
            <ul>
                <li>Left/Right arrows or Enter: Next slide</li>
                <li>Shift + Arrows: Previous slide</li>
                <li>Home/End: Goto first/last slide</li>
                <li>T: Toggle side panel</li>
                <li>X or Escape: Close slide</li>
                <li>?: Show help</li>
            </ul>
        </div>
        
        <div class="slide" id="slide-3">
            <h2>Keyboard Shortcuts</h2>
            <p>Remember to press <strong>T</strong> to see the slide navigation menu.</p>
            <p>Or use the buttons at the bottom.</p>
        </div>
        
        <div class="slide" id="slide-4">
            <h2>Features</h2>
            <ul>
                <li>Auto-slide toggle</li>
                <li>Progress bar</li>
                <li>Slide counter</li>
                <li>Responsive layout</li>
            </ul>
        </div>
        
        <div class="slide" id="slide-5">
            <h2>Thank You!</h2>
            <p>Press the right arrow to end this presentation.</p>
        </div>
    </div>
    
    <div class="footer" id="footer">
        <div class="nav-panel">
            <button class="btn btn-prev" id="btn-prev">&lt;&lt;</button>
            <div class="slide-counter" id="slide-counter"></div>
            <button class="btn btn-next" id="btn-next">&gt;&gt;</button>
            <span style="display:inline-block; width:1px; height:20px; margin:0 8px; background:var(--border-color);"></span>
            <label style="display:flex; align-items:center; gap:4px; font-size:0.8rem;">
                <input type="checkbox" id="auto-slide-toggle"> Auto-slide
            </label>
            <button class="btn btn-top" id="btn-top">↑</button>
            <button class="btn btn-close" id="btn-close">&times;</button>
        </div>
        <div class="keyboard-hint">
            Arrows/Enter: Navigate | T: Toggle TOC | Space/Home/End | X to close | ? for help
        </div>
    </div>
    
    <!-- Side panel -->
    <div id="side-panel" aria-hidden="true">
        <nav class="side-panel-toc" id="side-panel-toc-nav">
            <h3>Slide Navigation</h3>
            <ul id="slide-toc-visible">
            </ul>
            <button class="btn btn-close" id="btn-close-sidepanel" style="margin-top:1rem; width:100%;">✕ Close</button>
        </nav>
    </div>
    
    <script src="./js/script.js"></script>
</body>
</html>
HTMLEOF
else
    # Generate slides with Python examples
    cat > "$HTML_DIR/test_slides.html" << 'PHTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Slide Show with Python</title>
    <link rel="stylesheet" href="./static/style.css">
    <style>
        .code-block {
            background: var(--code-bg);
            border: 1px solid var(--code-border);
            border-radius: 4px;
            padding: 8px;
            margin: 8px 0;
            overflow-x: auto;
        }
        .highlight {
            color: var(--accent);
            font-weight: bold;
        }
        .slide-content {
            max-width: 800px;
            margin: 0 auto;
        }
    </style>
</head>

<body>
<div class="content" id="content">
    <div class="slides" id="slides-container">
        <div class="slide" id="slide-1">
            <h2>Welcome to the Slide Show</h2>
            <div class="slide-content">
                <p>This is an interactive slide show with navigation controls.</p>
                <p>Use keyboard or mouse to navigate through slides.</p>
            </div>
            <div class="code-block">
                <p><strong>Tip:</strong> Press <span class="highlight">T</span> to show the navigation menu!</p>
            </div>
        </div>
        
        <div class="slide" id="slide-2">
            <h2>Navigation Controls</h2>
            <div class="slide-content">
                <p><strong>Navigation:</strong></p>
                <ul>
                    <li>Left/Right arrows or Enter: Previous/Next slide</li>
                    <li>Shift + Arrows: Go back/forward</li>
                    <li>Home/End: First/Last slide</li>
                    <li>Space: Next slide</li>
                </ul>
                <p><strong>UI Controls:</strong></p>
                <ul>
                    <li>T: Toggle side panel</li>
                    <li>X or Escape: Close slide</li>
                    <li>?: Show help</li>
                </ul>
            </div>
        </div>
        
        <div class="slide" id="slide-3">
            <h2>Python Code Example</h2>
            <div class="slide-content">
                <p>Here's a simple Python example:</p>
                <div class="code-block">
<pre>import matplotlib.pyplot as plt
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Plot it
plt.figure(figsize=(8, 4))
plt.plot(x, y, linewidth=2)
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.title('Sine Wave')</pre>
                </div>
                <p>Run this code to see the plot.</p>
            </div>
        </div>
        
        <div class="slide" id="slide-4">
            <h2>Features</h2>
            <div class="slide-content">
                <ul>
                    <li><strong>Auto-slide:</strong> Enable automatic progression</li>
                    <li><strong>Progress bar:</strong> See where you are</li>
                    <li><strong>Slide counter:</strong> Track slide number</li>
                    <li><strong>Responsive:</strong> Works on all screens</li>
                    <li><strong>Accessible:</strong> Keyboard navigable</li>
                </ul>
            </div>
        </div>
        
        <div class="slide" id="slide-5">
            <h2>Additional Examples</h2>
            <div class="slide-content">
                <p>Python for data visualization examples.</p>
                <div class="code-block">
<pre># Data visualization example
import pandas as pd
import seaborn as sns

# Create sample data
tips = sns.load_dataset('tips')

# Box plot
sns.boxplot(x='day', y='total_bill', data=tips)</pre>
                </div>
            </div>
        </div>
        
        <div class="slide" id="slide-6">
            <h2>Thank You!</h2>
            <div class="slide-content">
                <p>End of the presentation.</p>
                <p>Press Enter or Right arrow to end.</p>
            </div>
        </div>
        
        <div class="slide" id="slide-7">
            <h2>Final Slide</h2>
            <div class="slide-content">
                <p>This is the last slide.</p>
                <p>Try navigating around freely!</p>
            </div>
        </div>
    </div>
    
    <div class="footer" id="footer">
        <div class="nav-panel">
            <button class="btn btn-prev" id="btn-prev">&lt;&lt;</button>
            <div class="slide-counter" id="slide-counter"></div>
            <button class="btn btn-next" id="btn-next">&gt;&gt;</button>
            <span style="display:inline-block; width:1px; height:20px; margin:0 8px; background:var(--border-color);"></span>
            <label style="display:flex; align-items:center; gap:4px; font-size:0.8rem;">
                <input type="checkbox" id="auto-slide-toggle"> Auto-slide
            </label>
            <button class="btn btn-top" id="btn-top">↑</button>
            <button class="btn btn-close" id="btn-close">&times;</button>
        </div>
        <div class="keyboard-hint">
            <strong>Keyboard:</strong> Arrows/Enter: Navigate | T: Toggle TOC | Space/Home/End | X to close | ? for help
        </div>
    </div>
    
    <!-- Side panel -->
    <div id="side-panel" aria-hidden="true">
        <nav class="side-panel-toc" id="side-panel-toc-nav">
            <h3>Slide Navigation</h3>
            <ul id="slide-toc-visible">
            </ul>
            <button class="btn btn-close" id="btn-close-sidepanel" style="margin-top:1rem; width:100%;">✕ Close</button>
        </nav>
    </div>
    
    <script src="./js/script.js"></script>
</body>
</html>
PHTMLEOF
fi

echo "Generated: $HTML_DIR/test_slides.html"
echo "Open a browser and navigate to: $HTML_DIR/"