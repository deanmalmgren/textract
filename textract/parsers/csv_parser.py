import csv
import io

from .utils import NativeParser


class Parser(NativeParser):
    """Extract text from comma separated values files (.csv)."""

    delimiter = ","

    def extract_from_text(self, text, **kwargs):
        reader = csv.reader(io.StringIO(text), delimiter=self.delimiter)
        return "\n".join(["\t".join(row) for row in reader])
