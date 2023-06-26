from .utils import BaseParser


class Parser(BaseParser):
    """Parse ``.txt`` files"""

    def extract(self, filename, **kwargs):
        with open(filename, encoding='latin-1') as stream:
            return stream.read()
