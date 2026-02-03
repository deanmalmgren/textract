from .utils import BaseParser


class Parser(BaseParser):
    """Parse ``.txt`` files"""

    def extract(self, filename, **kwargs):
        with open(filename, errors='ignore') as stream:
            return stream.read()
