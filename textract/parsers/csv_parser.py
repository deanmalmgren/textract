import csv
import io
from pathlib import Path

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from comma separated values files (.csv)."""

    delimiter = ","

    def extract(self, filename, input_encoding=None, **kwargs):
        raw_bytes = Path(filename).read_bytes()
        text = self.decode(raw_bytes, input_encoding)
        reader = csv.reader(io.StringIO(text), delimiter=self.delimiter)
        return "\n".join(["\t".join(row) for row in reader])
