"""Keeps docs/platform_differences.rst in sync with the registry it's generated from."""

import unittest
from pathlib import Path

from .platform_limitations import PLATFORM_LIMITATIONS

_DOCS_PAGE = (
    Path(__file__).resolve().parent.parent / "docs" / "platform_differences.rst"
)


class PlatformLimitationsTestCase(unittest.TestCase):
    def test_docs_mention_every_limitation(self):
        docs_text = _DOCS_PAGE.read_text(encoding="utf-8")
        for limitation in PLATFORM_LIMITATIONS:
            with self.subTest(format=limitation.format):
                assert limitation.format in docs_text
                assert limitation.platform in docs_text
                assert limitation.reason in docs_text
