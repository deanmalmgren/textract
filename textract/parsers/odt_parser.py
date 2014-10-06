import zipfile
import xml.etree.ElementTree as ET
import StringIO

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from open document files.
    """

    def extract(self, filename, **kwargs):
        with open(filename) as stream:
            zip_stream = zipfile.ZipFile(stream)
            self.content = ET.fromstring(zip_stream.read("content.xml"))
        return self.to_string()

    def to_string(self):
        """ Converts the document to a string. """
        buff = u""
        for child in self.content.iter():
            if child.tag in [self.qn('text:p'), self.qn('text:h')]:
                buff += self.text_to_string(child) + "\n"
        # remove last newline char
        if buff:
            buff = buff[:-1]
        return buff

    def text_to_string(self, element):
        buff = u""
        if element.tag == self.qn('text:tab'):
            buff = "\t"
            if element.tail is not None:
                buff += element.tail
            return buff
        if element.tag == self.qn('text:s'):
            buff = u" "
            if element.get(self.qn('text:c')) is not None:
                buff *= int(element.get(self.qn('text:c')))
            if element.tail is not None:
                buff += element.tail
            return buff
        if element.text:
            buff += element.text
        for child in element:
            buff += self.text_to_string(child)
        if element.tail is not None:
            buff += element.tail
        return buff

    def qn(self, namespace):
        nsmap = {
            'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        }
        spl = namespace.split(':')
        return '{{{}}}{}'.format(nsmap[spl[0]], spl[1])
