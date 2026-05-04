"""Test special character handling in filenames (issue #168)."""
import shutil
import tempfile
import unittest
from pathlib import Path

import pytest

import textract


class TestSpecialFilenames(unittest.TestCase):
    """Test various special characters in filenames."""

    def setup_method(self):
        """Create a temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_test_file(self, filename):
        """Create a test PDF file with the given filename."""
        # Copy a known good PDF file to the test filename
        source = Path(__file__).parent / "pdf" / "raw_text.pdf"
        if not source.exists():
            pytest.skip(f"Test fixture not found: {source}")
        dest = Path(self.temp_dir) / filename
        shutil.copyfile(source, dest)
        return str(dest)

    def _test_filename(self, filename):
        """Test that a filename can be processed without crashing."""
        filepath = self._create_test_file(filename)

        # Test via Python API
        result = textract.process(filepath)
        assert result is not None
        assert len(result) > 0

        # Test via CLI - this is the critical test for shell escaping
        import subprocess

        cmd = ["textract", filepath]
        proc = subprocess.run(
            cmd, capture_output=True, text=True, check=False, timeout=30
        )
        assert proc.returncode == 0, f"CLI failed: {proc.stderr}"

    # Test cases: (description, filename)
    _FILENAME_TEST_CASES = [
        ("unbalanced opening parenthesis", "test(1.pdf"),
        ("unbalanced closing parenthesis", "document).pdf"),
        ("multiple parentheses", "file(with)many)pars.pdf"),
        ("spaces in filename", "file with spaces.pdf"),
        ("ampersand in filename", "file&test.pdf"),
        ("dollar sign in filename", "file$dollar.pdf"),
        ("semicolon in filename", "file;semicolon.pdf"),
        ("pipe in filename", "file|pipe.pdf"),
        ("angle brackets", "file<test>.pdf"),
        ("hash in filename", "file#hash.pdf"),
        ("exclamation in filename", "file!exclaim.pdf"),
        ("backtick in filename", "file`backtick`.pdf"),
        ("quote in filename", 'file"quote".pdf'),
        ("apostrophe in filename", "file'apostrophe.pdf"),
        ("percent in filename", "file%percent.pdf"),
        ("asterisk in filename", "file*asterisk.pdf"),
        ("combined special chars", "file (1) & test $.pdf"),
        ("unicode filename", "文件émoji📄.pdf"),
        (
            "very long filename",
            "file" + " (1)" * 20 + ".pdf",
        ),
    ]

    def test_special_filenames(self):
        """Test that various special characters in filenames are handled correctly."""
        for description, filename in self._FILENAME_TEST_CASES:
            with self.subTest(description=description, filename=filename):
                self._test_filename(filename)