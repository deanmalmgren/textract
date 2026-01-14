"""Command-line application."""

import sys

from .. import process
from ..cli import get_parser
from ..colors import red
from ..exceptions import CommandLineError


# extract text
def main():
    """Interpret the command-line arguments, process the document and
    raise errors accordingly (with traceback surpressed).
    """
    parser = get_parser()
    args = parser.parse_args()
    try:
        output = process(**vars(args))
    except CommandLineError as ex:
        sys.stderr.write(red(ex) + "\n")
        sys.exit(1)
    else:
        args.output.write(output)
