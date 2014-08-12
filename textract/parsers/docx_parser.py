import docx

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from docx file using python-docx.
    """

    def extract(self, filename, **kwargs):
        document = docx.Document(filename)
        return '\n\n'.join([
            paragraph.text for paragraph in document.paragraphs
        ])
