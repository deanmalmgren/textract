import unittest
import os

from . import base


class HtmlTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'html'

    def test_table_text_python(self):
        """Make sure tables in html look pretty through python"""
        d = self.get_extension_directory()
        self.compare_python_output(os.path.join(d, "tables.html"))

    def test_table_text_cli(self):
        """Make sure tables in html look pretty through cli"""
        d = self.get_extension_directory()
        self.compare_cli_output(os.path.join(d, "tables.html"))
