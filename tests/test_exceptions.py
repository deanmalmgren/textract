import subprocess
import unittest
import uuid
from pathlib import Path

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
        try:
            result = subprocess.run(
                ["textract", filename],
                stderr=subprocess.DEVNULL,
                check=False,
            )
        finally:
            Path(filename).unlink(missing_ok=True)
        assert result.returncode == 1

    def test_unsupported_extension_python(self):
        """Make sure unsupported extension raises the correct error."""
        filename = self.get_temp_filename(extension="extension")
        try:
            with pytest.raises(ExtensionNotSupported):
                textract.process(filename)
        finally:
            Path(filename).unlink(missing_ok=True)

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

    def test_shell_parser_run_passes_startupinfo_on_windows(self):
        """On win32, run() must pass a STARTUPINFO that suppresses the console
        window, otherwise every call pops up a cmd window (#180).
        """
        captured_kwargs = {}

        class _FakePipe:
            returncode = 0

            def communicate(self):
                return b"", b""

        def _fake_popen(args, **kwargs):
            captured_kwargs.update(kwargs)
            return _FakePipe()

        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.setattr(utils.sys, "platform", "win32")
            monkeypatch.setattr(
                utils.subprocess,
                "STARTUPINFO",
                lambda: type("_FakeStartupInfo", (), {"dwFlags": 0})(),
                raising=False,
            )
            fake_show_window_flag = 1
            monkeypatch.setattr(
                utils.subprocess,
                "STARTF_USESHOWWINDOW",
                fake_show_window_flag,
                raising=False,
            )
            monkeypatch.setattr(utils.subprocess, "Popen", _fake_popen)

            parser = utils.ShellParser()
            parser.run(["ignored-on-fake-popen"])

        assert "startupinfo" in captured_kwargs
        startupinfo = captured_kwargs["startupinfo"]
        assert startupinfo is not None
        assert startupinfo.dwFlags & fake_show_window_flag
