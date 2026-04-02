import unittest

from . import base


class MsgTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = 'msg'
