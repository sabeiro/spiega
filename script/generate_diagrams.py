#!/usr/bin/env python3
#===============================================================================
# generate_diagrams.py - Generate diagrams from markdown files
#===============================================================================

import sys
import re
import os
from pathlib import Path

def extract_code_blocks(content, block_type=None):
    """Extract code blocks from markdown content."""
    # Pattern for ```language ... ```
    pattern = r'```(.*?)\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    blocks = []
    for lang, body in matches:
        block_type = block_type or lang.strip()
        blocks.append({
            'type': block_type,
            'content': body.strip()
        })
    
    return blocks

def merge_diagrams_into_html(md_file, html_file, diagram_input=""):
    """Merge diagrams from markdown into HTML output."""
    
    try:
        # Read markdown file
        if md_file == '-':
            md_content = sys.stdin.read()
            md_filename = '<stdin>'
        elif os.path.exists(md_file):
            with open(md_file, 'r') as f:
                md_content = f.read()
            md_filename = os.path.basename(md_file)
        else:
            print(f"Error: Markdown file not found: {md_file}", file=sys.stderr)
            sys.exit(1)
        
        # Read any diagram input
        diagram_content = diagram_input[:5000] if diagram_input else ""
        
        # Extract all diagram blocks
        diagrams = extract_code_blocks(md_content)
        
        # Generate HTML header
        header = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
'''
        
        # Determine page title
        lines = md_content.split('\n')
        title = lines[0] if lines else f"H{len(diagrams)+1} - $(basename)"
        title = title.replace('#', '').strip()
        
        header += f'    <title>{title} - Blender CV Documentation</title>\n'
        header += '''    <link rel="stylesheet" href="../static_html/assets/css/style.css">
    <style>
        /* Slide styles */
        :root {
        --primary: #2563eb;
        --secondary: #7c3aed;
        --bg: #0f172a;
        --text: #e2e8f0;
        --slide-bg: #1e293b;
        --heading: #f1f5f9;
        --code-bg: #334155;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .document { padding: 2rem 0; }
        h1, h2, h3, h4 { margin: 1.5rem 0 1rem; color: var(--heading); }
        h1 { font-size: 2rem; border-bottom: 2px solid var(--primary); padding-bottom: 0.5rem; }
        h2 { font-size: 1.5rem; }
        
        /* Code blocks */
        pre {
            background: var(--code-bg);
            padding: 1rem;
            border-radius: 5px;
            overflow-x: auto;
            margin: 1rem 0;
            font-family: 'Monospace', monospace;
        }
        
        /* Diagram container */
        .diagram-container {
            background: var(--slide-bg);
            padding: 2rem;
            margin: 2rem 0;
            border-left: 4px solid var(--primary);
            border-radius: 5px;
            min-height: 400px;
        }
        .diagram-header {
            font-size: 1.2rem;
            margin-bottom: 1rem;
            color: var(--heading);
        }
        .diagram-content {
            min-height: 200px;
            border: 1px dashed var(--primary);
            padding: 1rem;
            margin-top: 1rem;
            border-radius: 3px;
        }
        
        /* Mermaid specific */
        .diagram-content.mermaid {
            font-family: 'monospace';
        }
        
        /* Graphviz specific */
        .diagram-content.dot {
            font-family: 'monospace';
        }
        
        /* Plantuml specific */
        .diagram-content.plantuml {
            font-family: 'monospace';
        }
        
        /* Markdown content */
        .markdown-content {
            margin: 1rem 0;
            padding: 0 1rem;
        }
        
        /* Footer */
        footer {
            text-align: center;
            padding: 2rem;
            color: #64748b;
        }
        
    </style>
</head>
<body>\n'''
        
        # Generate document body
        body = f'<div class="document">\n'
        
        # Add title
        body += f'    <h1>{title}</h1>\n'
        
        # Add markdown content (excluding diagram blocks)
        md_lines = md_content.split('\n')
        has_markdown = False
        
        i = 0
        while i < len(md_lines):
            line = md_lines[i]
            
            # Skip lines that would be part of diagram blocks
            if '```' in line:
                i += 1
                continue
            
            has_markdown = True
            body += f'    {line}\n'
            i += 1
        
        if has_markdown:
            body += '\n    <div class="markdown-content">\n'
            body += md_content
            body += '\n    </div>\n'
        
        # Add diagrams section
        if diagrams:
            body += '    <div class="diagram-container">\n'
            body += '        <div class="diagram-header">\n'
            body += '            <strong>Diagrams:</strong>\n'
            body += '        </div>\n'
            
            for diag in diagrams:
                body += f'        <div class="diagram-content {diag["type"].lower()}">\n'
                body += f'            <pre>{diag["content"].replace("\\n", "\\n")}</pre>\n'
                body += '        </div>\n'
            
            body += '    </div>\n'
        
        # Add diagram input if provided
        if diagram_input:
            body += '    <div class="diagram-container">\n'
            body += '        <div class="diagram-header">\n'
            body += '            <strong>Additional Diagram Input:</strong>\n'
            body += '        </div>\n'
            body += f'        <div class="diagram-content mermaid">\n'
            body += f'            <pre>{diagram_input[:2000].replace("\\n", "\\n")}</pre>\n'
            body += '        </div>\n'
            body += '    </div>\n'
        
        # Close document
        body += '</div>\n'
        
        # Footer
        footer = '''
</body>
</html>'''
        
        # Write output
        html_content = header + body + footer
        html_filename = os.path.basename(html_file)
        
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        print(f"Generated HTML: {html_filename}")
        
        if diagrams:
            print(f"Extracted {len(diagrams)} diagram(s)")
            for i, diag in enumerate(diagrams, 1):
                print(f"  {i}. {diag}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    md_file = sys.argv[1] if len(sys.argv) > 1 else '-'
    html_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Read diagram input if specified
    diagram_input = sys.argv[3] if len(sys.argv) > 3 else ""
    
    sys.exit(merge_diagrams_into_html(md_file, html_file, diagram_input))
