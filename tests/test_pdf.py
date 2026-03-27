"""Tests for PDF file format."""

import platform
import shutil
import unittest.mock
from pathlib import Path

import pytest

import textract
from textract.exceptions import ShellError, UnknownMethod
from textract.parsers.pdf_parser import Parser

from . import base

_HAS_PDFTOPPM = shutil.which("pdftoppm") is not None
_HAS_PDFTOTEXT = shutil.which("pdftotext") is not None
_HAS_TESSERACT = shutil.which("tesseract") is not None

_NO_PDFTOPPM_REASON = "pdftoppm is not installed (part of poppler; required for PDF OCR via tesseract)"
_NO_PDFTOTEXT_REASON = "pdftotext is not installed (part of poppler; install via your system package manager, e.g. apt/brew/pacman)"
_NO_TESSERACT_REASON = "tesseract-ocr is not installed (see https://tesseract-ocr.github.io/tessdoc/Installation.html)"
_LINUX_TESSERACT_REASON = "Tesseract OCR output varies by version; Linux CI has different output"
_WINDOWS_PDF_REASON = "PDF content may differ on Windows"

_windows_xfail = pytest.mark.xfail(
    platform.system() == "Windows",
    reason=_WINDOWS_PDF_REASON,
    strict=False,
)

_EXTENSION = "pdf"


@_windows_xfail
def test_filename_spaces():
    base.run_filename_spaces(_EXTENSION)


@_windows_xfail
def test_raw_text_cli():
    base.run_raw_text_cli(_EXTENSION)


@_windows_xfail
def test_raw_text_python():
    base.run_raw_text_python(_EXTENSION)


@_windows_xfail
def test_standardized_text_cli():
    base.run_standardized_text_cli(_EXTENSION)


@_windows_xfail
def test_standardized_text_python():
    base.run_standardized_text_python(_EXTENSION)


@pytest.mark.skipif(not _HAS_PDFTOTEXT, reason=_NO_PDFTOTEXT_REASON)
@_windows_xfail
def test_pdftotext_python():
    base.compare_python_output(base.raw_text_filename(_EXTENSION), method="pdftotext")


@pytest.mark.skipif(not _HAS_PDFTOTEXT, reason=_NO_PDFTOTEXT_REASON)
@_windows_xfail
def test_pdftotext_cli():
    base.compare_cli_output(base.raw_text_filename(_EXTENSION), method="pdftotext")


def test_pdfminer_python():
    base.compare_python_output(base.raw_text_filename(_EXTENSION), method="pdfminer")


def test_pdfminer_cli():
    base.compare_cli_output(base.raw_text_filename(_EXTENSION), method="pdfminer")


@pytest.mark.skipif(not _HAS_PDFTOPPM, reason=_NO_PDFTOPPM_REASON)
@pytest.mark.skipif(not _HAS_TESSERACT, reason=_NO_TESSERACT_REASON)
@pytest.mark.skipif(platform.system() == "Linux", reason=_LINUX_TESSERACT_REASON)
def test_tesseract_python():
    d = Path(base.get_extension_directory(_EXTENSION))
    base.compare_python_output(str(d / "ocr_text.pdf"), method="tesseract")


@pytest.mark.skipif(not _HAS_PDFTOPPM, reason=_NO_PDFTOPPM_REASON)
@pytest.mark.skipif(not _HAS_TESSERACT, reason=_NO_TESSERACT_REASON)
@pytest.mark.skipif(platform.system() == "Linux", reason=_LINUX_TESSERACT_REASON)
def test_tesseract_cli():
    d = Path(base.get_extension_directory(_EXTENSION))
    base.compare_cli_output(str(d / "ocr_text.pdf"), method="tesseract")


@pytest.mark.skipif(
    platform.system() in {"Linux", "Windows"},
    reason="PDF layout extraction varies by platform; character encoding differs",
)
def test_two_column():
    """Preserve two column layout in extraction."""
    d = Path(base.get_extension_directory(_EXTENSION))
    base.compare_python_output(str(d / "two_column.pdf"), layout=True)


def test_unknown_method_raises():
    """Unknown method string raises UnknownMethod."""
    with pytest.raises(UnknownMethod):
        textract.process(base.raw_text_filename(_EXTENSION), method="bogus")


def test_pdftotext_fallback_to_pdfminer():
    """Default method falls back to pdfminer when pdftotext is not installed."""
    with unittest.mock.patch.object(
        Parser,
        "extract_pdftotext",
        side_effect=ShellError("pdftotext", 127, b"", b""),
    ):
        result = textract.process(base.raw_text_filename(_EXTENSION))
    assert result
