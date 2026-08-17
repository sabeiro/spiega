import markdown
from markdown_mermaid import Extension as MermaidExtension
import sys, os, re
from bs4 import BeautifulSoup, Comment, NavigableString
from typing import List

new_ext = '.html'
file_path = sys.argv[1]
name, ext = os.path.splitext(file_path)
directory, filename = os.path.split(file_path)
with open(filename) as f:
    txtS = f.read()

# file_path = os.environ['HOME'] + '/lav/siti/spiega/markdown/activation.md'
# with open(file_path) as f:
#     txtS = f.read()

md = markdown.Markdown(extensions=['tables','abbr','fenced_code','footnotes','codehilite','meta','nl2br'])
htmS = md.convert(txtS)
# with open(directory + filename) as f:
#     txtS = f.read()
soup = BeautifulSoup(htmS, "html.parser")
headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

imgL = soup.find_all(["img"])
for img in imgL:
    imgTag = soup.new_tag("div",attrs={"class":"img_box"})
    img.wrap(imgTag)

htmlS = soup.prettify()
htmlS = re.sub("<h1>",'</section><h1>',htmlS)
htmlS = re.sub("</h1>",'</h1><section class="collapse">',htmlS)
htmlS = re.sub("<h2>",'</section><h2>',htmlS)
htmlS = re.sub("</h2>",'</h2><section class="collapse">',htmlS)
htmlS = re.sub("<h3>",'</section><h3>',htmlS)
htmlS = re.sub("</h3>",'</h3><section class="collapse">',htmlS)

htmlS = '<section class="collapse">' + htmlS + '</section>'

print(htmlS)

# with open("output.html","w") as f:
#     f.write(htmlS)


# for i, header in enumerate(headers):
#     level = int(re.match(r'h(\d)', header.name).group(1)) if re.match(r'h', header.name) else 0
#     level_class = f"section_level-{level}"
#     new_section = soup.new_tag("section",attrs={"class": level_class })

# section_pattern = re.compile(r"<section|\t*<h1", re.IGNORECASE)
# for tag_name in ["h1", "h2", "h3", "h4", "h5"]:
#     if tag_name not in soup:
#         for child in soup.children:
#             child = soup.find_all(tag_name + ">", stop=1)
#     if soup.find("header"):
#         for tag_name in TAGS_MAP:
#             parent = soup.find(tag_name)
#             child_wrapper = soup.new_string(f"<article class={'article-container'}>")
#         else:
#             soup.body.new_tag("article", class_="article-container")

# soup.prettify()
