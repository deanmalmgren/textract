from .csv_parser import Parser as BaseParser


class Parser(BaseParser):
    """Extract text from pipe separated values files (.psv).
    """

    delimiter = '|'
