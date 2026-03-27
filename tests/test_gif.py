"""Tests for GIF image format."""

import shutil

import pytest

from . import base

_HAS_TESSERACT = shutil.which("tesseract") is not None

pytestmark = pytest.mark.skipif(
    not _HAS_TESSERACT,
    reason="tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)",
)

_EXTENSION = "gif"


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
