import os
import unittest

from . import base


class DocxTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = "docx"

    def test_tables(self):
        """Make sure table output is correct."""
        d = self.get_extension_directory()
        self.compare_cli_output(os.path.join(d, "paragraphs_and_tables.docx"))
