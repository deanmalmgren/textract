"""Tests for processing files without extensions."""

import unittest
from pathlib import Path

import textract


class NoExtTestCase(unittest.TestCase):
    """Test extraction from files without file extensions."""

    def test_docx(self):
        """Extract from file without extension using extension parameter."""
        current_dir = Path(__file__).resolve().parents[1]
        docx_file = current_dir / "tests/no_ext/docx_paragraphs_and_tables"
        result = textract.process(docx_file, extension="docx")
        assert result, "Expected non-empty extraction result"
        assert len(result) > 0

    def test_msg(self):
        """Extract from email file without extension using extension parameter."""
        current_dir = Path(__file__).resolve().parents[1]
        msg_file = current_dir / "tests/no_ext/msg_standardized_text"
        result = textract.process(msg_file, extension="msg")
        assert result, "Expected non-empty extraction result"
        assert len(result) > 0

    def test_pdf(self):
        """Extract from PDF file without extension using extension parameter."""
        current_dir = Path(__file__).resolve().parents[1]
        pdf_file = current_dir / "tests/no_ext/pdf_standardized_text"
        result = textract.process(pdf_file, extension=".pdf")
        assert result, "Expected non-empty extraction result"
        assert len(result) > 0
