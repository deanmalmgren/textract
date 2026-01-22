"""Use argparse to handle command-line arguments."""

import argparse
import encodings
import pathlib
import pkgutil
import sys

import argcomplete
import six

from . import VERSION
from .parsers import DEFAULT_ENCODING, _get_available_extensions


class AddToNamespaceAction(argparse.Action):
    """This adds KEY,VALUE arbitrary pairs to the argparse.Namespace object."""

    def __call__(self, parser, namespace, values, option_string=None):  # noqa: ANN001, ANN204, D102
        assert isinstance(values, str)  # noqa: S101
        key, val = values.strip().split("=")
        if hasattr(namespace, key):
            parser.error(
                ('Duplicate specification of the key "{key}" with --option.').format(
                    **locals(),
                ),
            )
        setattr(namespace, key, val)


# Fix FileType to honor 'b' flag, see: https://bugs.python.org/issue14156
class FileType(argparse.FileType):  # noqa: D101
    def __call__(self, string):  # noqa: ANN001, ANN204, D102
        if string == "-" and six.PY3:  # noqa: YTT202
            if "r" in self._mode:
                fileno = sys.stdin.fileno()
                return open(  # noqa: PTH123
                    fileno,
                    self._mode,
                    self._bufsize,
                    self._encoding,
                    self._errors,
                )  # noqa: RUF100, SIM115
            if "w" in self._mode:
                fileno = sys.stdout.fileno()
                return open(  # noqa: PTH123
                    fileno,
                    self._mode,
                    self._bufsize,
                    self._encoding,
                    self._errors,
                )  # noqa: RUF100, SIM115
        return super().__call__(string)


# This function is necessary to enable autodocumentation of the script
# output
def get_parser():  # noqa: ANN201
    """Initialize the parser for the command line interface and bind the
    autocompletion functionality.
    """  # noqa: D205
    # initialize the parser
    parser = argparse.ArgumentParser(
        description="Command line tool for extracting text from any document. ",
    )

    # define the command line options here
    parser.add_argument(
        "filename",
        help="Filename to extract text.",
    ).completer = argcomplete.completers.FilesCompleter  # type: ignore[attr-defined]
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


def _get_available_encodings():  # noqa: ANN202
    """Get a list of the available encodings to make it easy to
    tab-complete the command line interface.

    Inspiration from http://stackoverflow.com/a/3824405/564709
    """  # noqa: D205
    available_encodings = set(encodings.aliases.aliases.values())
    paths = [str(pathlib.Path(encodings.__file__).parent)]
    available_encodings.update(
        modname for importer, modname, ispkg in pkgutil.walk_packages(path=paths)
    )
    available_encodings = list(available_encodings)
    available_encodings.sort()
    return available_encodings
