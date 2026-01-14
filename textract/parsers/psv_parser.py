from .csv_parser import Parser as BaseParser  # noqa: D100


class Parser(BaseParser):
    """Extract text from pipe separated values files (.psv)."""

    delimiter = "|"
