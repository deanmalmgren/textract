import unittest

from . import base


class EmlTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'csv'
