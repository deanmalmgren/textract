"""Tests for TIFF image format."""

import unittest

from . import base


class TiffTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from TIFF images."""

    extension = "tiff"
