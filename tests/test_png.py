"""Tests for PNG image format."""

import shutil

import pytest

from . import base

_HAS_TESSERACT = shutil.which("tesseract") is not None


@pytest.mark.skipif(
    not _HAS_TESSERACT,
    reason="tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)",
)
class PngTestCase(base.ShellParserTests):
    """Test text extraction from PNG images."""

    extension = "png"
