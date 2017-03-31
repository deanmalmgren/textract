import unittest

from . import base


class TsvTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'tsv'
