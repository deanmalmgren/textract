"""Test special character handling in filenames (issue #168)."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pytest

import textract

_IS_WINDOWS = sys.platform == "win32"


class TestSpecialFilenames(unittest.TestCase):
    """Test handling of special characters in filenames (issue #168)."""

    def setup_method(self, _):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self, _):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_test_file(self, filename):
        source = Path(__file__).parent / "pdf" / "raw_text.pdf"
        if not source.exists():
            pytest.skip(f"Test fixture not found: {source}")
        dest = Path(self.temp_dir) / filename
        shutil.copyfile(source, dest)
        return str(dest)

    def _test_filename(self, filename):
        filepath = self._create_test_file(filename)
        result = textract.process(filepath)
        assert result is not None
        assert len(result) > 0

        proc = subprocess.run(
            ["textract", filepath],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        assert proc.returncode == 0, f"CLI failed: {proc.stderr}"

    def test_unbalanced_parentheses(self):
        """Issue #168: unbalanced parentheses caused crashes."""
        self._test_filename("test(1.pdf")
        self._test_filename("document).pdf")

    def test_shell_injection_chars(self):
        """Characters that could enable shell injection."""
        self._test_filename("file$dollar.pdf")
        self._test_filename("file;semicolon.pdf")

    @pytest.mark.skipif(
        _IS_WINDOWS,
        reason="Windows filesystem does not allow quotes in filenames",
    )
    def test_quotes(self):
        self._test_filename('file"quote".pdf')

    def test_spaces(self):
        """Common in real-world filenames."""
        self._test_filename("file with spaces.pdf")

    def test_combined_special_chars(self):
        self._test_filename("file (1) & test $.pdf")

    @pytest.mark.skipif(
        _IS_WINDOWS,
        reason="Windows external commands do not support unicode filenames",
    )
    def test_unicode_filename(self):
        self._test_filename("文件émoji📄.pdf")

    def test_very_long_filename(self):
        self._test_filename("file" + " (1)" * 20 + ".pdf")
