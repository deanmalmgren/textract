"""Tests for PostScript file format."""

import shutil
import sys
import unittest

import pytest

from . import base

_IS_WINDOWS = sys.platform == "win32"
_CAN_PROCESS_PS = shutil.which("gswin64c" if _IS_WINDOWS else "ps2ascii") is not None

_WINDOWS_PS_REASON = "PS text layout may differ between gswin64c txtwrite and ps2ascii"


@pytest.mark.skipif(
    not _CAN_PROCESS_PS,
    reason="ps2ascii is not installed (part of ghostscript; install via your system package manager, e.g. apt/brew/pacman)",
)
@pytest.mark.xfail(
    _IS_WINDOWS,
    reason=_WINDOWS_PS_REASON,
    strict=False,
)
class PsTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PostScript files."""

    extension = "ps"
