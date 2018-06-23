from lxml import etree

file = raw_input("Enter the file: ")
parser = etree.XMLParser(remove_blank_text = True)
xml = etree.parse(file, parser)

build = etree.XPath("//text()")
print build(xml)
