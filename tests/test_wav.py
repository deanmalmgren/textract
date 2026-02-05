"""Tests for WAV audio format."""

import shutil
import unittest

import pytest

from . import base

_HAS_SOX = shutil.which("sox") is not None


@pytest.mark.skipif(
    not _HAS_SOX,
    reason="sox is not installed (install via: brew install sox)",
)
class WavTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from WAV audio files."""

    extension = "wav"
