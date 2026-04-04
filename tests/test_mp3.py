"""Tests for MP3 audio format."""

import os
import shutil
import sys
import unittest

import pytest

from . import base

_IS_WINDOWS = sys.platform == "win32"

_HAS_SOX = shutil.which("sox") is not None

_SKIP_NETWORK_TESTS = os.environ.get("SKIP_NETWORK_TESTS", "false").lower() == "true"


@pytest.mark.skipif(
    not _HAS_SOX,
    reason="sox is not installed (install via your system package manager, e.g. apt/brew/pacman)",
)
@pytest.mark.xfail(
    _IS_WINDOWS,
    reason="sox.portable on Windows lacks libmad for MP3 decoding",
    strict=True,
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

    def test_mp3_sphinx(self):
        """Make sure sphinx python output is correct."""
        self.compare_python_output(self.raw_text_filename, method="sphinx")
