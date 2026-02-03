import unittest

from . import base


class CsvTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'csv'
