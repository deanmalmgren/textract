import unittest

from . import base


class PsTestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'ps'
