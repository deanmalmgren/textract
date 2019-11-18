import csv

from .utils import BaseParser, _call_with_kwargs


class Parser(BaseParser):
    """Extract text from comma separated values files (.csv).
    """

    delimiter = ','

    def extract(self, filename, **kwargs):

        # quick 'n dirty solution for the time being
        with open(filename) as stream:
            kwargs['delimiter'] = self.delimiter
            reader = _call_with_kwargs(csv.reader, stream, **kwargs)
            return '\n'.join(['\t'.join(row) for row in reader])
