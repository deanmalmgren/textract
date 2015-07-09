import csv

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from .csv files. Whenever possible, this ignores
    header lines (which is considered markup for the csv).
    """

    def extract(self, filename, **kwargs):

        # TODO: it would be pretty awesome to not have to specify the
        # dialect (delimiters) for the CSV and be able to sniff the
        # dialect using the csv.Sniffer, but this doesn't work on the
        # raw_text.csv test at the moment...

        # # sniff the dialect using python's csv.Sniffer. takes
        # # inspiration from http://www.dotnetperls.com/csv
        # with open(filename) as stream:

        #     # get a sample of the text from the stream and then go
        #     # back to the beginning of the stream
        #     sample = ''
        #     for i, line in enumerate(stream):
        #         sample += line
        #         if i==10: break
        #     stream.seek(0)

        #     # use csv.Sniffer to determine the dialect (what
        #     # delimiters are used) and to determine if the file has a
        #     # header row
        #     sniffer = csv.Sniffer()
        #     dialect = sniffer.sniff(sample)
        #     if sniffer.has_header(sample):
        #         stream.readline()

        #     # assemble the result
        #     reader = csv.reader(stream, dialect)
        #     return '\n'.join(['\t'.join(row) for row in reader])

        # quick 'n dirty solution for the time being
        with open(filename) as stream:
            reader = csv.reader(stream)
            return '\n'.join(['\t'.join(row) for row in reader])
