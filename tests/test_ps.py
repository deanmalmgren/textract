"""Tests for PostScript file format."""

import platform
import shutil
import sys
import unittest

import pytest

from . import base

if sys.platform == "win32":
    _CAN_PROCESS_PS = shutil.which("gswin64c") is not None
else:
    _CAN_PROCESS_PS = shutil.which("ps2ascii") is not None

_WINDOWS_PS_REASON = "PS text layout may differ between gswin64c txtwrite and ps2ascii"


@pytest.mark.skipif(
    not _CAN_PROCESS_PS,
    reason="ps2ascii is not installed (part of ghostscript; install via your system package manager, e.g. apt/brew/pacman)",
)
@pytest.mark.xfail(
    platform.system() == "Windows",
    reason=_WINDOWS_PS_REASON,
    strict=False,
)
class PsTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PostScript files."""

    extension = "ps"
