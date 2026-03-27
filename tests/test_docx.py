"""Tests for DOCX file format."""

from pathlib import Path

from . import base

_EXTENSION = "docx"


def test_raw_text_cli():
    base.run_raw_text_cli(_EXTENSION)


def test_raw_text_python():
    base.run_raw_text_python(_EXTENSION)


def test_standardized_text_cli():
    base.run_standardized_text_cli(_EXTENSION)


def test_standardized_text_python():
    base.run_standardized_text_python(_EXTENSION)


def test_tables():
    """Make sure table output is correct."""
    d = Path(base.get_extension_directory(_EXTENSION))
    base.compare_cli_output(str(d / "paragraphs_and_tables.docx"))
