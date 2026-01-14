"""Tests for PNG image format."""

import unittest

from . import base


class PngTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PNG images."""

    extension = "png"
