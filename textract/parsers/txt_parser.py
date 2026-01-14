import pathlib  # noqa: D100

from .utils import BaseParser


class Parser(BaseParser):
    """Parse ``.txt`` files."""

    def extract(self, filename, **kwargs):  # noqa: ANN001, ANN201, ARG002, D102, PLR6301
        with pathlib.Path(filename).open("rb") as stream:  # noqa: FURB101
            return stream.read()
