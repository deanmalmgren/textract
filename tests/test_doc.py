import unittest

import base


class DocTestCase(unittest.TestCase, base.ShellParserTestCase):
    extension = 'doc'
