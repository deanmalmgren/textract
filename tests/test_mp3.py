"""Tests for MP3 audio format."""

import importlib.util
import os
import shutil
import sys
import unittest

import pytest

from . import base

_HAS_SOX = shutil.which("sox") is not None

_HAS_POCKETSPHINX = importlib.util.find_spec("pocketsphinx") is not None

_SKIP_NETWORK_TESTS = os.environ.get("SKIP_NETWORK_TESTS", "false").lower() == "true"


@pytest.mark.skipif(
    not _HAS_SOX,
    reason="sox is not installed (install via: brew install sox)",
)
@pytest.mark.skipif(
    sys.platform == "win32",
    reason="sox.portable on Windows lacks libmad for MP3 decoding",
)
class Mp3TestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from MP3 audio files."""

    extension = "mp3"

    @pytest.mark.skipif(
        _SKIP_NETWORK_TESTS,
        reason="network access required for Google API",
    )
    def test_mp3(self):
        """Make sure default audio method output is correct."""
        self.compare_python_output(self.raw_text_filename)

    @pytest.mark.skipif(
        _SKIP_NETWORK_TESTS,
        reason="network access required for Google API",
    )
    def test_mp3_google(self):
        """Make sure google api python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="google")

    @pytest.mark.skipif(not _HAS_POCKETSPHINX, reason="pocketsphinx not installed")
    def test_mp3_sphinx(self):
        """Make sure sphinx python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="sphinx")
