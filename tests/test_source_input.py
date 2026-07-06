"""Beta: bytes/stream/stdin input (issues #300, #97).

Proves the new public entry points (``process_bytes``, ``process_stream``,
and CLI ``-`` stdin) produce the same text as ``process(filename)`` across the
three parser input kinds:

- text  (csv -> TextParser, decoded in memory)
- bytes (docx -> BytesParser, opened in memory, no temp file)
- path  (pdf -> shell parser, Source spools a temp file for pdftotext)
"""

import io
import subprocess
import unittest
import warnings
from pathlib import Path

import textract

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
        with self.assertRaises(textract.exceptions.ExtensionNotSupported):
            _quiet(textract.process_bytes, b"hello", extension=None)

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
