"""Tests for TXT file format."""

from pathlib import Path
import shutil

from . import base

_EXTENSION = "txt"


def test_raw_text_cli():
    base.run_raw_text_cli(_EXTENSION)


def test_raw_text_python():
    base.run_raw_text_python(_EXTENSION)


def test_standardized_text_cli():
    base.run_standardized_text_cli(_EXTENSION)


def test_standardized_text_python():
    base.run_standardized_text_python(_EXTENSION)


def test_extensionless_filenames():
    """Make sure that text from extensionless files is treated as txt."""
    raw_filename = base.raw_text_filename(_EXTENSION)
    temp_filename = base.get_temp_filename()
    shutil.copyfile(raw_filename, temp_filename)
    try:
        base.compare_python_output(temp_filename, raw_filename)
    finally:
        Path(temp_filename).unlink(missing_ok=True)
