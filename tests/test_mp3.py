"""Tests for MP3 audio format."""

import importlib.util
import os
import shutil
import sys

import pytest

from . import base

_HAS_SOX = shutil.which("sox") is not None
_HAS_POCKETSPHINX = importlib.util.find_spec("pocketsphinx") is not None
_SKIP_NETWORK_TESTS = os.environ.get("SKIP_NETWORK_TESTS", "false").lower() == "true"

pytestmark = [
    pytest.mark.skipif(
        not _HAS_SOX,
        reason="sox is not installed (install via your system package manager, e.g. apt/brew/pacman)",
    ),
    pytest.mark.xfail(
        sys.platform == "win32",
        reason="sox.portable on Windows lacks libmad for MP3 decoding",
        strict=True,
    ),
]

_EXTENSION = "mp3"


@pytest.mark.skipif(_SKIP_NETWORK_TESTS, reason="network access required for Google API")
def test_mp3():
    """Make sure default audio method output is correct."""
    base.compare_python_output(base.raw_text_filename(_EXTENSION))


@pytest.mark.skipif(_SKIP_NETWORK_TESTS, reason="network access required for Google API")
def test_mp3_google():
    """Make sure google api python output is correct."""
    base.compare_python_output(base.raw_text_filename(_EXTENSION), method="google")


@pytest.mark.skipif(not _HAS_POCKETSPHINX, reason="pocketsphinx not installed")
def test_mp3_sphinx():
    """Make sure sphinx python output is correct."""
    base.compare_python_output(base.raw_text_filename(_EXTENSION), method="sphinx")
