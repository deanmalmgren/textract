"""Tests for MSG file format."""

import unittest

from . import base


class MsgTestCase(base.BaseParserTestCase, unittest.TestCase):
    """Test text extraction from MSG files."""

    extension = "msg"
