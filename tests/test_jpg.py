"""Tests for JPG image format."""

import shutil
import unittest
from pathlib import Path

import pytest

from . import base

_HAS_TESSERACT = shutil.which("tesseract") is not None


@pytest.mark.skipif(
    not _HAS_TESSERACT,
    reason="tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)",
)
class JpgTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from JPG images."""

    extension = "jpg"

    def get_jpeg_filename(self, contents_filename):
        """Generate JPEG version of file."""
        temp_filename = self.get_temp_filename()
        jpeg_filename = temp_filename + ".jpeg"
        Path(temp_filename).unlink()
        shutil.copyfile(contents_filename, jpeg_filename)
        return jpeg_filename

    def test_jpeg_synonym_cli(self):
        """Make sure .jpeg synonym works in cli."""
        jpeg_filename = self.get_jpeg_filename(self.raw_text_filename)
        try:
            self.compare_cli_output(
                jpeg_filename,
                self.get_expected_filename(self.raw_text_filename),
            )
        finally:
            Path(jpeg_filename).unlink(missing_ok=True)

    def test_jpeg_synonym_python(self):
        """Make sure .jpeg synonym works in python."""
        jpeg_filename = self.get_jpeg_filename(self.raw_text_filename)
        try:
            self.compare_python_output(
                jpeg_filename,
                self.get_expected_filename(self.raw_text_filename),
            )
        finally:
            Path(jpeg_filename).unlink(missing_ok=True)
