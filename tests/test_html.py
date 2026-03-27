"""Tests for HTML file format."""

from pathlib import Path

from . import base

_EXTENSION = "html"


def test_raw_text_cli():
    base.run_raw_text_cli(_EXTENSION)


def test_raw_text_python():
    base.run_raw_text_python(_EXTENSION)


def test_standardized_text_cli():
    base.run_standardized_text_cli(_EXTENSION)


def test_standardized_text_python():
    base.run_standardized_text_python(_EXTENSION)


def test_table_text_python():
    """Make sure tables in html look pretty through python."""
    d = Path(base.get_extension_directory(_EXTENSION))
    base.compare_python_output(str(d / "tables.html"))


def test_table_text_cli():
    """Make sure tables in html look pretty through cli."""
    d = Path(base.get_extension_directory(_EXTENSION))
    base.compare_cli_output(str(d / "tables.html"))
