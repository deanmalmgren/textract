import argparse

import argcomplete

from . import VERSION


# This function is necessary to enable autodocumentation of the script
# output
def get_parser():
    """Initialize the parser for the command line interface and bind the
    autocompletion functionality"""

    # initialize the parser
    parser = argparse.ArgumentParser(
        description=(
            'Command line tool for extracting text from any document. '
        ) % locals(),
    )

    # define the command line options here
    parser.add_argument(
        'filename', help='Filename to extract text.',
    ).completer = argcomplete.completers.FilesCompleter
    parser.add_argument(
        '-o', '--output', type=argparse.FileType('w'), default='-',
        help='output raw text in this file',
    )
    parser.add_argument(
        '-m', '--method', default='',
        help='specify a method of extraction for formats that support it',
    )
    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s '+VERSION,
    )

    # enable autocompletion with argcomplete
    argcomplete.autocomplete(parser)

    return parser
