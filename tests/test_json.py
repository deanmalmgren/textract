"""Tests for JSON file format."""

import unittest

from . import base


class JsonTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from JSON files."""

    extension = "json"
