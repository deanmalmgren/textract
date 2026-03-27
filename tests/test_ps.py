"""Tests for PostScript file format."""

import platform
import shutil
import sys

import pytest

from . import base

if sys.platform == "win32":
    _CAN_PROCESS_PS = shutil.which("gswin64c") is not None
else:
    _CAN_PROCESS_PS = shutil.which("ps2ascii") is not None

pytestmark = [
    pytest.mark.skipif(
        not _CAN_PROCESS_PS,
        reason="ps2ascii is not installed (part of ghostscript; install via your system package manager, e.g. apt/brew/pacman)",
    ),
    pytest.mark.xfail(
        platform.system() == "Windows",
        reason="PS text layout may differ between gswin64c txtwrite and ps2ascii",
        strict=False,
    ),
]

_EXTENSION = "ps"


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
