"""Tests for DOC file format."""

import shutil

import pytest

from . import base

_HAS_ANTIWORD = shutil.which("antiword") is not None

pytestmark = pytest.mark.skipif(
    not _HAS_ANTIWORD,
    reason="antiword is not installed (install via your system package manager)",
)

_EXTENSION = "doc"


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
