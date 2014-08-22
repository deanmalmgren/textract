"""
Use argparse to handle command-line arguments.
"""

import argparse
import encodings
import os
import pkgutil

import argcomplete

from . import VERSION
from .parsers import DEFAULT_ENCODING


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
        '-e', '--encoding', type=str, default=DEFAULT_ENCODING,
        choices=_get_available_encodings(),
        help='Specify the encoding of the output.',
    )
    parser.add_argument(
        '-m', '--method', default='',
        help='specify a method of extraction for formats that support it',
    )
    parser.add_argument(
        '-o', '--output', type=argparse.FileType('w'), default='-',
        help='output raw text in this file',
    )
    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s '+VERSION,
    )

    # enable autocompletion with argcomplete
    argcomplete.autocomplete(parser)

    return parser


def _get_available_encodings():
    """Get a list of the available encodings to make it easy to
    tab-complete the command line interface.

    Inspiration from http://stackoverflow.com/a/3824405/564709
    """
    available_encodings = set(encodings.aliases.aliases.values())
    paths = [os.path.dirname(encodings.__file__)]
    for importer, modname, ispkg in pkgutil.walk_packages(path=paths):
        available_encodings.add(modname)
    available_encodings = list(available_encodings)
    available_encodings.sort()
    return available_encodings
