import unittest

import base


class HtmlTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'html'
