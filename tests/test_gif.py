"""Tests for GIF image format."""

import unittest

from . import base


class GifTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from GIF images."""

    extension = "gif"
