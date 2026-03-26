"""Tests for DOC file format."""

import shutil

import pytest

from . import base

_HAS_ANTIWORD = shutil.which("antiword") is not None


@pytest.mark.skipif(
    not _HAS_ANTIWORD,
    reason=(
        "antiword is not installed (install via your system package manager)"
    ),
)
class DocTestCase(base.ShellParserTests):
    """Test text extraction from DOC files."""

    extension = "doc"
