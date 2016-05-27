"""
Route the request to the appropriate parser based on file type.
"""

import os
import importlib

from .. import exceptions

# Dictionary structure for synonymous file extension types
EXTENSION_SYNONYMS = {
    ".jpeg": ".jpg",
    ".htm": ".html",
    "": ".txt",
    ".tif": ".tiff",
}

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

    # get the filename extension, which is something like .docx for
    # example, and import the module dynamically using importlib. This
    # is a relative import so the name of the package is necessary
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    # check the EXTENSION_SYNONYMS dictionary
    ext = EXTENSION_SYNONYMS.get(ext, ext)

    # to avoid conflicts with packages that are installed globally
    # (e.g. python's json module), all extension parser modules have
    # the _parser extension
    rel_module = ext + '_parser'
    module_name = rel_module[1:]

    # if this module name doesn't exist in this directory it isn't
    # currently supported
    this_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(this_dir, module_name + '.py')):
        raise exceptions.ExtensionNotSupported(ext)

    # do the extraction
    filetype_module = importlib.import_module(rel_module, 'textract.parsers')
    parser = filetype_module.Parser()
    return parser.process(filename, encoding, **kwargs)
