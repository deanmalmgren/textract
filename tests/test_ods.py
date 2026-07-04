import unittest

from . import base


class OdsTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = "ods"
