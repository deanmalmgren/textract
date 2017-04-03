"""
Route the request to the appropriate parser based on file type.
"""

import os
import importlib
import glob
import re

from .. import exceptions

# Dictionary structure for synonymous file extension types
EXTENSION_SYNONYMS = {
    ".jpeg": ".jpg",
    ".tff": ".tiff",
    ".tif": ".tiff",
    ".htm": ".html",
    "": ".txt",
    ".log": ".txt",
}

# default encoding that is returned by the process method. specify it
# here so the default is used on both the process function and also by
# the command line interface
DEFAULT_ENCODING = 'utf_8'

# filename format
_FILENAME_SUFFIX = '_parser'


def process(filename, encoding=DEFAULT_ENCODING, extension=None, **kwargs):
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
    # normally, file extension will be extracted from the file name
    # if the file name has no extension, then the user can pass the
    # extension as an argument
    if extension:
        ext = extension
        # check if the extension has the leading .
        if not ext.startswith('.'):
            ext = '.' + ext
        ext = ext.lower()
    else:
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

    # check the EXTENSION_SYNONYMS dictionary
    ext = EXTENSION_SYNONYMS.get(ext, ext)

    # to avoid conflicts with packages that are installed globally
    # (e.g. python's json module), all extension parser modules have
    # the _parser extension
    rel_module = ext + _FILENAME_SUFFIX

    # If we can't import the module, the file extension isn't currently
    # supported
    try:
        filetype_module = importlib.import_module(
            rel_module, 'textract.parsers'
        )
    except ImportError:
        raise exceptions.ExtensionNotSupported(ext)

    # do the extraction

    parser = filetype_module.Parser()
    return parser.process(filename, encoding, **kwargs)


def _get_available_extensions():
    """Get a list of available file extensions to make it easy for
    tab-completion and exception handling.
    """
    extensions = []

    # from filenames
    parsers_dir = os.path.join(os.path.dirname(__file__))
    glob_filename = os.path.join(parsers_dir, "*" + _FILENAME_SUFFIX + ".py")
    ext_re = re.compile(glob_filename.replace('*', "(?P<ext>\w+)"))
    for filename in glob.glob(glob_filename):
        ext_match = ext_re.match(filename)
        ext = ext_match.groups()[0]
        extensions.append(ext)
        extensions.append('.' + ext)

    # from relevant synonyms (don't use the '' synonym)
    for ext in EXTENSION_SYNONYMS.keys():
        if ext:
            extensions.append(ext)
            extensions.append(ext.replace('.', '', 1))
    extensions.sort()
    return extensions
