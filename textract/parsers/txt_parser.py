from pathlib import Path

from .utils import BaseParser


class Parser(BaseParser):
    """Parse ``.txt`` files."""

    def extract(self, filename, **kwargs):
        with Path(filename).open("rb") as stream:
            return stream.read()
