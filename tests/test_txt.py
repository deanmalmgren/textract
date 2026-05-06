"""Tests for TXT file format."""

import shutil
import unittest
from pathlib import Path

from . import base


class TxtTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from TXT files."""

    extension = "txt"

    def test_extensionless_filenames(self):
        """Make sure that text from extensionless files is treated as txt."""
        temp_filename = self.get_temp_filename()
        shutil.copyfile(self.raw_text_filename, temp_filename)
        try:
            self.compare_python_output(temp_filename, self.raw_text_filename)
        finally:
            Path(temp_filename).unlink(missing_ok=True)
