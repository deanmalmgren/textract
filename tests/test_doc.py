import unittest

import base


class DocTestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'doc'
