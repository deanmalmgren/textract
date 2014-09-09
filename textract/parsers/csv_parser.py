import csv

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from .csv files. Whenever possible, this ignores
    header lines (which is considered markup for the csv).
    """

    def extract(self, filename, **kwargs):

        with open(filename, 'rb') as csv_file:

            # detect csv delimiter
            delimiter = self.detect_delimiter(csv_file)

            csv_reader = csv.reader(csv_file, delimiter=delimiter)

            # detect dialect and header line
            # TODO: detection is not accurate enough
            '''
            sniffer = csv.Sniffer()
            csv_sample = csv_file.read(1024)
            csv_file.seek(0)
            dialect = sniffer.sniff(csv_sample)
            csv_reader = csv.reader(csv_file, dialect)
            if sniffer.has_header(csv_sample):
                next(csv_reader)
            '''

            rows = ['\t'.join(row) for row in csv_reader]
            output = '\n'.join(rows)
            output += '\n'  # make output cleaner

            return output

    def detect_delimiter(self, csv_file):
        """Simple, custom delimiter detection"""

        delimiters = [',', ';', '|', '\t']

        # use first line to detect delimiter
        # assumes first column has no conflicting punctuation usage
        line = next(csv_file.xreadlines())
        csv_file.seek(0)

        for c in line:
            if c in delimiters:
                return c
        else:
            return ''
