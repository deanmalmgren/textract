import csv
import io

from .utils import DecodedParser


class Parser(DecodedParser):
    """Extract text from comma separated values files (.csv)."""

    delimiter = ","

    def extract_from_text(self, text, **kwargs):
        reader = csv.reader(io.StringIO(text), delimiter=self.delimiter)
        return "\n".join(["\t".join(row) for row in reader])

    def extract_from_lines(self, lines, **kwargs):
        """Beta streaming path (issue #97): ``csv.reader`` pulls rows one at
        a time from ``lines``, so with an explicit ``input_encoding`` this
        never buffers the whole file, only used with process_bytes/
        process_stream/``-`` stdin and an explicit ``--input-encoding``.
        """
        reader = csv.reader(lines, delimiter=self.delimiter)
        return "\n".join("\t".join(row) for row in reader)
