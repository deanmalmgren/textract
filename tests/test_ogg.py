"""Tests for OGG audio format."""

import shutil

import pytest

from . import base

_HAS_SOX = shutil.which("sox") is not None

pytestmark = pytest.mark.skipif(
    not _HAS_SOX,
    reason="sox is not installed (install via your system package manager, e.g. apt/brew/pacman)",
)

_EXTENSION = "ogg"


def test_raw_text_cli():
    base.run_raw_text_cli(_EXTENSION)


def test_raw_text_python():
    base.run_raw_text_python(_EXTENSION)


def test_standardized_text_cli():
    base.run_standardized_text_cli(_EXTENSION)


def test_standardized_text_python():
    base.run_standardized_text_python(_EXTENSION)


def test_filename_spaces():
    base.run_filename_spaces(_EXTENSION)
