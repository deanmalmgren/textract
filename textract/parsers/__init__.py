"""
Route the request to the appropriate parser based on file type.
"""

import glob
import importlib.util
import re
import sys
import warnings
from pathlib import Path
from typing import BinaryIO

from textract import exceptions
from textract.parsers.utils import Source

# Dictionary structure for synonymous file extension types
EXTENSION_SYNONYMS = {
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
DEFAULT_OUTPUT_ENCODING = "utf_8"

# filename format
_FILENAME_SUFFIX = "_parser"


def process(
    filename,
    input_encoding=None,
    output_encoding=DEFAULT_OUTPUT_ENCODING,
    extension=None,
    **kwargs,
):
    """This is the core function used for extracting text. It routes the
    ``filename`` to the appropriate parser and returns the extracted
    text as a byte-string encoded with ``encoding``.

    ``filename`` may be ``"-"`` to read the document from ``stdin`` (beta),
    in which case ``extension`` is required.
    """
    if filename == "-":
        return process_stream(
            sys.stdin.buffer,
            extension=extension,
            input_encoding=input_encoding,
            output_encoding=output_encoding,
            **kwargs,
        )

    # make sure the filename exists
    if not Path(filename).exists():
        raise exceptions.MissingFileError(filename)

    source = Source.from_path(filename, extension=extension)
    return _process_source(source, input_encoding, output_encoding, **kwargs)


def process_bytes(
    data: bytes,
    extension: str | None,
    input_encoding=None,
    output_encoding=DEFAULT_OUTPUT_ENCODING,
    **kwargs,
):
    """Beta: extract text from in-memory ``data`` (e.g. an HTTP response
    body), no temp file required by the caller. ``extension`` is required to
    route to a parser since there is no filename to sniff. See issue #300.
    """
    _warn_beta()
    source = Source.from_bytes(data, extension=extension)
    return _process_source(source, input_encoding, output_encoding, **kwargs)


def process_stream(
    stream: BinaryIO,
    extension: str | None,
    input_encoding=None,
    output_encoding=DEFAULT_OUTPUT_ENCODING,
    **kwargs,
):
    """Beta: extract text from a readable binary ``stream`` (e.g.
    ``sys.stdin.buffer`` or an open file object). ``extension`` is required.
    See issues #97 and #300.
    """
    _warn_beta()
    source = Source.from_stream(stream, extension=extension)
    return _process_source(source, input_encoding, output_encoding, **kwargs)


def _warn_beta():
    warnings.warn(
        "textract's bytes/stream input (process_bytes, process_stream, and "
        "`-` stdin) is beta; the Source API may change in a future release.",
        FutureWarning,
        stacklevel=3,
    )


def _resolve_extension(source: Source) -> str:
    """Resolve the routing extension from an explicit override or the
    source's filename, applying the leading-dot/lowercase/synonym rules.
    """
    if source.extension:
        ext = source.extension
        if not ext.startswith("."):
            ext = "." + ext
        ext = ext.lower()
    elif source.filename is not None:
        ext = source.filename.suffix.lower()
    else:
        raise exceptions.ExtensionRequired()
    return EXTENSION_SYNONYMS.get(ext, ext)


def _process_source(source, input_encoding, output_encoding, **kwargs):
    ext = _resolve_extension(source)

    # to avoid conflicts with packages that are installed globally
    # (e.g. python's json module), all extension parser modules have
    # the _parser extension
    rel_module = ext + _FILENAME_SUFFIX

    # if there's no parser module for this extension at all, the file
    # extension isn't currently supported
    if importlib.util.find_spec("textract.parsers" + rel_module) is None:
        raise exceptions.ExtensionNotSupported(ext)

    # the parser module exists, but importing it can still fail if one
    # of its third-party dependencies isn't installed
    try:
        filetype_module = importlib.import_module(rel_module, "textract.parsers")
    except ImportError as err:
        raise exceptions.MissingModuleError(err, ext) from err

    # do the extraction
    parser = filetype_module.Parser()
    try:
        return parser.process_source(source, input_encoding, output_encoding, **kwargs)
    except (exceptions.ShellError, exceptions.InvalidInputEncoding) as err:
        err.ext = ext
        raise


def _get_available_extensions():
    """Get a list of available file extensions to make it easy for
    tab-completion and exception handling.
    """
    extensions = []

    # from filenames
    parsers_dir = Path(__file__).parent
    glob_filename = str(parsers_dir / f"*{_FILENAME_SUFFIX}.py")
    # Escape the path for regex to handle Windows backslashes and special chars
    ext_re = re.compile(
        re.escape(glob_filename).replace(re.escape("*"), r"(?P<ext>\w+)"),
    )
    for filename in glob.glob(glob_filename):
        if ext_match := ext_re.match(filename):
            ext = ext_match.groups()[0]
            extensions.extend((ext, "." + ext))

    # from relevant synonyms (don't use the '' synonym)
    for ext in EXTENSION_SYNONYMS:
        if ext:
            extensions.extend((ext, ext.replace(".", "", 1)))
    extensions.sort()
    return extensions
