"""Tests for JPG image format."""

from pathlib import Path
import shutil

import pytest

from . import base

_HAS_TESSERACT = shutil.which("tesseract") is not None

pytestmark = pytest.mark.skipif(
    not _HAS_TESSERACT,
    reason="tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)",
)


def _get_jpeg_filename(contents_filename: str) -> str:
    """Return a .jpeg copy of contents_filename (caller must delete)."""
    temp_filename = base.get_temp_filename()
    jpeg_filename = temp_filename + ".jpeg"
    Path(temp_filename).unlink()
    shutil.copyfile(contents_filename, jpeg_filename)
    return jpeg_filename


def test_jpeg_synonym_cli():
    """Make sure .jpeg synonym works in cli."""
    raw_filename = base.raw_text_filename("jpg")
    jpeg_filename = _get_jpeg_filename(raw_filename)
    try:
        base.compare_cli_output(jpeg_filename, base.get_expected_filename(raw_filename))
    finally:
        Path(jpeg_filename).unlink(missing_ok=True)


def test_jpeg_synonym_python():
    """Make sure .jpeg synonym works in python."""
    raw_filename = base.raw_text_filename("jpg")
    jpeg_filename = _get_jpeg_filename(raw_filename)
    try:
        base.compare_python_output(jpeg_filename, base.get_expected_filename(raw_filename))
    finally:
        Path(jpeg_filename).unlink(missing_ok=True)
