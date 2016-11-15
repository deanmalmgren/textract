import unittest

from . import base


class DocTestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'doc'
