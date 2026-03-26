import csv
from pathlib import Path

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from comma separated values files (.csv)."""

    delimiter = ","

    def extract(self, filename, **kwargs):

        # quick 'n dirty solution for the time being
        with Path(filename).open(encoding="utf-8") as stream:
            reader = csv.reader(stream, delimiter=self.delimiter)
            return "\n".join(["\t".join(row) for row in reader])
