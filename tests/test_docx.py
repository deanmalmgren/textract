"""Tests for DOCX file format."""

from pathlib import Path

from . import base


def test_tables():
    """Make sure table output is correct."""
    d = Path(base.get_extension_directory("docx"))
    base.compare_cli_output(str(d / "paragraphs_and_tables.docx"))
