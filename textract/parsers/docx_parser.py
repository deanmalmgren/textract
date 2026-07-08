import io

import docx2txt

from .utils import BytesParser


class Parser(BytesParser):
    """Extract text from docx file using docx2txt."""

    def extract_from_bytes(self, data, **kwargs):
        return docx2txt.process(io.BytesIO(data))
