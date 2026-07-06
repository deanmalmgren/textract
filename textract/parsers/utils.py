"""This module includes a bunch of convenient base classes that are
reused in many of the other parser modules.
"""

from __future__ import annotations

import contextlib
import errno
import io
import os
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import BinaryIO

import chardet

from textract import exceptions


class Source:
    """Beta: a single input to extract text from, regardless of where it
    lives (a file on disk, a ``bytes`` blob, or a readable binary stream).

    The core materializes the input into whatever form a parser declares it
    needs via :meth:`as_bytes` / :meth:`as_path` / :meth:`as_text_stream`, so
    parsers stop owning file I/O. This is what lets textract accept
    in-memory content and streams without every parser learning about it.
    ``as_text_stream`` is the only one of the three that avoids buffering the
    whole input in memory (the other two materialize it, since ``as_bytes``
    reads/drains it all and ``as_path`` spools it to disk)

    Not frozen and single-use when backed by a stream: the stream is drained
    on the first :meth:`as_bytes`/:meth:`as_path` call and the bytes cached,
    and calling :meth:`as_text_stream` after that reads from the cache
    rather than the (already-drained) stream
    """

    def __init__(
        self,
        *,
        filename: str | os.PathLike | None = None,
        data: bytes | None = None,
        stream: BinaryIO | None = None,
        extension: str | None = None,
    ) -> None:
        self.filename = Path(filename) if filename is not None else None
        self.extension = extension
        self._stream = stream
        self._data = data

    @classmethod
    def from_path(cls, filename, extension: str | None = None) -> Source:
        return cls(filename=filename, extension=extension)

    @classmethod
    def from_bytes(cls, data: bytes, extension: str | None) -> Source:
        return cls(data=data, extension=extension)

    @classmethod
    def from_stream(cls, stream: BinaryIO, extension: str | None) -> Source:
        return cls(stream=stream, extension=extension)

    def as_bytes(self) -> bytes:
        """Return the raw bytes, reading the file or draining the stream once."""
        if self._data is None:
            if self._stream is not None:
                self._data = self._stream.read()
            elif self.filename is not None:
                self._data = self.filename.read_bytes()
            else:
                self._data = b""
        return self._data

    @contextlib.contextmanager
    def as_path(self) -> Iterator[Path]:
        """Yield a real filesystem path for parsers that shell out to an
        external program. Uses the original file when there is one, otherwise
        spools the bytes to a temp file that is removed on exit
        """
        if self.filename is not None:
            yield self.filename
            return
        suffix = self.extension or ""
        if suffix and not suffix.startswith("."):
            suffix = "." + suffix
        handle = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        try:
            handle.write(self.as_bytes())
            handle.close()
            yield Path(handle.name)
        finally:
            os.unlink(handle.name)

    @contextlib.contextmanager
    def _binary_stream(self) -> Iterator[BinaryIO]:
        if self._data is not None:
            yield io.BytesIO(self._data)
        elif self._stream is not None:
            yield self._stream
        elif self.filename is not None:
            with self.filename.open("rb") as handle:
                yield handle
        else:
            yield io.BytesIO(b"")

    @contextlib.contextmanager
    def as_text_stream(self, input_encoding: str) -> Iterator[Iterator[str]]:
        """Yield decoded lines lazily instead of buffering the whole input in
        memory (issue #97). Requires an explicit ``input_encoding``:
        auto-detection (chardet) needs the full byte content to score its
        confidence, which would defeat the point of streaming, so callers
        without one fall back to :meth:`as_bytes` (see
        ``DecodedParser.process_source``).
        """
        with self._binary_stream() as binary:
            yield io.TextIOWrapper(binary, encoding=input_encoding)


class BaseParser:
    """The :class:`.BaseParser` abstracts out some common functionality
    that is used across all document Parsers. In particular, it has
    the responsibility of handling all unicode and byte-encoding.
    """

    def extract(self, filename, **kwargs) -> bytes | str:
        """This method must be overwritten by child classes to extract raw
        text from a filename. This method can return either a
        byte-encoded string or unicode.
        """
        raise NotImplementedError("must be overwritten by child classes")

    def encode(self, text, encoding):
        """Encode the ``text`` in ``encoding`` byte-encoding. This ignores
        code points that can't be encoded in byte-strings.
        """
        return text.encode(encoding, "ignore")

    def process(self, filename, input_encoding, output_encoding="utf8", **kwargs):
        """Process ``filename`` and encode byte-string with ``encoding``. This
        method is called by :func:`textract.parsers.process` and wraps
        the :meth:`.BaseParser.extract` method in `a delicious unicode
        sandwich <http://nedbatchelder.com/text/unipain.html>`_.

        """
        return self.process_source(
            Source.from_path(filename), input_encoding, output_encoding, **kwargs
        )

    def process_source(self, source, input_encoding, output_encoding="utf8", **kwargs):
        """Extract text from a :class:`.Source` and wrap it in a `unicode
        sandwich <http://nedbatchelder.com/text/unipain/unipain.html#35>`_.

        The default treats the source as a path (spooling to a temp file when
        the input is bytes/stream), which is what shell-out parsers need.
        Text and bytes parsers override this to consume the source in memory.
        """
        with source.as_path() as path:
            byte_string = self.extract(str(path), **kwargs)
        unicode_string = self.decode(byte_string, input_encoding)
        return self.encode(unicode_string, output_encoding)

    def decode(self, text, input_encoding=None):
        """Decode ``text`` using the `chardet
        <https://github.com/chardet/chardet>`_ package.
        """
        # only decode byte strings into unicode if it hasn't already
        # been done by a subclass
        if isinstance(text, str):
            return text

        # empty text? nothing to decode
        if not text:
            return ""

        # use the provided encoding
        if input_encoding:
            try:
                return text.decode(input_encoding)
            except UnicodeDecodeError as err:
                raise exceptions.InvalidInputEncoding(input_encoding, str(err)) from err

        # use chardet to automatically detect the encoding text if no encoding is provided
        result = chardet.detect(text)
        encoding = result["encoding"] if result["confidence"] > 0.80 else "utf8"
        return text.decode(encoding, errors="replace")


class PathParser(BaseParser):
    """Input-kind base for parsers that require a real filesystem path,
    typically because they hand it to an external program. Behaviorally
    identical to :class:`.BaseParser` (whose default ``process_source``
    already spools bytes/stream input to a temp file); it exists to name the
    third leg of the path/text/bytes taxonomy alongside :class:`.DecodedParser`
    and :class:`.BytesParser`.
    """


class ShellParser(PathParser):
    """The :class:`.ShellParser` extends the :class:`.PathParser` to make
    it easy to run external programs from the command line with
    `Fabric <http://www.fabfile.org/>`_-like behavior.
    """

    def run(self, args):
        """Run ``command`` and return the subsequent ``stdout`` and ``stderr``
        as a tuple. If the command is not successful, this raises a
        :exc:`textract.exceptions.ShellError`.
        """

        # run a subprocess and put the stdout and stderr on the pipe object
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            startupinfo = None
        try:
            pipe = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo,
            )
        except OSError as e:
            if e.errno == errno.ENOENT:
                # File not found.
                # This is equivalent to getting exitcode 127 from sh
                raise exceptions.ShellError(
                    " ".join(args),
                    127,
                    b"",
                    b"",
                )
            raise  # Reraise the last exception unmodified

        # pipe.wait() ends up hanging on large files. using
        # pipe.communicate appears to avoid this issue
        stdout, stderr = pipe.communicate()

        # if pipe is busted, raise an error (unlike Fabric)
        if pipe.returncode != 0:
            raise exceptions.ShellError(
                " ".join(args),
                pipe.returncode,
                stdout,
                stderr,
            )

        return stdout, stderr

    def temp_filename(self):
        """Return a unique tempfile name."""
        # TODO: it would be nice to get this to behave more like a
        # context so we can make sure these temporary files are
        # removed, regardless of whether an error occurs or the
        # program is terminated.
        handle, filename = tempfile.mkstemp()
        os.close(handle)
        return filename


class DecodedParser(BaseParser):
    """Input-kind base for parsers that operate on decoded text rather than a
    filename. The core reads and decodes the source, honoring
    ``input_encoding``, so subclasses implement
    :meth:`.DecodedParser.extract_from_text` and never deal with byte-encodings
    themselves.
    """

    def extract_from_text(self, text, **kwargs) -> str:
        """This method must be overwritten by child classes. It receives
        the already-decoded contents of the file instead of a filename.
        """
        raise NotImplementedError("must be overwritten by child classes")

    def extract_from_lines(self, lines, **kwargs) -> str:
        """Beta streaming hook: override alongside :meth:`extract_from_text`
        for formats whose parsing library can consume an iterator of decoded
        lines incrementally instead of one big string (see ``csv_parser.py``)
        """
        return self.extract_from_text("".join(lines), **kwargs)

    def process_source(self, source, input_encoding, output_encoding="utf8", **kwargs):
        streamable = (
            type(self).extract_from_lines is not DecodedParser.extract_from_lines
        )
        if streamable and input_encoding:
            try:
                with source.as_text_stream(input_encoding) as lines:
                    text = self.extract_from_lines(lines, **kwargs)
            except UnicodeDecodeError as err:
                raise exceptions.InvalidInputEncoding(input_encoding, str(err)) from err
            return self.encode(text, output_encoding)
        text = self.decode(source.as_bytes(), input_encoding)
        return self.encode(self.extract_from_text(text, **kwargs), output_encoding)


class BytesParser(BaseParser):
    """Beta input-kind base for parsers whose library can consume raw bytes
    or a file-like object in process (e.g. docx/xlsx/pptx/epub open a zip),
    so no temp file is needed. Subclasses implement
    :meth:`.BytesParser.extract_from_bytes`.
    """

    def extract_from_bytes(self, data: bytes, **kwargs) -> bytes | str:
        """This method must be overwritten by child classes. It receives the
        raw bytes of the source instead of a filename.
        """
        raise NotImplementedError("must be overwritten by child classes")

    def process_source(self, source, input_encoding, output_encoding="utf8", **kwargs):
        byte_string = self.extract_from_bytes(source.as_bytes(), **kwargs)
        unicode_string = self.decode(byte_string, input_encoding)
        return self.encode(unicode_string, output_encoding)
