"""Tests for HTML file format."""

from pathlib import Path

from . import base


def test_table_text_python():
    """Make sure tables in html look pretty through python."""
    d = Path(base.get_extension_directory("html"))
    base.compare_python_output(str(d / "tables.html"))


def test_table_text_cli():
    """Make sure tables in html look pretty through cli."""
    d = Path(base.get_extension_directory("html"))
    base.compare_cli_output(str(d / "tables.html"))
