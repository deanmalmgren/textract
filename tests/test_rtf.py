"""Tests for RTF file format."""

import shutil
import unittest

import pytest

from . import base

_HAS_UNRTF = shutil.which("unrtf") is not None


@pytest.mark.skipif(
    not _HAS_UNRTF,
    reason="unrtf is not installed (install via: brew install unrtf)",
)
class RtfTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from RTF files."""

    extension = "rtf"
