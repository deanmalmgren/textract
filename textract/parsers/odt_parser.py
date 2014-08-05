import sys
import zipfile
import xml.dom.minidom
import StringIO


def extract(filename, **kwargs):
    s = StringIO.StringIO(file(filename).read())
    odt = OpenDocumentTextFile(s)
    return odt.toString().encode('ascii', 'replace')


class OpenDocumentTextFile:
    def __init__(self, filepath):
        zip = zipfile.ZipFile(filepath)
        self.content = xml.dom.minidom.parseString(zip.read("content.xml"))

    def toString(self):
        """ Converts the document to a string. """
        buffer = u""
        for val in ["text:p", "text:h", "text:list"]:
            for paragraph in self.content.getElementsByTagName(val):
                buffer += self.textToString(paragraph) + "\n"
        return buffer

    def textToString(self, element):
        buffer = u""
        for node in element.childNodes:
            if node.nodeType == xml.dom.Node.TEXT_NODE:
                buffer += node.nodeValue
            elif node.nodeType == xml.dom.Node.ELEMENT_NODE:
                buffer += self.textToString(node)
        return buffer
