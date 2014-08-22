import unittest

import base


class DocxTestCase(unittest.TestCase, base.BaseParserTestCase):
    extension = 'docx'
