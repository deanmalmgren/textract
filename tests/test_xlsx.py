import unittest

from . import base


class XlsxTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'xlsx'
