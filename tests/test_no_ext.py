"""Tests for processing files without extensions."""

import pathlib
import unittest

import textract


class NoExtTestCase(unittest.TestCase):
    """Test extraction from files without file extensions."""

    def test_docx(self):  # noqa: PLR6301
        """Extract from file without extension using extension parameter."""
        current_dir = pathlib.Path(__file__).resolve().parent.parent
        docx_file = current_dir / "tests/no_ext/docx_paragraphs_and_tables"
        textract.process(docx_file, extension="docx")

    def test_msg(self):  # noqa: PLR6301
        """Extract from email file without extension using extension parameter."""
        current_dir = pathlib.Path(__file__).resolve().parent.parent
        msg_file = current_dir / "tests/no_ext/msg_standardized_text"
        textract.process(msg_file, extension="msg")

    def test_pdf(self):  # noqa: PLR6301
        """Extract from PDF file without extension using extension parameter."""
        current_dir = pathlib.Path(__file__).resolve().parent.parent
        pdf_file = current_dir / "tests/no_ext/pdf_standardized_text"
        textract.process(pdf_file, extension=".pdf")
