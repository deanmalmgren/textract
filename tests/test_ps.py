import unittest

import base


class PsTestCase(unittest.TestCase, base.ShellParserTestCase):
    extension = 'ps'
