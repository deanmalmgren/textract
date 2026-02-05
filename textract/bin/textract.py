"""Command-line application."""

import sys

from textract import process
from textract.cli import get_parser
from textract.colors import red
from textract.exceptions import CommandLineError


# extract text
def main() -> None:
    """Interpret the command-line arguments, process the document and
    raise errors accordingly (with traceback surpressed).
    """
    parser = get_parser()
    args = parser.parse_args()
    try:
        output = process(**vars(args))
    except CommandLineError as ex:
        sys.stderr.write(red(ex) + '\n')
        sys.exit(1)
    else:
        args.output.write(output)
