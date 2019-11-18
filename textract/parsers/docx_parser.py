import docx2txt

from .utils import BaseParser, _call_with_kwargs


class Parser(BaseParser):
    """Extract text from docx file using python-docx.
    """

    def extract(self, filename, **kwargs):
        return _call_with_kwargs(docx2txt.process, filename, **kwargs)
