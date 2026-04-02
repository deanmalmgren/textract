import unittest

from . import base


class XlsTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'xls'
