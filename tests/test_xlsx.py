"""Tests for XLSX file format."""

import unittest

from . import base


class XlsxTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from XLSX files."""

    extension = "xlsx"
