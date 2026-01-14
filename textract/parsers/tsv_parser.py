from .csv_parser import Parser as BaseParser  # noqa: D100


class Parser(BaseParser):
    """Extract text from tab separated values files (.tsv)."""

    delimiter = "\t"
