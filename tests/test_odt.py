import unittest

from . import base


class OdtTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'odt'
