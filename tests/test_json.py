import unittest

from . import base


class JsonTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'json'
