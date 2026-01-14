"""Tests for OGG audio format."""

import unittest

from . import base


class OggTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from OGG audio files."""

    extension = "ogg"
