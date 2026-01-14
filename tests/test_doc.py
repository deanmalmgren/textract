"""Tests for DOC file format."""

import shutil
import unittest

import pytest

from . import base

_HAS_ANTIWORD = shutil.which("antiword") is not None


@pytest.mark.skipif(
    not _HAS_ANTIWORD,
    reason="antiword is not installed (no longer maintained, install via: brew install antiword)",
)
class DocTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from DOC files."""

    extension = "doc"
