"""Tests for PDF file format."""

import platform
import shutil
import unittest.mock
from pathlib import Path

import pytest

import textract
from textract.exceptions import ShellError, UnknownMethod
from textract.parsers.pdf_parser import Parser

from . import base

_HAS_PDFTOPPM = shutil.which("pdftoppm") is not None
_HAS_PDFTOTEXT = shutil.which("pdftotext") is not None
_HAS_TESSERACT = shutil.which("tesseract") is not None

_NO_PDFTOPPM_REASON = "pdftoppm is not installed (part of poppler; required for PDF OCR via tesseract)"
_NO_PDFTOTEXT_REASON = "pdftotext is not installed (part of poppler; install via your system package manager, e.g. apt/brew/pacman)"
_NO_TESSERACT_REASON = "tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)"
_LINUX_TESSERACT_REASON = "Tesseract OCR output varies by version; Linux CI has different output"
_WINDOWS_PDF_REASON = "PDF content may differ on Windows"

_pdftotext_marks = [
    pytest.mark.skipif(not _HAS_PDFTOTEXT, reason=_NO_PDFTOTEXT_REASON),
    pytest.mark.xfail(platform.system() == "Windows", reason=_WINDOWS_PDF_REASON, strict=False),
]
_tesseract_marks = [
    pytest.mark.skipif(not _HAS_PDFTOPPM, reason=_NO_PDFTOPPM_REASON),
    pytest.mark.skipif(not _HAS_TESSERACT, reason=_NO_TESSERACT_REASON),
    pytest.mark.skipif(platform.system() == "Linux", reason=_LINUX_TESSERACT_REASON),
]

# Each method with its source fixture.  Expected output is auto-derived as
# "<stem>-m=<method>.txt" by get_expected_filename() in base.py.
_METHOD_PARAMS = [
    pytest.param("pdftotext", "raw_text.pdf", marks=_pdftotext_marks),
    pytest.param("pdfminer", "raw_text.pdf"),
    pytest.param("tesseract", "ocr_text.pdf", marks=_tesseract_marks),
]

# Reusable decorator for the five default-method tests inherited from base.
# A class-level mark cannot be used because the explicit-method tests
# (pdfminer, tesseract) must not carry the Windows xfail.
_windows_xfail = pytest.mark.xfail(
    platform.system() == "Windows",
    reason=_WINDOWS_PDF_REASON,
    strict=False,
)


class PdfTestCase(base.ShellParserTests):
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

    @pytest.mark.parametrize("method,filename", _METHOD_PARAMS)
    def test_method_python(self, method, filename):
        """Extract text via Python API for each supported method."""
        d = Path(self.get_extension_directory())
        self.compare_python_output(str(d / filename), method=method)

    @pytest.mark.parametrize("method,filename", _METHOD_PARAMS)
    def test_method_cli(self, method, filename):
        """Extract text via CLI for each supported method."""
        d = Path(self.get_extension_directory())
        self.compare_cli_output(str(d / filename), method=method)

    @pytest.mark.skipif(
        platform.system() in {"Linux", "Windows"},
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
