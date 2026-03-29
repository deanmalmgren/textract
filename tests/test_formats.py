"""Parametrized standard extraction tests for all supported file formats."""

from __future__ import annotations

import platform
import shutil
import sys

import pytest

from . import base

_HAS_ANTIWORD = shutil.which("antiword") is not None
_HAS_SOX = shutil.which("sox") is not None
_HAS_TESSERACT = shutil.which("tesseract") is not None
_HAS_UNRTF = shutil.which("unrtf") is not None
_CAN_PROCESS_PS = shutil.which("gswin64c" if sys.platform == "win32" else "ps2ascii") is not None

_skip_antiword = pytest.mark.skipif(
    not _HAS_ANTIWORD,
    reason="antiword is not installed (install via your system package manager)",
)
_skip_sox = pytest.mark.skipif(
    not _HAS_SOX,
    reason="sox is not installed (install via your system package manager, e.g. apt/brew/pacman)",
)
_skip_tesseract = pytest.mark.skipif(
    not _HAS_TESSERACT,
    reason="tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)",
)
_skip_unrtf = pytest.mark.skipif(
    not _HAS_UNRTF,
    reason="unrtf is not installed (install via your system package manager, e.g. apt/brew/pacman)",
)
_skip_ps = pytest.mark.skipif(
    not _CAN_PROCESS_PS,
    reason="ps2ascii is not installed (part of ghostscript; install via your system package manager, e.g. apt/brew/pacman)",
)
_xfail_ps_windows = pytest.mark.xfail(
    platform.system() == "Windows",
    reason="PS text layout may differ between gswin64c txtwrite and ps2ascii",
    strict=False,
)

# All formats supporting the four standard extraction tests (raw/standardized × cli/python).
# pdf is excluded — its standard tests carry per-test marks handled in test_pdf.py.
# mp3 is excluded — its tests use a different structure (method= kwargs, no standard fixtures).
_ALL_FORMATS = [
    "csv",
    pytest.param("doc", marks=_skip_antiword),
    "docx",
    "eml",
    "epub",
    pytest.param("gif", marks=_skip_tesseract),
    "html",
    pytest.param("jpg", marks=_skip_tesseract),
    "json",
    "msg",
    "odt",
    pytest.param("ogg", marks=_skip_sox),
    pytest.param("png", marks=_skip_tesseract),
    "pptx",
    pytest.param("ps", marks=[_skip_ps, _xfail_ps_windows]),
    "psv",
    pytest.param("rtf", marks=_skip_unrtf),
    pytest.param("tiff", marks=_skip_tesseract),
    "tsv",
    "txt",
    pytest.param("wav", marks=_skip_sox),
    "xls",
    "xlsx",
]

# Subset of formats that also support filename-with-spaces tests.
_FILENAME_SPACES_FORMATS = [
    pytest.param("doc", marks=_skip_antiword),
    pytest.param("gif", marks=_skip_tesseract),
    pytest.param("jpg", marks=_skip_tesseract),
    pytest.param("ogg", marks=_skip_sox),
    pytest.param("png", marks=_skip_tesseract),
    pytest.param("ps", marks=[_skip_ps, _xfail_ps_windows]),
    pytest.param("rtf", marks=_skip_unrtf),
    pytest.param("tiff", marks=_skip_tesseract),
    pytest.param("wav", marks=_skip_sox),
]


@pytest.mark.parametrize("ext", _ALL_FORMATS)
def test_raw_text_cli(ext: str) -> None:
    base.run_raw_text_cli(ext)


@pytest.mark.parametrize("ext", _ALL_FORMATS)
def test_raw_text_python(ext: str) -> None:
    base.run_raw_text_python(ext)


@pytest.mark.parametrize("ext", _ALL_FORMATS)
def test_standardized_text_cli(ext: str) -> None:
    base.run_standardized_text_cli(ext)


@pytest.mark.parametrize("ext", _ALL_FORMATS)
def test_standardized_text_python(ext: str) -> None:
    base.run_standardized_text_python(ext)


@pytest.mark.parametrize("ext", _FILENAME_SPACES_FORMATS)
def test_filename_spaces(ext: str) -> None:
    base.run_filename_spaces(ext)
