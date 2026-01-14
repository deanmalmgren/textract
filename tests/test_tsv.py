"""Tests for TSV file format."""

import unittest

from . import base


class TsvTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from TSV files."""

    extension = "tsv"
