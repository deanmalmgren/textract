import unittest

import base


class PdfTestCase(unittest.TestCase, base.ShellParserTestCase):
    extension = 'pdf'

    def test_pdfminer_python(self):
        """make sure pdfminer python output is correct"""
        self.compare_python_output(self.raw_text_filename, method='pdfminer')

    def test_pdfminer_cli(self):
        """make sure pdfminer command line output is correct"""
        self.compare_cli_output(self.raw_text_filename, method='pdfminer')

    #49TODO add test for large file that was causing things to hang a
    #while back
