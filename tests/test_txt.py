"""Tests for TXT file format."""

from pathlib import Path
import shutil

from . import base


class TxtTestCase(base.BaseParserTests):
    """Test text extraction from TXT files."""

    extension = "txt"

    def test_extensionless_filenames(self):
        """Make sure that text from extensionless files is treated as txt."""
        temp_filename = self.get_temp_filename()
        shutil.copyfile(self.raw_text_filename, temp_filename)
        self.compare_python_output(temp_filename, self.raw_text_filename)
        Path(temp_filename).unlink()
