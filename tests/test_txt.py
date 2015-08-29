import unittest
import shutil
import os

import base


class TxtTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'txt'

    def test_extensionless_filenames(self):
        """make sure that text from extensionless files is treated as txt"""
        temp_filename = self.get_temp_filename()
        shutil.copyfile(self.raw_text_filename, temp_filename)
        self.compare_python_output(temp_filename, self.raw_text_filename)
        os.remove(temp_filename)
