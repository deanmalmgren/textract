"""Tests for PostScript file format."""

import unittest

from . import base


class PsTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PostScript files."""

    extension = "ps"
