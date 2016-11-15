import unittest

from . import base


class GifTestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'gif'
