import unittest

from . import base


class RtfTestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'rtf'
