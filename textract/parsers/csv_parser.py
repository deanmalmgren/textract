import csv
import io

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from comma separated values files (.csv)."""

    delimiter = ","
    needs_decoded_text = True

    def extract_from_text(self, text, **kwargs):
        reader = csv.reader(io.StringIO(text), delimiter=self.delimiter)
        return "\n".join(["\t".join(row) for row in reader])
