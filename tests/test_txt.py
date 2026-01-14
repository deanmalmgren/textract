import pathlib
import shutil
import unittest

from . import base


class TxtTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = "txt"

    def test_extensionless_filenames(self):
        """Make sure that text from extensionless files is treated as txt"""
        temp_filename = self.get_temp_filename()
        shutil.copyfile(self.raw_text_filename, temp_filename)
        self.compare_python_output(temp_filename, self.raw_text_filename)
        pathlib.Path(temp_filename).unlink()
