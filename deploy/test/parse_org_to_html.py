#!/usr/bin/env python3
"""
Parse an OrgMode outline file and convert it to a slide show
"""

import argparse
import re
import sys

def parse_org_outline(org_content):
    """Parse OrgMode outline into slides"""
    lines = org_content.split('\n')
    slides = []
    current_slide = None
    in_header_block = False
    in_code_blocks = False
    in_example_blocks = false
    
    # Parse properties
    properties = {}
    
    for i, line in enumerate(lines):
        # Remove trailing whitespace
        line = line.rstrip()
        
        # Skip empty lines
        if not line or line.strip() == '':
            continue
            
        # Check for header block start
        if line.startswith('#+begin_src') or line.startswith('#+begin_example'):
            in_code_blocks = True
            in_example_blocks = True
            continue
            
        # Check for header block end
        if line.startswith('#+end_src') or line.startswith('#+end_example'):
            in_code_blocks = False
            in_example_blocks = False
            continue
            
        # Check for headline
        if line.startswith('#'):
            # Check for properties line
            if line == '*+TITLE:':
                continue
            
            level = int(line[0])  # # = 1, ## = 2, etc
            title = line[1:]
            body_lines = lines[i+1:i+3]  # Get next 1-2 lines as body
            body = '\n'.join(body_lines)
            
            # Check if this is a new slide (subheadline creates new slide in our case)
            # For now, we treat top-level headings as slide candidates
            
            if current_slide is None:
                current_slide = {
                    'level': level,
                    'title': title,
                    'body': body,
                    'code': []
                }
            else:
                # Check if this should be a new slide
                # For simplicity: 2nd level headings are new slides
                if level == 2 or current_slide.get('slide'):
                    slides.append(current_slide)
                    current_slide = {
                        'level': level,
                        'title': title,
                        'body': body,
                        'code': []
                    }
            continue
        
        # Non-indented text is part of the current heading if there's one
        if current_slide and not line.startswith(' ' * 2):
            if current_slide['body']:
                current_slide['body'] += '\n' + line
            else:
                current_slide['body'] = line
        else:
            # Indented code or content
            if current_slide:
                current_slide['code'].append(line)
    
    # Add the last slide
    if current_slide:
        slides.append(current_slide)
    
    return slides

def clean_title(title):
    """Clean up the title string"""
    # Replace org links
    title = re.sub(r'\(\[([^\]]+)\]\)', r'\1', title)
    # Remove property markers
    title = re.sub(r'\*\+', '', title)
    title = title.strip('*')
    title = title.strip()
    return title

def clean_body(body):
    """Clean up body content"""
    # Keep first 2-3 lines, truncate if too long
    lines = body.split('\n')
    # Remove empty lines
    lines = [l.strip() for l in lines if l.strip()]
    # Take first few lines
    if len(lines) > 5:
        # Keep first few meaningful lines
        meaningful_lines = [l for l in lines[:3] if not l.startswith('#+')]
        return '\n'.join(meaningful_lines)
    return body

def process_slide(slide, idx):
    """Process a slide for HTML generation"""
    title = clean_title(slide['title'])
    body = clean_body(slide['body'])
    
    # Process code blocks (Python examples)
    code_lines = []
    for line in slide.get('code', []):
        # Check if this is part of a code block
        if 'python' in line.lower() or 'example' in line.lower() or 'code' in line.lower():
            code_lines.append(line)
    
    # Generate slide content
    if body:
        content = f'<p>{body.strip()}</p>'
    else:
        content = f'<p>Content for slide {idx + 1}</p>'
    
    # Process code blocks in body
    # Simple regex to find and process code blocks
    processed_body = re.sub(r'\\*?\[python\]+.*?\\*?\[end_index\]', lambda m: m.group(0), body)
    
    return {
        'title': title,
        'content': content,
        'code': code_lines
    }

def generate_html(slides):
    """Generate HTML file from slides"""
    
    # Check for required Python environment
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        pass  # Just warnings, we'll generate with placeholder content
    
    html_parts = []
    
    # Build slide content
    processed_slides = []
    for idx, slide in enumerate(slides):
        processed = process_slide(slide, idx)
        processed_slides.append(processed)
    
    # Generate HTML
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>''{title}'' - Slide Show</title>
    <link rel="stylesheet" href="../static/style.css">
    <style>
        /* Slide show specific */
        .slide-container {
            overflow-y: auto;
        }
        .slide {
            height: 100%;
        }
        .footer {
            height: 40px;
            background: var(--footer-bg);
        }
        .keyboard-hint {
            font-size: 0.7rem;
            color: var(--text-muted);
            padding: 8px;
        }
    </style>
</head>
<body>
<div class="content" id="content">
    <div class="slides" id="slides-container">
'''
    
    for i, slide in enumerate(processed_slides):
        if slide['title']:
            html += f'''
        <div class="slide active" id="slide-{i}">
            <h2>''{slide['title']}''</h2>
            {slide['content']}
        </div>
'''
        else:
            html += f'''
        <div class="slide" id="slide-{i}">
            <p>Slide {i+1}</p>
        </div>
'''
    
    # Check for Python environment and generate visualizations/examples
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Generate example plots
        fig, ax = plt.subplots(figsize=(6, 4))
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y)
        ax.set_title('Example Plot')
        plt.savefig('../static/example.png')
        
        # Add a Python code example
        html += '''
        <div class="slide" id="slide-python">
            <h2>Python Examples</h2>
            <pre><code>
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.show()
            </code></pre>
        </div>
'''
    except Exception:
        pass
    
    # Close HTML
    html += '''</div>

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
    <div class="keyboard-hint" title="Keyboard hints">
        Left/Right arrows or Enter | T toggle TOC | Space/Home/End | X to close | ? for help
    </div>
</div>

<!-- Side panel (TOC) -->
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
</html>'''
    
    return html

def main():
    parser = argparse.ArgumentParser(description='Parse OrgMode outline to slide show')
    parser.add_argument('input_file', help='Input OrgMode file')
    parser.add_argument('output_file', help='Output HTML file')
    parser.add_argument('--title', default='Slide Show', help='Title for the slide show')
    args = parser.parse_args()
    
    try:
        # Read Org file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            org_content = f.read()
        
        # Parse outline
        slides = parse_org_outline(org_content)
        
        if not slides:
            print('No slides found in the Org file. Using placeholder content.')
            slides = [
                {'title': 'First Slide', 'body': 'This is the first slide.'},
                {'title': 'Second Slide', 'body': 'This is the second slide.'},
            ]
        
        # Generate HTML
        html = generate_html(slides)
        
        # Generate complete slide show HTML
        final_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$$args.title$$ - Slide Show</title>
    <link rel="stylesheet" href="../static/style.css">
    <style>...</style>
</head>
<body>
'''
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f'Generated slide show: {args.output_file}')
        print(f'Total slides: {len(slides)}')
        
        return 0
    except FileNotFoundError:
        print(f'Error: File {args.input_file} not found')
        return 1
    except Exception as e:
        print(f'Error: {e}')
        return 1

if __name__ == '__main__':
    sys.exit(main())