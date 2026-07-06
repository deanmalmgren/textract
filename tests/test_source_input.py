"""Beta: bytes/stream/stdin input (issues #300, #97).

Proves the new public entry points (``process_bytes``, ``process_stream``,
and CLI ``-`` stdin) produce the same text as ``process(filename)`` across the
three parser input kinds:

- text  (csv -> NativeParser, decoded in memory, or streamed line-by-line
  when ``input_encoding`` is explicit -- see ``test_csv_streams_without_
  buffering_full_input``)
- bytes (docx -> BytesParser, opened in memory, no temp file)
- path  (pdf -> shell parser, Source spools a temp file for pdftotext)

Next steps beyond this tracer bullet:

- Only csv has a real ``extract_from_lines`` streaming implementation.
  html/eml/json/txt all parse their whole document at once (DOM, MIME
  message, JSON) so they keep buffering; worth revisiting per-format if a
  truly huge file shows up in practice.
- Streaming still requires an explicit ``input_encoding``: auto-detection
  (chardet) scores confidence off the full byte content, which would force
  buffering anyway. A ``chardet.universaldetector.UniversalDetector`` fed
  incrementally could recover auto-detection without giving up streaming.
- BytesParser formats (docx/xlsx/pptx/epub/msg) still materialize the whole
  blob in memory by design (their libraries need to seek a zip's central
  directory); that's a memory-vs-temp-file tradeoff, not a missed
  optimization, so it isn't "streaming" in the same sense as the text path.
- Streaming only applies to the input side: process_* still returns one
  complete string, so very large *output* isn't addressed here.
"""

import io
import subprocess
import unittest
import warnings
from pathlib import Path

import textract
from textract.parsers import csv_parser
from textract.parsers.utils import Source

_FIXTURES = Path(__file__).resolve().parent
_CASES = {
    "csv": _FIXTURES / "csv" / "raw_text.csv",
    "docx": _FIXTURES / "docx" / "raw_text.docx",
    "pdf": _FIXTURES / "pdf" / "raw_text.pdf",
}


def _quiet(func, *args, **kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        return func(*args, **kwargs)


class SourceInputTestCase(unittest.TestCase):
    def test_process_bytes_matches_filename(self):
        for ext, path in _CASES.items():
            with self.subTest(ext=ext):
                expected = textract.process(str(path))
                got = _quiet(textract.process_bytes, path.read_bytes(), extension=ext)
                assert got == expected

    def test_process_stream_matches_filename(self):
        for ext, path in _CASES.items():
            with self.subTest(ext=ext):
                expected = textract.process(str(path))
                got = _quiet(
                    textract.process_stream,
                    io.BytesIO(path.read_bytes()),
                    extension=ext,
                )
                assert got == expected

    def test_beta_warning(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            textract.process_bytes(_CASES["csv"].read_bytes(), extension="csv")
        assert any(issubclass(w.category, FutureWarning) for w in caught)

    def test_missing_extension_raises(self):
        with self.assertRaises(textract.exceptions.ExtensionRequired):
            _quiet(textract.process_bytes, b"hello", extension=None)

    def test_csv_streams_without_buffering_full_input(self):
        """With an explicit input_encoding, csv is read lazily instead of
        buffered whole: Source._data (the as_bytes() cache) stays empty.
        """
        path = _CASES["csv"]
        source = Source.from_path(path, extension="csv")
        result = csv_parser.Parser().process_source(source, input_encoding="utf-8")
        assert result == textract.process(str(path))
        assert source._data is None

    def test_csv_streams_from_stdin_pipe(self):
        path = _CASES["csv"]
        expected = textract.process(str(path))
        result = subprocess.run(
            ["textract", "--extension", "csv", "--input-encoding", "utf_8", "-"],
            input=path.read_bytes(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        assert result.stdout == expected

    def test_cli_stdin(self):
        path = _CASES["pdf"]
        expected = textract.process(str(path))
        result = subprocess.run(
            ["textract", "--extension", "pdf", "-"],
            input=path.read_bytes(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        assert result.stdout == expected


if __name__ == "__main__":
    unittest.main()
