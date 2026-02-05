import unittest
import os
import subprocess
import uuid

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

    def test_shell_parser_run(self):
        """get a useful error message when a dependency is missing"""
        from textract.parsers import utils
        from textract.parsers import exceptions
        parser = utils.ShellParser()
        try:
            # There shouldn't be a command on the path matching a random uuid
            parser.run([str(uuid.uuid4())])
        except exceptions.ShellError as e:
            self.assertTrue(e.is_not_installed())
        else:
            self.assertTrue(False, "Expected ShellError")

    def test_missing_module_python(self):
        """Make sure not installed modules raises the correct error"""
        filename = self.get_temp_filename()
        import sys
        temp = os
        sys.modules['os'] = None
        import textract
        from textract.exceptions import MissingModuleError
        with self.assertRaises(MissingModuleError):
            textract.process(filename)
        sys.modules['os'] = temp
        os.remove(filename)
