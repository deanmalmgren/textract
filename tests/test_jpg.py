import unittest

import base


class JpgTestCase(unittest.TestCase, base.ShellParserTestCase):
    extension = 'jpg'

    #49TODO add test case for jpeg filename synonym
