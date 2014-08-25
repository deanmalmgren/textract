import unittest

import base


class PsTestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'ps'
