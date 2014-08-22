import unittest

import base


class HtmlTestCase(unittest.TestCase, base.BaseParserTestCase):
    extension = 'html'
