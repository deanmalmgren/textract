import unittest

from . import base

_ENCODING_TEST_CASES: tuple[str, ...] = (
    "cyrillic",
    "chinese",
    "emoji",
    "mixed_scripts",
)


class JsonTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = "json"

    def test_character_sets_python(self):
        """Test JSON parser with various character encodings via Python API."""
        d = self.get_extension_directory()
        for charset in _ENCODING_TEST_CASES:
            with self.subTest(charset=charset):
                filename = f"{d}/{charset}.json"
                expected_filename = f"{d}/{charset}.txt"
                self.compare_python_output(filename, expected_filename)

    def test_character_sets_cli(self):
        """Test JSON parser with various character encodings via CLI."""
        d = self.get_extension_directory()
        for charset in _ENCODING_TEST_CASES:
            with self.subTest(charset=charset):
                filename = f"{d}/{charset}.json"
                expected_filename = f"{d}/{charset}.txt"
                self.compare_cli_output(filename, expected_filename)

    def test_explicit_input_encoding(self):
        """Regression test for #353: a json file encoded as cp1251 must be
        readable when input_encoding is specified explicitly."""
        self.assert_input_encoding_respected("cyrillic_cp1251", "cp1251")

    def test_invalid_input_encoding(self):
        """A valid-but-wrong input_encoding must raise a friendly error
        instead of leaking a raw UnicodeDecodeError."""
        self.assert_invalid_input_encoding_raises("cyrillic_cp1251", "ascii")
