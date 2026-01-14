"""Tests for CSV file format."""

import unittest

from . import base


class CsvTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from CSV files."""

    extension = "csv"
