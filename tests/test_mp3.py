"""Tests for MP3 audio format."""

import shutil
import unittest

import pytest

from . import base

_HAS_SOX = shutil.which("sox") is not None


@pytest.mark.skipif(
    not _HAS_SOX,
    reason="sox is not installed (install via: brew install sox)",
)
class Mp3TestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from MP3 audio files."""

    extension = "mp3"

    def test_mp3(self):
        """Make sure default audio method output is correct."""
        self.compare_python_output(self.raw_text_filename)

    def test_mp3_google(self):
        """Make sure google api python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="google")

    def test_mp3_sphinx(self):
        """Make sure sphinx python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="sphinx")
