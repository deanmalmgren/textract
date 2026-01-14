"""Tests for PSV file format."""

import unittest

from . import base


class PsvTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from PSV files."""

    extension = "psv"
