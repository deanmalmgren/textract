import csv

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from .csv files. Whenever possible, this ignores
    header lines (which is considered markup for the csv).
    """

    delimiter = ','

    def extract(self, filename, **kwargs):

        # quick 'n dirty solution for the time being
        with open(filename) as stream:
            reader = csv.reader(stream, delimiter=self.delimiter)
            return '\n'.join(['\t'.join(row) for row in reader])
