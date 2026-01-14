"""Tests for XLS file format."""

import unittest

from . import base


class XlsTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from XLS files."""

    extension = "xls"
