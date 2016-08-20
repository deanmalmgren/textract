"""
Route the request to the appropriate parser based on file type.
"""

import os
import importlib

from .. import exceptions
from .filetype import detect_filetype


# default encoding that is returned by the process method. specify it
# here so the default is used on both the process function and also by
# the command line interface
DEFAULT_ENCODING = 'utf_8'


def process(filename, encoding=DEFAULT_ENCODING, **kwargs):
    """This is the core function used for extracting text. It routes the
    ``filename`` to the appropriate parser and returns the extracted
    text as a byte-string encoded with ``encoding``.
    """

    # make sure the filename exists
    if not os.path.exists(filename):
        raise exceptions.MissingFileError(filename)

    ext = detect_filetype(filename)

    # to avoid conflicts with packages that are installed globally
    # (e.g. python's json module), all extension parser modules have
    # the _parser extension
    module_name = ext + '_parser'

    ## If it can't find the module, it's an unsupported file type
    try:
        import_path = 'textract.parsers.' + module_name
        filetype_module = importlib.import_module(import_path)
    except ImportError:
        raise exceptions.ExtensionNotSupported(ext)

    # do the extraction
    parser = filetype_module.Parser()
    return parser.process(filename, encoding, **kwargs)
