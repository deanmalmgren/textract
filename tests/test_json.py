import unittest

from . import base


_ENCODING_TEST_CASES: list[tuple[str, str]] = [
    ("cyrillic", ""),
    ("chinese", ""),
    ("emoji", ""),
    ("mixed_scripts", ""),
]
class JsonTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = "json"



    def test_character_sets_python(self):
        """Test JSON parser with various character encodings via Python API."""
        d = self.get_extension_directory()
        for charset, skip_reason in _ENCODING_TEST_CASES:
            with self.subTest(charset=charset):
                if skip_reason:
                    self.skipTest(skip_reason)
                filename = f"{d}/{charset}.json"
                expected_filename = f"{d}/{charset}.txt"
                self.compare_python_output(filename, expected_filename)
    
    def test_character_sets_cli(self):
        """Test JSON parser with various character encodings via CLI."""
        d = self.get_extension_directory()
        for charset, skip_reason in _ENCODING_TEST_CASES:
            with self.subTest(charset=charset):
                if skip_reason:
                    self.skipTest(skip_reason)
                filename = f"{d}/{charset}.json"
                expected_filename = f"{d}/{charset}.txt"
                self.compare_cli_output(filename, expected_filename)


    def test_explicit_encoding_parameter(self):
        """Test that encoding parameter is respected."""
        filename = self.get_extension_directory() + "/cyrillic.json"
        expected_filename = self.get_extension_directory() + "/cyrillic.txt"
        # Test with explicit UTF-8 encoding
        self.compare_python_output(filename, expected_filename, encoding='utf-8')
