import pathlib  # noqa: D100

from .utils import BaseParser


class Parser(BaseParser):
    """Parse ``.txt`` files."""

    def extract(self, filename, **kwargs):
        with pathlib.Path(filename).open("rb") as stream:  # noqa: FURB101
            return stream.read()
