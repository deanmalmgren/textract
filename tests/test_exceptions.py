import pathlib
import subprocess
import unittest
import uuid

import pytest

from . import base


class ExceptionTestCase(base.GenericUtilities, unittest.TestCase):
    """This class contains a bunch of tests to make sure that textract
    fails in expected ways.
    """

    def test_unsupported_extension_cli(self):
        """Make sure unsupported extension exits with non-zero status."""
        filename = self.get_temp_filename(extension="extension")
        command = "textract {filename} 2> /dev/null".format(**locals())
        assert subprocess.call(command, shell=True) == 1
        pathlib.Path(filename).unlink()

    def test_unsupported_extension_python(self):
        """Make sure unsupported extension raises the correct error."""
        filename = self.get_temp_filename(extension="extension")
        import textract
        from textract.exceptions import ExtensionNotSupported

        with pytest.raises(ExtensionNotSupported):
            textract.process(filename)
        pathlib.Path(filename).unlink()

    def test_missing_filename_cli(self):
        """Make sure missing files exits with non-zero status."""
        filename = self.get_temp_filename()
        pathlib.Path(filename).unlink()
        command = "textract {filename} 2> /dev/null".format(**locals())
        assert subprocess.call(command, shell=True) == 1

    def test_missing_filename_python(self):
        """Make sure missing files raise the correct error."""
        filename = self.get_temp_filename()
        pathlib.Path(filename).unlink()
        import textract
        from textract.exceptions import MissingFileError

        with pytest.raises(MissingFileError):
            textract.process(filename)

    def test_shell_parser_run(self):
        """Get a useful error message when a dependency is missing."""
        from textract.parsers import exceptions, utils

        parser = utils.ShellParser()
        try:
            # There shouldn't be a command on the path matching a random uuid
            parser.run([str(uuid.uuid4())])
        except exceptions.ShellError as e:
            assert e.is_not_installed()
        else:
            raise AssertionError("Expected ShellError")
