import unittest

from . import base


class EpubTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'epub'
