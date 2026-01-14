"""Tests for PPTX file format."""

import unittest

from . import base


class PptxTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from PPTX files."""

    extension = "pptx"
