"""Beta: bytes/stream/stdin input.

Proves the new public entry points (``process_bytes``, ``process_stream``,
and CLI ``-`` stdin) produce the same text as ``process(filename)`` across the
three parser input kinds:

- text  (csv -> DecodedParser, decoded in memory, or streamed line-by-line
  when ``input_encoding`` is explicit, see
  ``test_csv_streams_without_buffering_full_input`` and
  ``StreamingMemoryTestCase`` below)
- bytes (docx -> BytesParser, opened in memory, no temp file)
- path  (pdf -> shell parser, Source spools a temp file for pdftotext)

Next steps beyond this tracer MVP:

- Only csv has a real ``extract_from_lines`` streaming implementation.
  html/eml/json/txt all parse their whole document at once (DOM, MIME
  message, JSON), so they keep buffering. Worth revisiting per-format if a
  truly huge file shows up in practice
- Streaming still requires an explicit ``input_encoding``, since
  auto-detection (chardet) scores confidence off the full byte content,
  which would force buffering anyway. A
  ``chardet.universaldetector.UniversalDetector`` fed incrementally could
  recover auto-detection without giving up streaming
- BytesParser formats (docx/xlsx/pptx/epub/msg) still materialize the whole
  blob in memory by design (their libraries need to seek a zip's central
  directory). That's a memory-vs-temp-file tradeoff, not a missed
  optimization, so it isn't "streaming" in the same sense as the text path
- Streaming only applies to the input side: process_* still returns one
  complete string, so very large *output* isn't addressed yet
"""

import io
import subprocess
import sys
import tempfile
import unittest
import warnings
from pathlib import Path

import pytest

import textract
from textract.parsers import csv_parser
from textract.parsers.utils import Source

from . import base

try:
    import resource
except ImportError:  # resource (peak RSS) is POSIX-only
    resource = None

_WINDOWS_PDF_XFAIL = pytest.mark.xfail(
    sys.platform == "win32",
    reason="PDF content may differ on Windows",
    strict=False,
)

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


class SourceInputTestCase(base.GenericUtilities, unittest.TestCase):
    def _assert_text_equal(self, actual: bytes, expected: bytes, label: str) -> None:
        """Compare extracted text tolerantly of platform-specific whitespace
        (line endings, tabs/nbsp, blank lines), same as the rest of the suite
        (see ``base.GenericUtilities.clean_text``), so these fixture-backed
        comparisons don't break on Windows CI's CRLF checkout.
        """
        cleaned_actual = self.clean_text(actual)
        cleaned_expected = self.clean_text(expected)
        if cleaned_actual != cleaned_expected:
            raise AssertionError(
                base._generate_bytes_diff_message(
                    cleaned_actual, cleaned_expected, label
                )
            )

    def test_process_bytes_matches_filename(self):
        for ext, path in _CASES.items():
            with self.subTest(ext=ext):
                expected = textract.process(str(path))
                got = _quiet(textract.process_bytes, path.read_bytes(), extension=ext)
                self._assert_text_equal(got, expected, str(path))

    def test_process_stream_matches_filename(self):
        for ext, path in _CASES.items():
            with self.subTest(ext=ext):
                expected = textract.process(str(path))
                got = _quiet(
                    textract.process_stream,
                    io.BytesIO(path.read_bytes()),
                    extension=ext,
                )
                self._assert_text_equal(got, expected, str(path))

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
        expected_filename = path.parent / "raw_text.txt"
        self._assert_text_equal(
            result, expected_filename.read_bytes(), str(expected_filename)
        )
        assert source._data is None

    def test_csv_streams_from_stdin_pipe(self):
        path = _CASES["csv"]
        expected_filename = path.parent / "raw_text.txt"
        result = subprocess.run(
            ["textract", "--extension", "csv", "--input-encoding", "utf_8", "-"],
            input=path.read_bytes(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._assert_text_equal(
            result.stdout, expected_filename.read_bytes(), str(expected_filename)
        )

    @_WINDOWS_PDF_XFAIL
    def test_cli_stdin(self):
        path = _CASES["pdf"]
        expected_filename = path.parent / "raw_text.txt"
        result = subprocess.run(
            ["textract", "--extension", "pdf", "-"],
            input=path.read_bytes(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._assert_text_equal(
            result.stdout, expected_filename.read_bytes(), str(expected_filename)
        )


class StreamingMemoryTestCase(unittest.TestCase):
    """Real (not just white-box) proof that csv streaming bounds memory: runs
    the CLI against a large file twice, with and without ``--input-encoding``,
    and compares peak child RSS. The ratio (not an absolute byte threshold)
    is what's asserted, so this holds regardless of ru_maxrss's unit (KB on
    Linux, bytes on macOS) or a runner's baseline interpreter overhead.
    """

    @unittest.skipUnless(resource is not None, "resource module is POSIX-only")
    def test_streaming_uses_less_memory_than_buffering(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "large.csv"
            row = ",".join(f"field{i}" for i in range(8)) + "\n"
            with path.open("w") as f:
                for _ in range(int(20 * 1024 * 1024 / len(row))):
                    f.write(row)

            streamed_rss = self._child_max_rss(
                [
                    "textract",
                    "--extension",
                    "csv",
                    "--input-encoding",
                    "utf_8",
                    str(path),
                ]
            )
            buffered_rss = self._child_max_rss(
                ["textract", "--extension", "csv", str(path)]
            )
            assert streamed_rss < buffered_rss * 0.85

    @staticmethod
    def _child_max_rss(cmd):
        """Run ``cmd`` as the sole child of a throwaway python process and
        return that child's peak RSS via RUSAGE_CHILDREN. Measuring from a
        fresh process (rather than this test process) keeps subprocesses
        started by other tests from inflating the high-water mark.
        """
        script = (
            "import resource, subprocess\n"
            f"subprocess.run({cmd!r}, check=True, stdout=subprocess.DEVNULL, "
            "stderr=subprocess.DEVNULL)\n"
            "print(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return int(result.stdout.strip())


if __name__ == "__main__":
    unittest.main()
