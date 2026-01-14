"""Tests for PostScript file format."""

import shutil
import unittest

import pytest

from . import base

_HAS_PS2ASCII = shutil.which("ps2ascii") is not None


@pytest.mark.skipif(
    not _HAS_PS2ASCII,
    reason="ps2ascii is not installed (install via: brew install ghostscript)",
)
class PsTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PostScript files."""

    extension = "ps"
