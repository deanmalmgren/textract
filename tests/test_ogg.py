import unittest

from . import base


class OggTestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'ogg'
