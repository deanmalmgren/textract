"""Tests for PDF file format."""

import pathlib
import unittest

from . import base


class PdfTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PDF files."""

    extension = "pdf"

    def test_pdfminer_python(self):
        """Make sure pdfminer python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="pdfminer")

    def test_pdfminer_cli(self):
        """Make sure pdfminer command line output is correct."""
        self.compare_cli_output(self.raw_text_filename, method="pdfminer")

    def test_tesseract_cli(self):
        """Confirm pdf extraction with tesseract."""
        d = pathlib.Path(self.get_extension_directory())
        self.compare_cli_output(
            str(d / "ocr_text.pdf"),
            expected_filename=str(d / "ocr_text.txt"),
            method="tesseract",
        )

    def test_two_column(self):
        """Preserve two column layout in extraction."""
        d = pathlib.Path(self.get_extension_directory())
        filename = str(d / "two_column.pdf")
        self.compare_python_output(filename, layout=True)
