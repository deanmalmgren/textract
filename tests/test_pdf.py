"""Tests for PDF file format."""

import shutil
import sys
import unittest
import unittest.mock
from pathlib import Path

import pytest

import textract
from textract.exceptions import ShellError, UnknownMethod
from textract.parsers.pdf_parser import Parser

from . import base

_IS_WINDOWS = sys.platform == "win32"
_IS_LINUX = sys.platform == "linux"

_HAS_PDFTOPPM = shutil.which("pdftoppm") is not None
_HAS_PDFTOTEXT = shutil.which("pdftotext") is not None
_HAS_TESSERACT = shutil.which("tesseract") is not None

_NO_PDFTOPPM_REASON = (
    "pdftoppm is not installed (part of poppler; required for PDF OCR via tesseract)"
)
_NO_PDFTOTEXT_REASON = "pdftotext is not installed (part of poppler; install via your system package manager, e.g. apt/brew/pacman)"
_NO_TESSERACT_REASON = "tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)"
_LINUX_TESSERACT_REASON = (
    "Tesseract OCR output varies by version; Linux CI has different output"
)
_WINDOWS_PDF_REASON = "PDF content may differ on Windows"


def _first_skip_reason(*conditions: tuple[bool, str]) -> str:
    """Return the reason string for the first failing condition, or empty string."""
    for condition, reason in conditions:
        if condition:
            return reason
    return ""


# Each method with its source fixture and an optional skip reason.
# Expected output is auto-derived as "<stem>-m=<method>.txt" by
# get_expected_filename() in base.py.
_METHOD_CASES: list[tuple[str, str, str]] = [
    (
        "pdftotext",
        "raw_text.pdf",
        _first_skip_reason(
            (not _HAS_PDFTOTEXT, _NO_PDFTOTEXT_REASON),
            (_IS_WINDOWS, _WINDOWS_PDF_REASON),
        ),
    ),
    ("pdfminer", "raw_text.pdf", ""),
    (
        "tesseract",
        "ocr_text.pdf",
        _first_skip_reason(
            (not _HAS_PDFTOPPM, _NO_PDFTOPPM_REASON),
            (not _HAS_TESSERACT, _NO_TESSERACT_REASON),
            (_IS_LINUX, _LINUX_TESSERACT_REASON),
        ),
    ),
]

# Reusable decorator for the five default-method tests inherited from base.
# A class-level mark cannot be used because the explicit-method tests (pdfminer,
# tesseract) must not carry the Windows xfail.
_windows_xfail = pytest.mark.xfail(
    _IS_WINDOWS,
    reason=_WINDOWS_PDF_REASON,
    strict=False,
)


class PdfTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PDF files."""

    extension = "pdf"

    @_windows_xfail
    def test_filename_spaces(self):
        super().test_filename_spaces()

    @_windows_xfail
    def test_raw_text_cli(self):
        super().test_raw_text_cli()

    @_windows_xfail
    def test_raw_text_python(self):
        super().test_raw_text_python()

    @_windows_xfail
    def test_standardized_text_cli(self):
        super().test_standardized_text_cli()

    @_windows_xfail
    def test_standardized_text_python(self):
        super().test_standardized_text_python()

    def test_method_python(self):
        """Extract text via Python API for each supported method."""
        d = Path(self.get_extension_directory())
        for method, filename, skip_reason in _METHOD_CASES:
            with self.subTest(method=method, filename=filename):
                if skip_reason:
                    self.skipTest(skip_reason)
                self.compare_python_output(str(d / filename), method=method)

    def test_method_cli(self):
        """Extract text via CLI for each supported method."""
        d = Path(self.get_extension_directory())
        for method, filename, skip_reason in _METHOD_CASES:
            with self.subTest(method=method, filename=filename):
                if skip_reason:
                    self.skipTest(skip_reason)
                self.compare_cli_output(str(d / filename), method=method)

    @pytest.mark.skipif(
        _IS_LINUX or _IS_WINDOWS,
        reason="PDF layout extraction varies by platform; character encoding differs",
    )
    def test_two_column(self):
        """Preserve two column layout in extraction."""
        d = Path(self.get_extension_directory())
        self.compare_python_output(str(d / "two_column.pdf"), layout=True)

    def test_unknown_method_raises(self):
        """Unknown method string raises UnknownMethod."""
        with pytest.raises(UnknownMethod):
            textract.process(self.raw_text_filename, method="bogus")

    def test_pdftotext_fallback_to_pdfminer(self):
        """Default method falls back to pdfminer when pdftotext is not installed."""
        with unittest.mock.patch.object(
            Parser,
            "extract_pdftotext",
            side_effect=ShellError("pdftotext", 127, b"", b""),
        ):
            result = textract.process(self.raw_text_filename)
        assert result
