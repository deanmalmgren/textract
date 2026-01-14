"""Tests for WAV audio format."""

import unittest

from . import base


class WavTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from WAV audio files."""

    extension = "wav"
