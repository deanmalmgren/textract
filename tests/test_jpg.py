import unittest
import shutil
import os

import base


class JpgTestCase(unittest.TestCase, base.ShellParserTestCase):
    extension = 'jpg'

    def get_jpeg_filename(self, contents_filename):
        jpeg_filename = self.get_temp_filename()
        jpeg_filename += ".jpeg"
        shutil.copyfile(contents_filename, jpeg_filename)
        return jpeg_filename

    def test_jpeg_synonym_cli(self):
        """Make sure .jpeg synonym works in cli"""
        jpeg_filename = self.get_jpeg_filename(self.raw_text_filename)
        self.compare_cli_output(
            jpeg_filename,
            self.get_expected_filename(self.raw_text_filename),
        )
        os.remove(jpeg_filename)

    def test_jpeg_synonym_python(self):
        """Make sure .jpeg synonym works in python"""
        jpeg_filename = self.get_jpeg_filename(self.raw_text_filename)
        self.compare_python_output(
            jpeg_filename,
            self.get_expected_filename(self.raw_text_filename),
        )
        os.remove(jpeg_filename)
        
