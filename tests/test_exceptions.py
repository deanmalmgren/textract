from pathlib import Path
import subprocess
import unittest
import uuid

import pytest

import textract
from textract.exceptions import ExtensionNotSupported, MissingFileError
from textract.parsers import exceptions, utils

from . import base


class ExceptionTestCase(base.GenericUtilities, unittest.TestCase):
    """This class contains a bunch of tests to make sure that textract
    fails in expected ways.
    """

    def test_unsupported_extension_cli(self):
        """Make sure unsupported extension exits with non-zero status."""
        filename = self.get_temp_filename(extension="extension")
        result = subprocess.run(
            ["textract", filename],
            stderr=subprocess.DEVNULL,
            check=False,
        )
        assert result.returncode == 1
        Path(filename).unlink()

    def test_unsupported_extension_python(self):
        """Make sure unsupported extension raises the correct error."""
        filename = self.get_temp_filename(extension="extension")

        with pytest.raises(ExtensionNotSupported):
            textract.process(filename)
        Path(filename).unlink()

    def test_missing_filename_cli(self):
        """Make sure missing files exits with non-zero status."""
        filename = self.get_temp_filename()
        Path(filename).unlink()
        result = subprocess.run(
            ["textract", filename],
            stderr=subprocess.DEVNULL,
            check=False,
        )
        assert result.returncode == 1

    def test_missing_filename_python(self):
        """Make sure missing files raise the correct error."""
        filename = self.get_temp_filename()
        Path(filename).unlink()

        with pytest.raises(MissingFileError):
            textract.process(filename)

    def test_shell_parser_run(self):
        """Get a useful error message when a dependency is missing."""
        parser = utils.ShellParser()
        with pytest.raises(exceptions.ShellError) as exc_info:
            # There shouldn't be a command on the path matching a random uuid
            parser.run([str(uuid.uuid4())])
        assert exc_info.value.is_not_installed()
