import unittest

import base


class XlsxTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'xlsx'
