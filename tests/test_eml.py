"""Tests for EML file format."""

import unittest

from . import base


class EmlTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from EML files."""

    extension = "eml"
