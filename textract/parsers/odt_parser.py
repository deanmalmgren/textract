import zipfile
import xml.dom.minidom
import StringIO

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from open document files.
    """

    def extract(self, filename, **kwargs):
        # Inspiration from
        # https://github.com/odoo/odoo/blob/master/addons/document/odt2txt.py
        with open(filename) as stream:
            zip_stream = zipfile.ZipFile(stream)
            self.content = xml.dom.minidom.parseString(
                zip_stream.read("content.xml")
            )

        return self.to_string()

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
