"""
Use argparse to handle command-line arguments.
"""

import argparse
import encodings
import pkgutil
import sys
from pathlib import Path

import argcomplete

from . import VERSION
from .parsers import DEFAULT_ENCODING, _get_available_extensions


class AddToNamespaceAction(argparse.Action):
    """This adds KEY,VALUE arbitrary pairs to the argparse.Namespace object"""

    def __call__(self, parser, namespace, values, option_string=None):
        assert isinstance(values, str)  # for pyright
        key, val = values.strip().split("=")
        if hasattr(namespace, key):
            parser.error(
                ('Duplicate specification of the key "%(key)s" with --option.')
                % locals()
            )
        setattr(namespace, key, val)


# Fix FileType to honor 'b' flag, see: https://bugs.python.org/issue14156
class FileType(argparse.FileType):
    def __call__(self, string):
        if string == "-":
            if "r" in self._mode:
                return sys.stdin.buffer if "b" in self._mode else sys.stdin
            if "w" in self._mode:
                return sys.stdout.buffer if "b" in self._mode else sys.stdout
        return super().__call__(string)


# This function is necessary to enable autodocumentation of the script
# output
def get_parser():
    """Initialize the parser for the command line interface and bind the
    autocompletion functionality"""

    # initialize the parser
    parser = argparse.ArgumentParser(
        description="Command line tool for extracting text from any document.",
    )

    # define the command line options here
    filename_action = parser.add_argument(
        "filename",
        help="Filename to extract text.",
    )
    filename_action.completer = argcomplete.completers.FilesCompleter  # type: ignore[attr-defined]
    parser.add_argument(
        "-e",
        "--encoding",
        type=str,
        default=DEFAULT_ENCODING,
        choices=_get_available_encodings(),
        help="Specify the encoding of the output.",
    )
    parser.add_argument(
        "--extension",
        type=str,
        default=None,
        choices=_get_available_extensions(),
        help="Specify the extension of the file.",
    )
    parser.add_argument(
        "-m",
        "--method",
        default="",
        help="Specify a method of extraction for formats that support it",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=FileType("wb"),
        default="-",
        help="Output raw text in this file",
    )
    parser.add_argument(
        "-O",
        "--option",
        type=str,
        action=AddToNamespaceAction,
        help=(
            "Add arbitrary options to various parsers of the form "
            "KEYWORD=VALUE. A full list of available KEYWORD options is "
            "available at http://bit.ly/textract-options"
        ),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + VERSION,
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
    paths = [str(Path(encodings.__file__).parent)]
    available_encodings.update(
        modname for importer, modname, ispkg in pkgutil.walk_packages(path=paths)
    )
    available_encodings = list(available_encodings)
    available_encodings.sort()
    return available_encodings
