import unittest

import base


class DocxTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'docx'
