"""Tests for OGG audio format."""

import shutil
import unittest

import pytest

from . import base

_HAS_SOX = shutil.which("sox") is not None


@pytest.mark.skipif(
    not _HAS_SOX,
    reason="sox is not installed (install via: brew install sox)",
)
class OggTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from OGG audio files."""

    extension = "ogg"
