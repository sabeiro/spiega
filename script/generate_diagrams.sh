#!/bin/bash
# Generate HTML from Mermaid diagrams automatically
# Usage: ./generate_diagrams.sh [diagrams_md_file] [theme] [output_html]
# Defaults: diagrams.md, default, diagrams.html

cd "$(dirname "$0")" || exit 1

# Arguments
DIAGRAMS="${1:-diagrams.md}"
THEME="${2:-default}"  # default or dark
OUTPUT="${3:-diagrams.html}"

# Set header common to all themes
HEADER='<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blender-MCP Diagrams</title>
  <script type="module">
    import mermaid from '"'"'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs'"'"';
    mermaid.initialize({
      startOnLoad: true,
      theme: '"'"${THEME}"'"',
      securityLevel: '"'"'loose'"'"'
    });
  </script>
  <style>
    .mermaid { background: var(--bg); border-radius: 8px; padding: 20px; margin: 20px; border: 1px solid var(--border); }
    h1, h2, h3 { color: var(--text-muted); }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    h1 { color: var(--primary); }
    h2 { color: var(--secondary); }
    body { background: var(--page-bg); color: var(--text); padding: 20px; }
  </style>
</head>
<body>
  <div style="max-width: 1200px; margin: 0 auto;">
    
    <h1>Blender-MCP ${THEME^}Diagram</h1>
    <p>Generated from: ${DIAGRAMS}</p>
    
'

# Initialize output file
> "$OUTPUT"

# Add header with proper casing
echo "${HEADER}" | sed 's/${THEME^}Diagram/$THEME Diagram/' > "$OUTPUT"

# Initialize a mermaid counter
M=1

# Read file line by line
while IFS= read -r line || [ -n "$line" ]; do
  # Check for mermaid code block start
  if echo "$line" | grep -q "^\\\`\`\\`mermaid\\`\\`"; then
    # Write closing div for previous diagram (if any)
    if [ $M -gt 1 ]; then
      echo "</div>" >> "$OUTPUT"
      echo "" >> "$OUTPUT"
    fi
    
    # Write opening div for new diagram
    echo "<div class=\"mermaid\" id=\"mermaid${M}\">" >> "$OUTPUT"
    
    # Increment counter
    M=$((M + 1))
    
    # Add comment for this diagram
    echo "# Diagram ${M}: " >> "$OUTPUT"
    
    # Output the diagram content
    echo "$line" >> "$OUTPUT"
    
  elif echo "$line" | grep -q "^\\\`\`\\`"; then
    # Code block end - close the div
    echo "</div>" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    
    echo "</div>" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    
  elif [ -z "$line" ]; then
    # Empty line
    echo "" >> "$OUTPUT"
    
  else
    # Normal line
    echo "$line" >> "$OUTPUT"
  fi
done < "$DIAGRAMS"

# Add footer
cat >> "$OUTPUT" << 'FOOTER'
    
  </div>
</body>
</html>
FOOTER

echo "✅ Generated: $OUTPUT (theme: $THEME)"
echo "   Source: $DIAGRAMS"
echo ""
echo "Commands to use:"
echo "  # View HTML file:"
echo "    xdg-open $OUTPUT"
echo ""
echo "  # Copy diagrams to your markdown:"
echo "    cp $OUTPUT ../../docs/diagrams/$(basename $OUTPUT)"
echo ""
echo "  # Share diagrams to GitHub/GitLab:"
echo "    cat ../diagrams.md >> your-docs.md"
