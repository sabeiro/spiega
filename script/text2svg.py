import sys, os, re, json, io
from svgpathtools import wsvg, Line, QuadraticBezier, Path, path
from xml.etree import ElementTree as ET
from xml.dom import minidom
from freetype import Face
import cairo
from bs4 import BeautifulSoup

face = Face('/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Regular.ttf')
face.set_char_size(48 * 64)

try:
    svgF = sys.argv[1]
except:
    svgF = os.environ['HOME'] + '/lav/siti/f/f_twin/arch_diagram.svg'

with open(svgF) as f:
    svgS = f.read()

dom = minidom.parse(svgF)
root = dom.documentElement
ns = {'svg': 'http://www.w3.org/2000/svg'}
tree = ET.parse(svgF)
root = tree.getroot()
text_elems = root.findall('.//svg:text', ns)
textL = []
###### parse text as text tag
for text_elem in root.findall('.//{http://www.w3.org/2000/svg}text'):
    text = text_elem.text or ""
    if text == "":
        tspan_texts = [ts.text for ts in text_elem.findall('.//{http://www.w3.org/2000/svg}tspan') if ts.text]
        child_elements = list(text_elem)
        tspan_elements = text_elem.findall('.//{http://www.w3.org/2000/svg}tspan')
        if not tspan_elements:
            tspan_elements = text_elem.findall('.//tspan')
        text = tspan_elements[0].text
    x = float(text_elem.get('x', 0))
    y = float(text_elem.get('y', 0))
    font_size = float(text_elem.get('font-size', '14').split('px')[0] or '14')
    width = int(font_size * len(text)/4)
    height = int(font_size/2)
    path_data = f"M {x},{y} L {x+width},{y} L {x+width},{y+height} L {x},{y+height} Z"
    textX = f"<path d=\"{path_data}\" fill=\"{text_elem.get('fill', '#000000')}\" style=\"fill:{text_elem.get('fill', '#000000')}\"/>"
    textL.append({"text":text,"bbox":textX,"x":x-width,"y":y+height,"size":font_size})
    # Remove text element from DOM
    # if text_elem.parentElement:
    #     text_elem.parentElement.removeChild(text_elem)
###### parse text as edgeLabel
def parse_transform(transform_str):
    m = re.search(r'translate\(([-\d.]+),\s*([-\d.]+)\)', transform_str)
    if m:
        return float(m.group(1)), float(m.group(2))
    return 0.0, 0.0

ns = {'svg': 'http://www.w3.org/2000/svg', 'xhtml': 'http://www.w3.org/1999/xhtml'}
for sel, label_class in [('svg:g[@class="edgeLabel"]', 'edgeLabel'),
                          ('svg:g[@class="node default"]', 'nodeLabel')]:
    for g in root.findall(f'.//{sel}', ns):
        outer_x, outer_y = parse_transform(g.get('transform', ''))
        inner_g = g.find('svg:g[@class="label"]', ns)
        if inner_g is not None:
            sub_x, sub_y = parse_transform(inner_g.get('transform', ''))
        else:
            sub_x, sub_y = 0.0, 0.0
        abs_x = outer_x + sub_x
        abs_y = outer_y + sub_y
        text = g.find('.//xhtml:p', ns)
        text_content = text.text.strip() if text is not None and text.text else ''
        font_size = float(g.get('font-size', '14').split('px')[0] or '14')
        width = int(font_size * len(text)/4)
        height = int(font_size/2)
        x = int(outer_x + sub_x)
        y = int(outer_y + sub_y)
        textL.append({"text":text_content,"bbox":"","x":x-width,"y":y+height,"size":font_size})

# tree = ET.parse(svgF)
# root = tree.getroot()
# for text_elem in root.getElementsByTagName('text'):
#     parent = text_elem.parentNode
#     print(text_elem)
    # if parent:
    #     parent.removeChild(text_elem)
    # xml_content = dom.toprettyxml()
    # if isinstance(xml_content, bytes):
    #     xml_content = xml_content.decode('utf-8')

size = [int(float(x)) for x in root.attrib['viewBox'].split(" ")]
#surface = cairo.SVGSurface("output.svg", size[2], size[3])

with cairo.SVGSurface("output.svg", size[2], size[3]) as surface:
    Context = cairo.Context(surface)
    for t in textL:
        Context.set_source_rgb(1, 0, 0)
        Context.set_font_size(t['size'])
        Context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        Context.move_to(t['x'], t['y'])
        Context.text_path(t['text'])
        Context.set_line_width(.5)
        #Context.stroke()
        Context.fill()
    #Context.save()


labelL = []
with open("output.svg", "r") as file:
    content = file.read()
soup = BeautifulSoup(content,'xml')
source_svg = soup.find('svg')
for s in source_svg.contents:
    labelL.append(s)
    
with open(svgF) as f:
    svgS = f.read()
soup = BeautifulSoup(svgS,'xml')
target_svg = soup.find('svg')
for text in soup.find_all('text'):
    text.decompose()
for i,s in enumerate(target_svg.contents):
    try:
        s.attrs.update({'id':s.attrs['class'] + "_" + str(i)})
    except:
        pass

new_group = soup.new_tag('g')
new_group['class'] = 'label-group'
for i,s in enumerate(labelL):
    try:
        s.attrs.update({'id':'text_' + str(i)})
    except:
        pass
    new_group.append(s)
target_svg.append(new_group)
with open('output.svg', 'w') as file:
    file.write(str(target_svg))

print("File processed: " + svgF + "results in output.svg")








    
#inner_html = str(source_svg.encode_contents())
#text_label = soup.new_tag(name="path")
#text_label.string = inner_html
#text_label = BeautifulSoup(inner_html, 'xml')
#svg.insert(0, text_label)
#svg.append(text_label)



def tuple_to_imag(t):
    return t[0] + t[1] * 1j

def conv_char(char):
    face.load_char(char)
    face.get_kerning('a', 'b')
    outline = face.glyph.outline
    y = [t[1] for t in outline.points]
    outline_points = [(p[0], max(y) - p[1]) for p in outline.points] # flip the points
    start, end = 0, 0
    paths = []
    for i in range(len(outline.contours)):
        end = outline.contours[i]
        points = outline_points[start:end + 1]
        points.append(points[0])
        tags = outline.tags[start:end + 1]
        tags.append(tags[0])
        segments = [[points[0], ], ]
        for j in range(1, len(points)):
            segments[-1].append(points[j])
            if tags[j] and j < (len(points) - 1):
                segments.append([points[j], ])
        for segment in segments:
            if len(segment) == 2:
                paths.append(Line(start=tuple_to_imag(segment[0]),
                                  end=tuple_to_imag(segment[1])))
            elif len(segment) == 3:
                paths.append(QuadraticBezier(start=tuple_to_imag(segment[0]),
                                         control=tuple_to_imag(segment[1]),
                                         end=tuple_to_imag(segment[2])))
            elif len(segment) == 4:
                C = ((segment[1][0] + segment[2][0]) / 2.0,
                     (segment[1][1] + segment[2][1]) / 2.0)

                paths.append(QuadraticBezier(start=tuple_to_imag(segment[0]),
                                             control=tuple_to_imag(segment[1]),
                                             end=tuple_to_imag(C)))
                paths.append(QuadraticBezier(start=tuple_to_imag(C),
                                             control=tuple_to_imag(segment[2]),
                                             end=tuple_to_imag(segment[3])))
        start = end + 1
    path = Path(*paths)
    return path

# path = conv_char(textS[0])
# wsvg(path, filename="text.svg")

# with open(textS + ".svg","w") as f:
#     f.write(text_to_path(textS))
