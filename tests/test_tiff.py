import unittest

from . import base


class PngTestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'png'
