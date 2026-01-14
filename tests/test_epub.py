"""Tests for EPUB file format."""

import unittest

from . import base


class EpubTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from EPUB files."""

    extension = "epub"
