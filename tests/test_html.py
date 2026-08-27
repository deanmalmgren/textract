"""Tests for HTML file format."""

import unittest
from pathlib import Path

from . import base


class HtmlTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from HTML files."""

    extension = "html"

    def test_table_text_python(self):
        """Make sure tables in html look pretty through python."""
        d = Path(self.get_extension_directory())
        self.compare_python_output(str(d / "tables.html"))

    def test_table_text_cli(self):
        """Make sure tables in html look pretty through cli."""
        d = Path(self.get_extension_directory())
        self.compare_cli_output(str(d / "tables.html"))

    def test_explicit_input_encoding(self):
        """Regression test for #353: an html file encoded as cp1251 must
        be readable when input_encoding is specified explicitly."""
        self.assert_input_encoding_respected("cyrillic_cp1251", "cp1251")

    def test_invalid_input_encoding(self):
        """A valid-but-wrong input_encoding must raise a friendly error
        instead of leaking a raw UnicodeDecodeError."""
        self.assert_invalid_input_encoding_raises("cyrillic_cp1251", "ascii")
