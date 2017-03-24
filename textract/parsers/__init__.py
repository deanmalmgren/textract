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
    # if no extension passed, extract the extension from the file
    # else use the passed extension (useful for files without extension)
    if 'extension' in kwargs:
        ext = kwargs['extension']
        print('ext:', ext)
    else:
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
    # if the extension has not the leading . , add it to the ext variable
    if not ext[0] == '.':
        ext = '.' + ext
    # check the EXTENSION_SYNONYMS dictionary
    ext = EXTENSION_SYNONYMS.get(ext, ext)

    # to avoid conflicts with packages that are installed globally
    # (e.g. python's json module), all extension parser modules have
    # the _parser extension
    rel_module = ext + '_parser'

    # If we can't import the module, the file extension isn't currently
    # supported
    try:
        filetype_module = importlib.import_module(
            rel_module, 'textract.parsers')
    except ImportError:
        raise exceptions.ExtensionNotSupported(ext)

    # do the extraction

    parser = filetype_module.Parser()
    return parser.process(filename, encoding, **kwargs)
