import csv

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from .csv files. Whenever possible, this ignores
    header lines (which is considered markup for the csv).
    """

    def extract(self, filename, **kwargs):

        with open(filename, 'rb') as csv_file:

            sniffer = csv.Sniffer()

            # prepare csv sample
            lines = csv_file.xreadlines()
            csv_sample = [next(lines) for _ in xrange(2)]
            csv_file.seek(0)

            # detect csv dialect
            dialect = sniffer.sniff(str(csv_sample))

            csv_reader = csv.reader(csv_file, dialect)

            # detect header line, and skip
            # TODO: header detection is not accurate enough
            # fails on standardized_text.csv
            '''
            if sniffer.has_header(csv_sample):
                next(csv_reader)
            '''

            rows = ['\t'.join(row) for row in csv_reader]
            output = '\n'.join(rows)
            output += '\n'  # make output cleaner

            return output
