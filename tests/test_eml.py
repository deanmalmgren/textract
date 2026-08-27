import unittest

from . import base


class EmlTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = "eml"

    def test_explicit_input_encoding(self):
        """Regression test for #353: an eml file encoded as cp1251 must be
        readable when input_encoding is specified explicitly."""
        self.assert_input_encoding_respected("cyrillic_cp1251", "cp1251")

    def test_invalid_input_encoding(self):
        """A valid-but-wrong input_encoding must raise a friendly error
        instead of leaking a raw UnicodeDecodeError."""
        self.assert_invalid_input_encoding_raises("cyrillic_cp1251", "ascii")
