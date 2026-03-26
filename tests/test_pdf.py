"""Tests for PDF file format."""

from pathlib import Path
import platform
import shutil
import unittest

import pytest

from . import base

_HAS_PDFTOPPM = shutil.which("pdftoppm") is not None
_HAS_PDFTOTEXT = shutil.which("pdftotext") is not None
_HAS_TESSERACT = shutil.which("tesseract") is not None

_WINDOWS_PDF_REASON = "PDF content may differ on Windows"


class PdfTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PDF files."""

    extension = "pdf"

    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason=_WINDOWS_PDF_REASON,
        strict=False,
    )
    def test_filename_spaces(self):
        """Make sure filenames with spaces work on the command line."""
        super().test_filename_spaces()

    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason=_WINDOWS_PDF_REASON,
        strict=False,
    )
    def test_raw_text_cli(self):
        """Make sure raw text matches from the command line."""
        super().test_raw_text_cli()

    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason=_WINDOWS_PDF_REASON,
        strict=False,
    )
    def test_raw_text_python(self):
        """Make sure raw text matches from python."""
        super().test_raw_text_python()

    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason=_WINDOWS_PDF_REASON,
        strict=False,
    )
    def test_standardized_text_cli(self):
        """Make sure standardized text matches from the command line."""
        super().test_standardized_text_cli()

    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason=_WINDOWS_PDF_REASON,
        strict=False,
    )
    def test_standardized_text_python(self):
        """Make sure standardized text matches from python."""
        super().test_standardized_text_python()

    @pytest.mark.skipif(
        not _HAS_PDFTOTEXT,
        reason="pdftotext is not installed (part of poppler; install via your system package manager, e.g. apt/brew/pacman)",
    )
    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason=_WINDOWS_PDF_REASON,
        strict=False,
    )
    def test_pdftotext_python(self):
        """Make sure pdftotext python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="pdftotext")

    @pytest.mark.skipif(
        not _HAS_PDFTOTEXT,
        reason="pdftotext is not installed (part of poppler; install via your system package manager, e.g. apt/brew/pacman)",
    )
    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason=_WINDOWS_PDF_REASON,
        strict=False,
    )
    def test_pdftotext_cli(self):
        """Make sure pdftotext command line output is correct."""
        self.compare_cli_output(self.raw_text_filename, method="pdftotext")

    def test_pdfminer_python(self):
        """Make sure pdfminer python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="pdfminer")

    def test_pdfminer_cli(self):
        """Make sure pdfminer command line output is correct."""
        self.compare_cli_output(self.raw_text_filename, method="pdfminer")

    @pytest.mark.skipif(
        not _HAS_PDFTOPPM,
        reason="pdftoppm is not installed (part of poppler; required for PDF OCR via tesseract)",
    )
    @pytest.mark.skipif(
        not _HAS_TESSERACT,
        reason="tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)",
    )
    @pytest.mark.skipif(
        platform.system() == "Linux",
        reason="Tesseract OCR output varies by version; Linux CI has different output",
    )
    def test_tesseract_cli(self):
        """Confirm pdf extraction with tesseract."""
        d = Path(self.get_extension_directory())
        self.compare_cli_output(
            str(d / "ocr_text.pdf"),
            expected_filename=str(d / "ocr_text.txt"),
            method="tesseract",
        )

    @pytest.mark.skipif(
        platform.system() in {"Linux", "Windows"},
        reason="PDF layout extraction varies by platform; character encoding differs",
    )
    def test_two_column(self):
        """Preserve two column layout in extraction."""
        d = Path(self.get_extension_directory())
        filename = str(d / "two_column.pdf")
        self.compare_python_output(filename, layout=True)
