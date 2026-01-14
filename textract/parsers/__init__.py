"""Route the request to the appropriate parser based on file type."""  # noqa: EXE002

import glob
import importlib
import pathlib
import re

from textract import exceptions

# Dictionary structure for synonymous file extension types
EXTENSION_SYNONYMS = {  # noqa: RUF067
    ".jpeg": ".jpg",
    ".tff": ".tiff",
    ".tif": ".tiff",
    ".htm": ".html",
    "": ".txt",
    ".log": ".txt",
    ".tab": ".tsv",
}

# default encoding that is returned by the process method. specify it
# here so the default is used on both the process function and also by
# the command line interface
DEFAULT_OUTPUT_ENCODING = "utf_8"  # noqa: RUF067
DEFAULT_ENCODING = "utf_8"  # noqa: RUF067

# filename format
_FILENAME_SUFFIX = "_parser"  # noqa: RUF067


def process(  # noqa: ANN201, RUF067
    filename,  # noqa: ANN001
    input_encoding=None,  # noqa: ANN001
    output_encoding=DEFAULT_OUTPUT_ENCODING,  # noqa: ANN001
    extension=None,  # noqa: ANN001
    **kwargs,
):
    """This is the core function used for extracting text. It routes the
    ``filename`` to the appropriate parser and returns the extracted
    text as a byte-string encoded with ``encoding``.
    """  # noqa: D205
    # make sure the filename exists
    if not pathlib.Path(filename).exists():
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
        if not ext.startswith("."):
            ext = "." + ext
        ext = ext.lower()
    else:
        ext = pathlib.Path(filename).suffix.lower()

    # check the EXTENSION_SYNONYMS dictionary
    ext = EXTENSION_SYNONYMS.get(ext, ext)

    # to avoid conflicts with packages that are installed globally
    # (e.g. python's json module), all extension parser modules have
    # the _parser extension
    rel_module = ext + _FILENAME_SUFFIX

    # If we can't import the module, the file extension isn't currently
    # supported
    try:
        filetype_module = importlib.import_module(rel_module, "textract.parsers")
    except ImportError as err:
        raise exceptions.ExtensionNotSupported(ext) from err

    # do the extraction

    parser = filetype_module.Parser()
    return parser.process(filename, input_encoding, output_encoding, **kwargs)


def _get_available_extensions():  # noqa: ANN202, RUF067
    """Get a list of available file extensions to make it easy for
    tab-completion and exception handling.
    """  # noqa: D205
    extensions = []

    # from filenames
    parsers_dir = pathlib.Path(__file__).parent
    glob_filename = str(parsers_dir / f"*{_FILENAME_SUFFIX}.py")
    # Escape the path for regex to handle Windows backslashes and special chars
    ext_re = re.compile(re.escape(glob_filename).replace(re.escape("*"), r"(?P<ext>\w+)"))
    for filename in glob.glob(glob_filename):  # noqa: PTH207
        if ext_match := ext_re.match(filename):
            ext = ext_match.groups()[0]
            extensions.extend((ext, "." + ext))

    # from relevant synonyms (don't use the '' synonym)
    for ext in EXTENSION_SYNONYMS:
        if ext:
            extensions.extend((ext, ext.replace(".", "", 1)))
    extensions.sort()
    return extensions
