from lxml import etree
from io import BytesIO,StringIO
import re

def url(string):
    Url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return Url

s_path = raw_input("Enter the file name: ")
tree = etree.parse(s_path)
root = tree.getroot()
build = root.tag
url1 = url(build)
print url1[0]
count = 0
for element in tree.iter():
    if element.tag == '{' + url1[0] + '}p':
        element.attrib["id"] = str(count)
        count += 1
print etree.tostring(tree, pretty_print = True, method = "xml")
