"""Tests for PDF file format."""

import pathlib
import platform
import shutil
import unittest

import pytest

from . import base

_HAS_PDFTOTEXT = shutil.which("pdftotext") is not None
_HAS_TESSERACT = shutil.which("tesseract") is not None


class PdfTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PDF files."""

    extension = "pdf"

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="PDF extraction character encoding differs on Windows",
    )
    def test_filename_spaces(self):
        """Make sure filenames with spaces work on the command line."""
        super().test_filename_spaces()

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="PDF extraction character encoding differs on Windows",
    )
    def test_raw_text_cli(self):
        """Make sure raw text matches from the command line."""
        super().test_raw_text_cli()

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="PDF extraction character encoding differs on Windows",
    )
    def test_raw_text_python(self):
        """Make sure raw text matches from python."""
        super().test_raw_text_python()

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="PDF extraction character encoding differs on Windows",
    )
    def test_standardized_text_cli(self):
        """Make sure standardized text matches from the command line."""
        super().test_standardized_text_cli()

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="PDF extraction character encoding differs on Windows",
    )
    def test_standardized_text_python(self):
        """Make sure standardized text matches from python."""
        super().test_standardized_text_python()

    @pytest.mark.skipif(
        not _HAS_PDFTOTEXT,
        reason="pdftotext is not installed (install via: brew install poppler)",
    )
    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="PDF extraction character encoding differs on Windows",
    )
    def test_pdftotext_python(self):
        """Make sure pdftotext python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="pdftotext")

    @pytest.mark.skipif(
        not _HAS_PDFTOTEXT,
        reason="pdftotext is not installed (install via: brew install poppler)",
    )
    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="PDF extraction character encoding differs on Windows",
    )
    def test_pdftotext_cli(self):
        """Make sure pdftotext command line output is correct."""
        self.compare_cli_output(self.raw_text_filename, method="pdftotext")

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="PDF extraction character encoding differs on Windows",
    )
    def test_pdfminer_python(self):
        """Make sure pdfminer python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="pdfminer")

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="PDF extraction character encoding differs on Windows",
    )
    def test_pdfminer_cli(self):
        """Make sure pdfminer command line output is correct."""
        self.compare_cli_output(self.raw_text_filename, method="pdfminer")

    @pytest.mark.skipif(
        not _HAS_TESSERACT,
        reason="tesseract-ocr is not installed (install via: brew install tesseract)",
    )
    @pytest.mark.skipif(
        platform.system() == "Linux",
        reason="Tesseract OCR output varies by version; Linux CI has different output",
    )
    def test_tesseract_cli(self):
        """Confirm pdf extraction with tesseract."""
        d = pathlib.Path(self.get_extension_directory())
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
        d = pathlib.Path(self.get_extension_directory())
        filename = str(d / "two_column.pdf")
        self.compare_python_output(filename, layout=True)
