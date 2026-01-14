import docx2txt  # noqa: D100

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from docx file using python-docx."""

    def extract(self, filename, **kwargs):  # noqa: ANN001, ANN201, ARG002, D102, PLR6301
        return docx2txt.process(filename)
