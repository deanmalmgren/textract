"""Tests for DOCX file format."""

import pathlib
import unittest

from . import base


class DocxTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from DOCX (Word) files."""

    extension = "docx"

    def test_tables(self):
        """Make sure table output is correct."""
        d = pathlib.Path(self.get_extension_directory())
        self.compare_cli_output(str(d / "paragraphs_and_tables.docx"))
