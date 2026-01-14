"""Tests for ODT file format."""

import unittest

from . import base


class OdtTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from ODT files."""

    extension = "odt"
