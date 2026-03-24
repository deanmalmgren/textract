"""Tests for PostScript file format."""

import shutil
import sys
import unittest

import pytest

from . import base

if sys.platform == 'win32':
    _CAN_PROCESS_PS = shutil.which("gswin64c") is not None
else:
    _CAN_PROCESS_PS = shutil.which("ps2ascii") is not None


@pytest.mark.skipif(
    not _CAN_PROCESS_PS,
    reason="ps2ascii is not installed (part of ghostscript; install via your system package manager, e.g. apt/brew/pacman)",
)
class PsTestCase(base.ShellParserTestCase, unittest.TestCase):
    """Test text extraction from PostScript files."""

    extension = "ps"
