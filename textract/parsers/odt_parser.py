import zipfile
import xml.dom.minidom
import StringIO

def extract(filename, **kwargs):
    """Extract text from open document files.
    """
    obj = StringIO.StringIO(file(filename).read())
    odt = OpenDocumentTextFile(obj)
    return odt.to_string().encode('ascii', 'replace')


class OpenDocumentTextFile(object):
    """
    Inspiration from
    https://github.com/odoo/odoo/blob/master/addons/document/odt2txt.py
    """
    def __init__(self, filepath):
        obj = zipfile.ZipFile(filepath)
        self.content = xml.dom.minidom.parseString(obj.read("content.xml"))

    def to_string(self):
        """ Converts the document to a string. """
        buff = u""
        for val in ["text:p", "text:h", "text:list"]:
            for paragraph in self.content.getElementsByTagName(val):
                buff += self.text_to_string(paragraph) + "\n"
        return buff

    def text_to_string(self, element):
        buff = u""
        for node in element.childNodes:
            if node.nodeType == xml.dom.Node.TEXT_NODE:
                buff += node.nodeValue
            elif node.nodeType == xml.dom.Node.ELEMENT_NODE:
                buff += self.text_to_string(node)
        return buff
