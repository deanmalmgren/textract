"""Tests for RTF file format."""

import unittest

from . import base


class RtfTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from RTF files."""

    extension = "rtf"
