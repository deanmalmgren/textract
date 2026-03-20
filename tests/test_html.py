"""Tests for HTML file format."""

import pathlib
import platform
import unittest

import pytest

from . import base

_xfail_windows = pytest.mark.xfail(
    platform.system() == "Windows",
    reason="HTML output varies on Windows due to BeautifulSoup/lxml platform differences",
    strict=False,
)


class HtmlTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from HTML files."""

    extension = "html"

    @_xfail_windows
    def test_raw_text_cli(self):
        """Make sure raw text matches from the command line."""
        super().test_raw_text_cli()

    @_xfail_windows
    def test_raw_text_python(self):
        """Make sure raw text matches from python."""
        super().test_raw_text_python()

    @_xfail_windows
    def test_standardized_text_cli(self):
        """Make sure standardized text matches from the command line."""
        super().test_standardized_text_cli()

    @_xfail_windows
    def test_standardized_text_python(self):
        """Make sure standardized text matches from python."""
        super().test_standardized_text_python()

    @_xfail_windows
    def test_table_text_python(self):
        """Make sure tables in html look pretty through python."""
        d = pathlib.Path(self.get_extension_directory())
        self.compare_python_output(str(d / "tables.html"))

    @_xfail_windows
    def test_table_text_cli(self):
        """Make sure tables in html look pretty through cli."""
        d = pathlib.Path(self.get_extension_directory())
        self.compare_cli_output(str(d / "tables.html"))
