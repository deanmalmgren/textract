"""Tests for DOC file format."""

import unittest

import pytest

from textract.parsers.doc_parser import _find_soffice

from . import base

_HAS_SOFFICE = _find_soffice() is not None


@pytest.mark.skipif(
    not _HAS_SOFFICE,
    reason="LibreOffice (soffice) is not installed",
)
class DocTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from DOC files."""

    extension = "doc"
