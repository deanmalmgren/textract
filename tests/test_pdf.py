import unittest
import os
import six

from . import base


class PdfTestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'pdf'

    def test_pdfminer_python(self):
        """make sure pdfminer python output is correct"""
        self.compare_python_output(self.raw_text_filename, method='pdfminer')

    def test_pdfminer_cli(self):
        """make sure pdfminer command line output is correct"""
        self.compare_cli_output(self.raw_text_filename, method='pdfminer')

    def test_tesseract_cli(self):
        """confirm pdf extraction with tesseract"""
        d = self.get_extension_directory()
        self.compare_cli_output(
            os.path.join(d, "ocr_text.pdf"),
            expected_filename=os.path.join(d, "ocr_text.txt"),
            method='tesseract',
        )

    def test_two_column(self):
        """Preserve two column layout in extraction"""
        filename = os.path.join(self.get_extension_directory(), 'two_column.pdf')
        self.compare_python_output(filename, layout=True)
