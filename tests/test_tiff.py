"""Tests for TIFF image format."""

import shutil
import unittest

import pytest

from . import base

_HAS_TESSERACT = shutil.which("tesseract") is not None


@pytest.mark.skipif(
    not _HAS_TESSERACT,
    reason="tesseract-ocr is not installed (install via: brew install tesseract)",
)
class TiffTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from TIFF images."""

    extension = "tiff"
