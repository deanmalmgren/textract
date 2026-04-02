import unittest

from . import base


class PsvTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'psv'
