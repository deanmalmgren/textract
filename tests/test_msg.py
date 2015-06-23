import unittest

import base


class MsgTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'msg'

    # # skipping these tests because I can't figure out how to make a damned .msg
    # # file with the standardized text
    # @unittest.skip("skipping standardized text test for .msg")
    # def test_standardized_text_cli(self):
    #     base.BaseBarserTestCase.test_standardized_text_python(self)
    #
    # @unittest.skip("skipping standardized text test for .msg")
    # def test_standardized_text_python(self):
    #     base.BaseBarserTestCase.test_standardized_text_python(self)
