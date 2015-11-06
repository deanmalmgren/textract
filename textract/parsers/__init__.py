"""
Route the request to the appropriate parser based on file type.
"""

import os
import importlib
import magic
import mimetypes

from .. import exceptions

# default encoding that is returned by the process method. specify it
# here so the default is used on both the process function and also by
# the command line interface
DEFAULT_ENCODING = 'utf_8'

def _get_extension(filename):
    """This function is used to get the extension of a filename, independent of
    whether the filename has an extension and return it in a preditable format
    (lower-case and always with a leading period).
    """

    # get the extension(s) from mimetype of the file
    try:
        mimetype = magic.from_file(filename, mime=True)
    except magic.MagicException:
        print exceptions.MimetypeNotDetected(filename)
    ext = mimetypes.guess_all_extensions(mimetype)
    if ext is None:
        raise exceptions.UnknownMimetypeExtension(filename, mimetype)
    return ext

def _check_mime(filename):
    """ This function checks the magic of a file referenced by ``filename``
    returns possible filename extension(s) based on detected mimetype 
    (could be a string or a list)
    """ 
    ext = []
    try:
        mimetype = magic.from_file(filename, mime=True)
        if mimetype:
            mimetype = mimetype.split(";")[0]
        if not mimetype:
            mimetype = None
    except:
        mimetype = None
    ext = mimetypes.guess_all_extensions(mimetype)    
    return ext

def process(filename, encoding=DEFAULT_ENCODING, **kwargs):
    """This is the core function used for extracting text. It routes the
    ``filename`` to the appropriate parser and returns the extracted
    text as a byte-string encoded with ``encoding``.
    """
    if not os.path.exists(filename):
        raise exceptions.MissingFileError(filename)
    # First we try to use file extension
    _, ext1 = os.path.splitext(filename)
    ext1 = ext1.lower()
    #print("ext1: %s" % ext1)
    # to avoid conflicts with packages that are installed globally
    # (e.g. python's json module), all extension parser modules have
    # the _parser extension

    ext3 = []
    ext2 = _check_mime(filename)
    #print("ext2: %s" % ext2)

    if isinstance(ext2, list):
        for i in ext2:
            ext3.append(i)
    else:
            ext3.append(ext2)

    if isinstance(ext1, list):
        for i in ext1:
            ext3.append(i)
    else:
            ext3.append(ext1)
    for ext in ext3:
        #print ("Processing ext: %s" % ext)
        if ext:
            rel_module = ext + '_parser'
            module_name = rel_module[1:]

            # if this module name doesn't exist in this directory it isn't
            # currently supported
            this_dir = os.path.dirname(os.path.abspath(__file__))
            if os.path.exists(os.path.join(this_dir, module_name + '.py')):
                #raise exceptions.ExtensionNotSupported(ext)

                # do the extraction
                filetype_module = importlib.import_module(rel_module, 'textract.parsers')
                #print ("Processing : %s" % filetype_module)
                parser = filetype_module.Parser()
                return parser.process(filename, encoding, **kwargs)
