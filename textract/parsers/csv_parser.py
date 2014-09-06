import csv

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from .csv files. Whenever possible, this ignores
    header lines (which is considered markup for the csv).
    """

    def extract(self, filename, **kwargs):

        with open(filename, 'rb') as csv_file:

            sniffer = csv.Sniffer()

            # detect csv dialect info
            csv_sample = str(csv_file.readlines()[0:2])
            dialect = sniffer.sniff(str(csv_sample))

            csv_file.seek(0)
            csv_reader = csv.reader(csv_file, dialect)

            # skip header line, if present
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
