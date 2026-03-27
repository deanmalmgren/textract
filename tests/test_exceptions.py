"""Tests for error handling."""

import subprocess
import uuid
from pathlib import Path

import pytest

import textract
from textract.exceptions import ExtensionNotSupported, MissingFileError
from textract.parsers import exceptions, utils

from . import base


def test_unsupported_extension_cli():
    """Textract CLI exits with non-zero status for unsupported extensions."""
    filename = base.get_temp_filename(extension="extension")
    result = subprocess.run(
        ["textract", filename],
        stderr=subprocess.DEVNULL,
        check=False,
    )
    assert result.returncode == 1
    Path(filename).unlink()


def test_unsupported_extension_python():
    """Textract raises ExtensionNotSupported for unsupported extensions."""
    filename = base.get_temp_filename(extension="extension")
    try:
        with pytest.raises(ExtensionNotSupported):
            textract.process(filename)
    finally:
        Path(filename).unlink(missing_ok=True)


def test_missing_filename_cli():
    """Textract CLI exits with non-zero status for missing files."""
    filename = base.get_temp_filename()
    Path(filename).unlink()
    result = subprocess.run(
        ["textract", filename],
        stderr=subprocess.DEVNULL,
        check=False,
    )
    assert result.returncode == 1


def test_missing_filename_python():
    """Textract raises MissingFileError for missing files."""
    filename = base.get_temp_filename()
    Path(filename).unlink()
    with pytest.raises(MissingFileError):
        textract.process(filename)


def test_shell_parser_run():
    """ShellParser raises ShellError with is_not_installed() when dependency is missing."""
    parser = utils.ShellParser()
    with pytest.raises(exceptions.ShellError) as exc_info:
        parser.run([str(uuid.uuid4())])
    assert exc_info.value.is_not_installed()
