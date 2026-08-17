#!/usr/bin/env python3
#===============================================================================
# org2slide.py - Convert org-mode presentations to HTML slides
#===============================================================================

import sys
import os, sys
import re
from bs4 import BeautifulSoup

baseDir = os.environ['HOME'] + '/lav/src/spiega/'

with open(sys.argv[1]) as f:
    htmlS = f.read()
    
soup = BeautifulSoup(htmlS, 'html.parser')
body = soup.find('body').decode_contents()

#with open(baseDir + "static_html/template/header.html") as f:
#    headS = f.read()
#with open(baseDir + "static_html/template/footer.html") as f:
#    footS = f.read()

with open(sys.argv[1],"w") as f:
    #f.write(headS + str(body) + footS)
    f.write(str(body))

