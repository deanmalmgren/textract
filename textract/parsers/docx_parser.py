import docx2txt

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from docx file using python-docx.
    """

    def extract(self, filename, **kwargs):
        return docx2txt.process(filename)
