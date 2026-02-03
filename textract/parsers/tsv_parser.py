from .csv_parser import Parser as BaseParser


class Parser(BaseParser):
    """Extract text from tab separated values files (.tsv).
    """

    delimiter = '\t'
