"""Tests for TXT file format."""

from pathlib import Path
import shutil

from . import base


def test_extensionless_filenames():
    """Make sure that text from extensionless files is treated as txt."""
    raw_filename = base.raw_text_filename("txt")
    temp_filename = base.get_temp_filename()
    shutil.copyfile(raw_filename, temp_filename)
    try:
        base.compare_python_output(temp_filename, raw_filename)
    finally:
        Path(temp_filename).unlink(missing_ok=True)
