"""Tests for HTML file format."""

import pathlib
import platform
import unittest

import pytest

from . import base


class HtmlTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from HTML files."""

    extension = "html"

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="HTML output varies on Windows due to BeautifulSoup/lxml platform differences",
    )
    def test_raw_text_cli(self):
        """Make sure raw text matches from the command line."""
        return super().test_raw_text_cli()

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="HTML output varies on Windows due to BeautifulSoup/lxml platform differences",
    )
    def test_raw_text_python(self):
        """Make sure raw text matches from python."""
        return super().test_raw_text_python()

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="HTML output varies on Windows due to BeautifulSoup/lxml platform differences",
    )
    def test_standardized_text_cli(self):
        """Make sure standardized text matches from the command line."""
        return super().test_standardized_text_cli()

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="HTML output varies on Windows due to BeautifulSoup/lxml platform differences",
    )
    def test_standardized_text_python(self):
        """Make sure standardized text matches from python."""
        return super().test_standardized_text_python()

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="HTML output varies on Windows due to BeautifulSoup/lxml platform differences",
    )
    def test_table_text_python(self):
        """Make sure tables in html look pretty through python."""
        d = pathlib.Path(self.get_extension_directory())
        self.compare_python_output(str(d / "tables.html"))

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="HTML output varies on Windows due to BeautifulSoup/lxml platform differences",
    )
    def test_table_text_cli(self):
        """Make sure tables in html look pretty through cli."""
        d = pathlib.Path(self.get_extension_directory())
        self.compare_cli_output(str(d / "tables.html"))
