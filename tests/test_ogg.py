"""Tests for OGG audio format."""

import shutil

import pytest

from . import base

_HAS_SOX = shutil.which("sox") is not None


@pytest.mark.skipif(
    not _HAS_SOX,
    reason="sox is not installed (install via your system package manager, e.g. apt/brew/pacman)",
)
class OggTestCase(base.ShellParserTests):
    """Test text extraction from OGG audio files."""

    extension = "ogg"
