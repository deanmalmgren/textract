import unittest
import os
import subprocess

from . import base


class ExceptionTestCase(base.GenericUtilities, unittest.TestCase):
    """This class contains a bunch of tests to make sure that textract
    fails in expected ways.
    """

    def test_unsupported_extension_cli(self):
        """Make sure unsupported extension exits with non-zero status"""
        filename = self.get_temp_filename(extension="extension")
        command = "textract %(filename)s 2> /dev/null" % locals()
        self.assertEqual(1, subprocess.call(command, shell=True))
        os.remove(filename)

    def test_unsupported_extension_python(self):
        """Make sure unsupported extension raises the correct error"""
        filename = self.get_temp_filename(extension="extension")
        import textract
        from textract.exceptions import ExtensionNotSupported
        with self.assertRaises(ExtensionNotSupported):
            textract.process(filename)
        os.remove(filename)

    def test_missing_filename_cli(self):
        """Make sure missing files exits with non-zero status"""
        filename = self.get_temp_filename()
        os.remove(filename)
        command = "textract %(filename)s 2> /dev/null" % locals()
        self.assertEqual(1, subprocess.call(command, shell=True))

    def test_missing_filename_python(self):
        """Make sure missing files raise the correct error"""
        filename = self.get_temp_filename()
        os.remove(filename)
        import textract
        from textract.exceptions import MissingFileError
        with self.assertRaises(MissingFileError):
            textract.process(filename)
