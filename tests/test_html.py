"""Tests for HTML file format."""

import pathlib
import unittest

from . import base


class HtmlTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from HTML files."""

    extension = "html"

    def test_table_text_python(self):
        """Make sure tables in html look pretty through python."""
        d = pathlib.Path(self.get_extension_directory())
        self.compare_python_output(str(d / "tables.html"))

    def test_table_text_cli(self):
        """Make sure tables in html look pretty through cli."""
        d = pathlib.Path(self.get_extension_directory())
        self.compare_cli_output(str(d / "tables.html"))
