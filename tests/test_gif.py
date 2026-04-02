"""Tests for GIF image format."""

import shutil
import unittest

import pytest

from . import base

_HAS_TESSERACT = shutil.which("tesseract") is not None


@pytest.mark.skipif(
    not _HAS_TESSERACT,
    reason="tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)",
)
class GifTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from GIF images."""

    extension = "gif"
