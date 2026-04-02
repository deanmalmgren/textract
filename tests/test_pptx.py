import unittest

from . import base


class PptxTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'pptx'
