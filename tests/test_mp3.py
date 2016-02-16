import unittest

from . import base


class Mp3TestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'mp3'
