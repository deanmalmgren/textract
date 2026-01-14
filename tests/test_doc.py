"""Tests for DOC file format."""

import unittest

from . import base


class DocTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from DOC files."""

    extension = "doc"
