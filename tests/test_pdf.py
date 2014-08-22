import unittest

import base


class PdfTestCase(unittest.TestCase, base.ShellParserTestCase):
    extension = 'pdf'

    #49TODO add test case for pdfminer method
