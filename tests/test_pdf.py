import unittest
import os

import base


class PdfTestCase(unittest.TestCase, base.ShellParserTestCase):
    extension = 'pdf'

    def test_pdfminer_python(self):
        """make sure pdfminer python output is correct"""
        self.compare_python_output(self.raw_text_filename, method='pdfminer')

    def test_pdfminer_cli(self):
        """make sure pdfminer command line output is correct"""
        self.compare_cli_output(self.raw_text_filename, method='pdfminer')

    def test_large_pdf(self):
        """Make sure extraction does not hang (issue #33)"""

        # download the file
        filename = os.path.join(self.get_extension_directory(), "large.pdf")
        self.download_file(
            "https://openknowledge.worldbank.org/bitstream/handle/10986/16091/9780821399378.pdf",
            filename,
        )

        # make sure textract can successfully run
        self.assertSuccessfulTextract(filename)
