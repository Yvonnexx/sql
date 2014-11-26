#!/usr/bin/python
from lxml import etree
import sys

tree = etree.parse(sys.argv[1])
root = tree.getroot()
print(etree.tostring(tree, pretty_print=True))

