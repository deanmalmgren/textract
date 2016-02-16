import unittest

from . import base


class WavTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'wav'
