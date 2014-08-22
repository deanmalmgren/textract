import unittest

import base


class XlsxTestCase(unittest.TestCase, base.BaseParserTestCase):
    extension = 'xlsx'
